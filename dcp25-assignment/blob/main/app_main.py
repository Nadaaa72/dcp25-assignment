"""Application entry point and high-level menu.

This module wires together the database loading and CLI user
interface while delegating detailed work to other modules.
"""

from __future__ import annotations


def main() -> None:
    """Run the main application menu.

    The menu offers options to (1) load ABC data into the database,
    (2) start the interactive user interface and (3) exit.

    Returns
    -------
    None
        The function runs until the user chooses to exit.
    """
    from db_utils import load_all_abc_data
    from ui_cli import run_user_interface

    print("ABC File Parser and Analysis System")
    print("=" * 40)

    while True:
        print("\nMain Options:")
        print("1. Load ABC data into database (run this first)")
        print("2. Run user interface")
        print("3. Exit")

        choice = input("Choose option (1-3): ").strip()

        if choice == "1":
            print("\nLoading ABC data into database...")
            total_tunes = load_all_abc_data()
            print(f"Successfully loaded {total_tunes} tunes into database!")

        elif choice == "2":
            print("\nStarting user interface...")
            run_user_interface()

        elif choice == "3":
            print("Goodbye!")
            break

        else:
            print("Invalid choice! Please enter 1-3.")
