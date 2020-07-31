"""Grammalecte wrapper."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from pprint import pprint
from typing import Generator
from zipfile import ZipFile

import requests

# TODO dataclass
class GrammalecteMessage:
    def __init__(self, line: int, start: int, end: int) -> None:
        self.line = line
        self.start = start
        self.end = end

    def __str__(self):
        return f"Ligne {self.line} [{self.start}:{self.end}]"


class GrammalecteSpellingMessage(GrammalecteMessage):
    def __init__(self, line: int, start: int, end: int, word: str) -> None:
        super().__init__(line, start, end)
        self.word = word

    def __str__(self):
        return super().__str__() + f" Mot inconnu : {self.word}"

    @staticmethod
    def from_dict(line: int, grammalecte_dict: dict) -> GrammalecteMessage:
        return GrammalecteSpellingMessage(
            line,
            int(grammalecte_dict["nStart"]),
            int(grammalecte_dict["nEnd"]),
            grammalecte_dict["sValue"],
        )


def grammalecte(filename: str) -> Generator[GrammalecteMessage, None, None]:
    """Run grammalecte on a file given its path, generate messages."""
    stdout = "[]"
    # TODO check existence of a file
    # TODO use text instead of filename
    print("HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    try:
        result = _run_grammalecte(filename)
        stdout = result.stdout
    except FileNotFoundError as e:
        if e.filename == "grammalecte-cli.py":
            _install_grammalecte()
            result = _run_grammalecte(filename)
            stdout = result.stdout

    warnings = json.loads(stdout)
    pprint(warnings)
    for warning in warnings["data"]:
        print("paragraph")
        lineno = int(warning["iParagraph"])
        for error in warning["lSpellingErrors"]:
            print("error")
            yield GrammalecteSpellingMessage.from_dict(lineno, error)


def _run_grammalecte(filename: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [
            "grammalecte-cli.py",
            "-f",
            filename,
            "-off",
            "apos",
            "--json",
            "--only_when_errors",
        ],
        capture_output=True,
        text=True,
    )


def _install_grammalecte():
    """Install grammalecte CLI."""
    tmpdirname = tempfile.mkdtemp(prefix="grammalecte_")
    tmpdirname = Path(tmpdirname)
    tmpdirname.mkdir(exist_ok=True)
    download_request = requests.get(
        "https://grammalecte.net/grammalecte/zip/Grammalecte-fr-v1.5.0.zip"
    )
    download_request.raise_for_status()
    zip_file = tmpdirname / "Grammalecte-fr-v1.5.0.zip"
    zip_file.write_bytes(download_request.content)
    with ZipFile(zip_file, "r") as zip_obj:
        zip_obj.extractall(tmpdirname / "Grammalecte-fr-v1.5.0")
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            str(tmpdirname / "Grammalecte-fr-v1.5.0"),
        ]
    )
