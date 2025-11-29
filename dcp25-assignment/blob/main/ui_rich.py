"""Rich-based terminal user interface for the ABC tunes project.

This module provides an interactive UI using the :mod:`rich` library.
"""

from __future__ import annotations

from typing import NoReturn

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table

from db_utils import load_tunes_from_database, load_all_abc_data
from tune_analysis import (
    count_tunes_by_book,
    get_tunes_by_book,
    get_tunes_by_key,
    get_tunes_by_meter,
    search_tunes,
    show_tune_statistics,
)


console = Console()


def _render_tunes_table(df: pd.DataFrame, title: str) -> None:
    """Render a DataFrame of tunes as a Rich table.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with tune data.
    title : str
        Title to display above the table.
    """
    if df.empty:
        console.print(Panel.fit("[bold yellow]No tunes found.[/bold yellow]", title=title))
        return

    table = Table(title=title, show_lines=True)
    table.add_column("ID", style="dim", justify="right")
    table.add_column("Title", style="bold")
    table.add_column("Book", justify="right")
    table.add_column("Key")
    table.add_column("Meter")

    for _, tune in df.iterrows():
        table.add_row(
            str(tune.get("id", "")),
            str(tune.get("title", "")),
            str(tune.get("book_number", "")),
            str(tune.get("key_signature", "")),
            str(tune.get("meter", "")),
        )

    console.print(table)


def run_rich_loader() -> int:
    """Load all ABC data into the database with a Rich progress bar.

    Returns
    -------
    int
        Number of tunes loaded into the database.
    """
    console.print(Panel.fit("[bold cyan]Loading ABC data into database...[/bold cyan]"))
    # Delegate to plain loader which already prints progress
    total_tunes = load_all_abc_data()
    console.print(
        Panel.fit(
            f"[bold green]Successfully loaded {total_tunes} tunes into database![/bold green]",
            border_style="green",
        )
    )
    return total_tunes


def run_rich_ui() -> NoReturn:
    """Run the Rich-based interactive user interface loop.

    Returns
    -------
    NoReturn
        The loop only exits when the user chooses the exit option.
    """
    console.print(Panel.fit("[bold cyan]Loading data from database...[/bold cyan]"))
    df = load_tunes_from_database()
    console.print(
        Panel.fit(
            f"[bold green]Loaded {len(df)} tunes from database![/bold green]",
            border_style="green",
        )
    )

    while True:
        console.print(
            Panel(
                """[bold]ABC TUNE DATABASE EXPLORER[/bold]\n\n
[1] Search tunes by title\n
[2] Show tunes by book number\n
[3] Show tune counts by book\n
[4] Show tunes by meter\n
[5] Show tunes by key\n
[6] Show tune statistics\n
[7] View all tunes\n
[8] Exit""",
                title="Main Menu",
                border_style="cyan",
            )
        )

        choice = Prompt.ask("[bold]Please enter your choice (1-8)[/bold]")

        if choice == "1":
            search_term = Prompt.ask("Enter title to search for").strip()
            if search_term:
                results = search_tunes(df, search_term)
                _render_tunes_table(results, f"Search results for '{search_term}'")
            else:
                console.print("[yellow]Please enter a search term![/yellow]")

        elif choice == "2":
            try:
                book_num = IntPrompt.ask("Enter book number")
                results = get_tunes_by_book(df, book_num)
                _render_tunes_table(results, f"Tunes in book {book_num}")
            except Exception:
                console.print("[red]Please enter a valid number![/red]")

        elif choice == "3":
            counts = count_tunes_by_book(df)
            table = Table(title="Tune counts by book", show_lines=True)
            table.add_column("Book", justify="right")
            table.add_column("Count", justify="right")
            for book_num, count in counts.items():
                table.add_row(str(book_num), str(count))
            console.print(table)

        elif choice == "4":
            meter = Prompt.ask("Enter meter to search for (e.g., 4/4, 3/4)").strip()
            if meter:
                results = get_tunes_by_meter(df, meter)
                _render_tunes_table(results, f"Tunes in meter {meter}")
            else:
                console.print("[yellow]Please enter a meter![/yellow]")

        elif choice == "5":
            key_sig = Prompt.ask("Enter key to search for (e.g., C, G, Dm)").strip()
            if key_sig:
                results = get_tunes_by_key(df, key_sig)
                _render_tunes_table(results, f"Tunes in key {key_sig}")
            else:
                console.print("[yellow]Please enter a key![/yellow]")

        elif choice == "6":
            # Re-use existing statistics printer but wrap header with Rich
            console.print(Panel.fit("[bold cyan]Tune statistics[/bold cyan]"))
            show_tune_statistics(df)

        elif choice == "7":
            _render_tunes_table(df, "All tunes")

        elif choice == "8":
            console.print("[bold magenta]Goodbye![/bold magenta]")
            raise SystemExit

        else:
            console.print("[red]Invalid choice! Please enter 1-8.[/red]")

        Prompt.ask("Press Enter to continue", default="")
