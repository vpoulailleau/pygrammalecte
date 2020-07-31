"""Grammalecte wrapper."""

import subprocess
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

import requests


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
