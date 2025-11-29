"""ABC tune file parsing utilities.

This module contains functions to locate and parse ABC files into
Python data structures suitable for loading into a database.
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import os

from config import ABC_ROOT


def find_abc_files(root_dir: str | None = None) -> List[Tuple[int, str, str]]:
    """Find all ABC files under the given root directory.

    Parameters
    ----------
    root_dir : str or None, optional
        Root directory that contains numbered subdirectories with
        ``.abc`` files. If ``None``, :data:`config.ABC_ROOT` is used.

    Returns
    -------
    list of tuple of (int, str, str)
        A list of ``(book_number, file_name, full_path)`` triples for
        every ``.abc`` file found.
    """
    if root_dir is None:
        root_dir = ABC_ROOT

    abc_files: List[Tuple[int, str, str]] = []
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path) and item.isdigit():
            book_number = int(item)
            for filename in os.listdir(item_path):
                if filename.lower().endswith(".abc"):
                    full_path = os.path.join(item_path, filename)
                    abc_files.append((book_number, filename, full_path))
    return abc_files


def parse_abc_file(file_path: str, book_number: int, file_name: str) -> List[Dict]:
    """Parse a single ABC file into tune dictionaries.

    Parameters
    ----------
    file_path : str
        Full path to the ABC file on disk.
    book_number : int
        Numeric identifier for the book the file belongs to.
    file_name : str
        Base file name (e.g. ``"hnr0.abc"``).

    Returns
    -------
    list of dict
        A list of dictionaries, one per tune, each containing at
        least ``reference_number``, ``book_number``, ``file_name``,
        ``title``, ``meter``, ``key_signature`` and ``raw_abc`` keys
        where the information is available in the file.
    """
    tunes: List[Dict] = []
    current_tune: Dict = {}
    tune_lines: List[str] = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            lines = [line.strip() for line in f.readlines()]

    for line in lines:
        if not line:
            continue

        if line.startswith("X:") and current_tune:
            current_tune["raw_abc"] = "\n".join(tune_lines)
            tunes.append(current_tune)
            current_tune = {}
            tune_lines = []

        if line.startswith("X:"):
            current_tune["reference_number"] = line[2:].strip()
            current_tune["book_number"] = book_number
            current_tune["file_name"] = file_name
        elif line.startswith("T:") and "title" not in current_tune:
            current_tune["title"] = line[2:].strip()
        elif line.startswith("M:"):
            current_tune["meter"] = line[2:].strip()
        elif line.startswith("K:"):
            current_tune["key_signature"] = line[2:].strip()

        tune_lines.append(line)

    if current_tune:
        current_tune["raw_abc"] = "\n".join(tune_lines)
        tunes.append(current_tune)

    return tunes
