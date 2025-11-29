"""Plain-text command-line user interface.

This module contains a simple non-rich CLI interface that mirrors the
behaviour of the original starter code but delegates work to the
modular helper modules.
"""

from __future__ import annotations

from typing import NoReturn

from db_utils import load_tunes_from_database
from tune_analysis import (
    count_tunes_by_book,
    get_tunes_by_book,
    get_tunes_by_key,
    get_tunes_by_meter,
    search_tunes,
    show_tune_statistics,
)


def show_menu() -> None:
    """Display the main menu options.

    Returns
    -------
    None
        The function prints to standard output.
    """
    print("\n" + "=" * 50)
    print("        ABC TUNE DATABASE EXPLORER")
    print("=" * 50)
    print("1. Search tunes by title")
    print("2. Show tunes by book number")
    print("3. Show tune counts by book")
    print("4. Show tunes by meter")
    print("5. Show tunes by key")
    print("6. Show tune statistics")
    print("7. View all tunes")
    print("8. Exit")
    print("-" * 50)


def run_user_interface() -> NoReturn:
    """Run the interactive command-line interface loop.

    The function loads all tunes from the database into a
    :class:`pandas.DataFrame` and then enters an input loop that
    allows the user to query and inspect the tunes.

    Returns
    -------
    NoReturn
        This function only exits when the user chooses the "Exit"
        option.
    """
    print("Loading data from database...")
    df = load_tunes_from_database()
    print(f"Loaded {len(df)} tunes from database!")

    while True:
        show_menu()
        choice = input("Please enter your choice (1-8): ").strip()

        if choice == "1":
            search_term = input("Enter title to search for: ").strip()
            if search_term:
                results = search_tunes(df, search_term)
                print(f"\nFound {len(results)} tunes:")
                for _, tune in results.iterrows():
                    print(
                        f"  - '{tune['title']}' (Book {tune['book_number']}, Key: {tune['key_signature']})"
                    )
            else:
                print("Please enter a search term!")

        elif choice == "2":
            try:
                book_num = int(input("Enter book number: "))
                results = get_tunes_by_book(df, book_num)
                print(f"\nFound {len(results)} tunes in book {book_num}:")
                for _, tune in results.iterrows():
                    print(
                        f"  - '{tune['title']}' (Key: {tune['key_signature']}, Meter: {tune['meter']})"
                    )
            except ValueError:
                print("Please enter a valid number!")

        elif choice == "3":
            counts = count_tunes_by_book(df)
            print("\nTune counts by book:")
            for book_num, count in counts.items():
                print(f"  Book {book_num}: {count} tunes")

        elif choice == "4":
            meter = input("Enter meter to search for (e.g., 4/4, 3/4): ").strip()
            if meter:
                results = get_tunes_by_meter(df, meter)
                print(f"\nFound {len(results)} tunes in {meter} meter:")
                for _, tune in results.iterrows():
                    print(f"  - '{tune['title']}' (Book {tune['book_number']})")
            else:
                print("Please enter a meter!")

        elif choice == "5":
            key_sig = input("Enter key to search for (e.g., C, G, Dm): ").strip()
            if key_sig:
                results = get_tunes_by_key(df, key_sig)
                print(f"\nFound {len(results)} tunes in key of {key_sig}:")
                for _, tune in results.iterrows():
                    print(f"  - '{tune['title']}' (Book {tune['book_number']})")
            else:
                print("Please enter a key!")

        elif choice == "6":
            show_tune_statistics(df)

        elif choice == "7":
            print(f"\nAll {len(df)} tunes:")
            for _, tune in df.iterrows():
                print(
                    f"  - '{tune['title']}' (Book {tune['book_number']}, Key: {tune['key_signature']})"
                )

        elif choice == "8":
            print("Goodbye!")
            raise SystemExit

        else:
            print("Invalid choice! Please enter 1-8.")

        input("\nPress Enter to continue...")
