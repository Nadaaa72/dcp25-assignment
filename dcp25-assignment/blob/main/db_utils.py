"""Database utilities for the ABC tunes project.

This module contains functions responsible for creating the SQLite
schema, inserting tunes and loading them back into pandas
DataFrames.
"""

from __future__ import annotations

from typing import Dict, List
import sqlite3

import pandas as pd

from config import DB_PATH
from abc_parser import find_abc_files, parse_abc_file


def setup_database() -> None:
    """Create the ``tunes`` table if it does not already exist.

    This function connects to the SQLite database pointed to by
    :data:`config.DB_PATH` and issues a ``CREATE TABLE IF NOT EXISTS``
    statement for the ``tunes`` table.

    Returns
    -------
    None
        The function is executed for its side effect of ensuring the
        table exists; it does not return a value.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_number INTEGER,
            file_name TEXT,
            reference_number TEXT,
            title TEXT,
            meter TEXT,
            key_signature TEXT,
            raw_abc TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def save_tune_to_database(tune_data: Dict) -> None:
    """Insert a single tune into the ``tunes`` table.

    Parameters
    ----------
    tune_data : dict
        Dictionary describing the tune. Expected keys include
        ``book_number``, ``file_name``, ``reference_number``,
        ``title``, ``meter``, ``key_signature`` and ``raw_abc``. Any
        missing keys will be replaced with sensible defaults.

    Returns
    -------
    None
        The function is executed for its side effect of inserting a
        row; it does not return a value.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tunes (
            book_number,
            file_name,
            reference_number,
            title,
            meter,
            key_signature,
            raw_abc
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            tune_data.get("book_number"),
            tune_data.get("file_name", ""),
            tune_data.get("reference_number", ""),
            tune_data.get("title", "Unknown Title"),
            tune_data.get("meter", ""),
            tune_data.get("key_signature", ""),
            tune_data.get("raw_abc", ""),
        ),
    )

    conn.commit()
    conn.close()


def load_all_abc_data() -> int:
    """Parse all ABC files and load them into the database.

    The function ensures the database schema exists, walks the
    ``abc_books`` tree, parses each ABC file into tune dictionaries
    and inserts them into the ``tunes`` table.

    Returns
    -------
    int
        Total number of tunes successfully inserted into the
        database.
    """
    setup_database()

    total_tunes = 0
    print("Starting ABC file processing...")

    for book_number, file_name, file_path in find_abc_files():
        print(f"Processing book {book_number}: {file_name}...")
        tunes = parse_abc_file(file_path, book_number, file_name)
        for tune in tunes:
            save_tune_to_database(tune)
        total_tunes += len(tunes)
        print(f"  Inserted {len(tunes)} tunes")

    print(f"\nCompleted! Processed {total_tunes} total tunes.")
    return total_tunes


def load_tunes_from_database() -> pd.DataFrame:
    """Load all tunes from the SQLite database into a DataFrame.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing one row per tune with the columns
        defined by the ``tunes`` table.
    """
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM tunes"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
