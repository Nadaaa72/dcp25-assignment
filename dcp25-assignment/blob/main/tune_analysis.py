"""Analysis helpers for working with tune DataFrames."""

from __future__ import annotations

import pandas as pd


def get_tunes_by_book(df: pd.DataFrame, book_number: int) -> pd.DataFrame:
    """Filter tunes by book number.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.
    book_number : int
        Book number to select.

    Returns
    -------
    pandas.DataFrame
        Subset of ``df`` containing only rows whose
        ``book_number`` matches ``book_number``.
    """
    return df[df["book_number"] == book_number]


def get_tunes_by_meter(df: pd.DataFrame, meter: str) -> pd.DataFrame:
    """Filter tunes by meter string.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.
    meter : str
        Meter value to filter for, e.g. ``"4/4"``.

    Returns
    -------
    pandas.DataFrame
        Subset of ``df`` with the given meter.
    """
    return df[df["meter"] == meter]


def get_tunes_by_key(df: pd.DataFrame, key_sig: str) -> pd.DataFrame:
    """Filter tunes by key signature.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.
    key_sig : str
        Key signature to filter for, e.g. ``"C"`` or ``"Dm"``.

    Returns
    -------
    pandas.DataFrame
        Subset of ``df`` with the given key signature.
    """
    return df[df["key_signature"] == key_sig]


def search_tunes(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search tunes by (case-insensitive) substring in the title.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.
    search_term : str
        Substring to search for in tune titles.

    Returns
    -------
    pandas.DataFrame
        Subset of ``df`` whose ``title`` column contains
        ``search_term``.
    """
    return df[df["title"].str.contains(search_term, case=False, na=False)]


def count_tunes_by_book(df: pd.DataFrame) -> pd.Series:
    """Count the number of tunes for each book.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.

    Returns
    -------
    pandas.Series
        A Series indexed by book number with counts as values.
    """
    return df["book_number"].value_counts().sort_index()


def show_tune_statistics(df: pd.DataFrame) -> None:
    """Print basic statistics about the collection of tunes.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.

    Returns
    -------
    None
        The function prints to standard output and does not
        return a value.
    """
    print(f"Total number of tunes: {len(df)}")
    print(f"Number of books: {df['book_number'].nunique()}")
    print(f"Most common keys: {df['key_signature'].value_counts().head(5)}")
    print(f"Most common meters: {df['meter'].value_counts().head(5)}")
