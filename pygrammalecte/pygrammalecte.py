"""Grammalecte wrapper."""

import io
import json
import os
import subprocess
import sys
import sysconfig
import tempfile
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator, List, Union
from zipfile import ZipFile

import requests


@dataclass
class GrammalecteMessage:
    """Base class for Grammalecte messages."""

    line: int
    start: int
    end: int

    def __str__(self):
        return f"Ligne {self.line} [{self.start}:{self.end}]"

    def __eq__(self, other: "GrammalecteMessage"):
        # to be sortable, but misleading equality usage
        return (self.line, self.start, self.end) == (other.line, other.start, other.end)

    def __lt__(self, other: "GrammalecteMessage"):
        return (self.line, self.start, self.end) < (other.line, other.start, other.end)


@dataclass
class GrammalecteSpellingMessage(GrammalecteMessage):
    """Spelling error message."""

    word: str
    message: str = field(init=False)

    def __post_init__(self):
        self.message = f"Mot inconnu : {self.word}"

    def __str__(self):
        return super().__str__() + " " + self.message

    @staticmethod
    def from_dict(line: int, grammalecte_dict: dict) -> "GrammalecteSpellingMessage":
        """Instanciate GrammalecteSpellingMessage from Grammalecte result."""
        return GrammalecteSpellingMessage(
            line=line,
            start=int(grammalecte_dict["nStart"]),
            end=int(grammalecte_dict["nEnd"]),
            word=grammalecte_dict["sValue"],
        )


@dataclass
class GrammalecteGrammarMessage(GrammalecteMessage):
    """Grammar error message."""

    url: str
    color: List[int]
    suggestions: List[str]
    message: str
    rule: str
    type: str

    def __str__(self):
        ret = super().__str__() + f" [{self.rule}] {self.message}"
        if self.suggestions:
            ret += f" (Suggestions : {', '.join(self.suggestions)})"
        return ret

    @staticmethod
    def from_dict(line: int, grammalecte_dict: dict) -> "GrammalecteGrammarMessage":
        """Instanciate GrammalecteGrammarMessage from Grammalecte result."""
        return GrammalecteGrammarMessage(
            line=line,
            start=int(grammalecte_dict["nStart"]),
            end=int(grammalecte_dict["nEnd"]),
            url=grammalecte_dict["URL"],
            color=grammalecte_dict["aColor"],
            suggestions=grammalecte_dict["aSuggestions"],
            message=grammalecte_dict["sMessage"].replace("“", "« ").replace("”", " »"),
            rule=grammalecte_dict["sRuleId"],
            type=grammalecte_dict["sType"],
        )


def grammalecte_text(text: str) -> Generator[GrammalecteMessage, None, None]:
    """Run grammalecte on a string, generate messages."""
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfile = Path(tmpdirname) / "file.txt"
        tmpfile.write_text(text, encoding="utf-8")
        yield from grammalecte_file(tmpfile)


def grammalecte_file(
    filename: Union[str, Path],
) -> Generator[GrammalecteMessage, None, None]:
    """Run grammalecte on a file given its path, generate messages."""
    stdout = '{"data":[]}'
    filename = str(filename)
    try:
        stdout = _run_grammalecte(filename)
    except FileNotFoundError as e:
        if e.filename == "grammalecte-cli.py":
            _install_grammalecte()
            stdout = _run_grammalecte(filename)
    yield from _convert_to_messages(stdout)


def _convert_to_messages(
    grammalecte_json: str,
) -> Generator[GrammalecteMessage, None, None]:
    # grammalecte 1.12.0 adds python comments in the JSON!
    grammalecte_json_str = "\n".join(
        line for line in grammalecte_json.splitlines() if not line.startswith("#")
    )
    warnings = json.loads(grammalecte_json_str)
    for warning in warnings["data"]:
        lineno = int(warning["iParagraph"])
        messages = []
        for error in warning["lGrammarErrors"]:
            messages.append(GrammalecteGrammarMessage.from_dict(lineno, error))
        for error in warning["lSpellingErrors"]:
            messages.append(GrammalecteSpellingMessage.from_dict(lineno, error))
        for message in sorted(messages):
            yield message


def _run_grammalecte(filepath: str) -> str:
    """Run Grammalecte on a file."""
    grammalecte_script = Path(sysconfig.get_paths()["scripts"]) / "grammalecte-cli.py"
    if not grammalecte_script.exists():
        exc = FileNotFoundError()
        exc.filename = "grammalecte-cli.py"
        raise exc

    # can be done only here, after the installation is properly done
    from grammalecte.grammalecte_cli import main

    old_args = list(sys.argv)
    sys.argv = [
        "grammalecte_cli.py",
        "-f",
        filepath,
        "-off",
        "apos",
        "--json",
        "--only_when_errors",
    ]

    with redirect_stdout(io.StringIO()) as stdout:
        main()

    sys.argv = old_args
    return stdout.getvalue()


def _install_grammalecte():
    """Install grammalecte CLI."""
    version = "2.1.1"
    tmpdirname = tempfile.mkdtemp(prefix="grammalecte_")
    tmpdirname = Path(tmpdirname)
    tmpdirname.mkdir(exist_ok=True)
    download_request = requests.get(
        f"https://grammalecte.net/zip/Grammalecte-fr-v{version}.zip"
    )
    download_request.raise_for_status()
    zip_file = tmpdirname / f"Grammalecte-fr-v{version}.zip"
    zip_file.write_bytes(download_request.content)
    with ZipFile(zip_file, "r") as zip_obj:
        zip_obj.extractall(tmpdirname / f"Grammalecte-fr-v{version}")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            str(tmpdirname / f"Grammalecte-fr-v{version}"),
        ]
    )

    grammalecte_script = Path(sysconfig.get_paths()["scripts"]) / "grammalecte-cli.py"
    grammalecte_dir = Path(sysconfig.get_paths()["purelib"]) / "grammalecte"

    importable_grammalecte_script = grammalecte_dir / "grammalecte_cli.py"
    importable_grammalecte_script.write_bytes(grammalecte_script.read_bytes())

    echo_file = grammalecte_dir / "graphspell" / "echo.py"
    content = echo_file.read_text(encoding="utf-8")
    content = content.replace("file=file, ", "")
    echo_file.write_text(content, encoding="utf-8")
