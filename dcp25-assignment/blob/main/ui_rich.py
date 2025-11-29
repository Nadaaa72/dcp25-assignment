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
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.layout import Layout
from rich.text import Text
from rich import box

from db_utils import load_tunes_from_database, setup_database, save_tune_to_database
from abc_parser import find_abc_files, parse_abc_file
from tune_analysis import (
    count_tunes_by_book,
    get_tunes_by_book,
    get_tunes_by_key,
    get_tunes_by_meter,
    search_tunes,
    show_tune_statistics,
)


console = Console()


def _create_bar_chart(data: pd.Series, max_width: int = 30) -> str:
    """Create a simple ASCII bar chart from a pandas Series.
    
    Parameters
    ----------
    data : pandas.Series
        Data to visualize (index as labels, values as counts).
    max_width : int
        Maximum width of the longest bar.
    
    Returns
    -------
    str
        Formatted bar chart string.
    """
    if data.empty:
        return "No data"
    
    max_value = data.max()
    lines = []
    
    for label, value in data.items():
        bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
        bar = "█" * bar_length
        lines.append(f"{str(label):>10} │ {bar} {value}")
    
    return "\n".join(lines)


def _show_fancy_statistics(df: pd.DataFrame) -> None:
    """Display fancy statistics with Rich panels and visual elements.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing all tunes.
    
    Returns
    -------
    None
        Displays statistics to the console.
    """
    # Main statistics panel
    stats_text = Text()
    stats_text.append("📊 Total Tunes: ", style="bold cyan")
    stats_text.append(f"{len(df):,}\n", style="bold yellow")
    stats_text.append("📚 Number of Books: ", style="bold cyan")
    stats_text.append(f"{df['book_number'].nunique()}\n", style="bold yellow")
    
    console.print(Panel(stats_text, title="[bold magenta]Overview[/bold magenta]", border_style="magenta"))
    
    # Top 10 Keys with bar chart
    top_keys = df['key_signature'].value_counts().head(10)
    keys_chart = _create_bar_chart(top_keys, max_width=40)
    
    console.print(Panel(
        f"[cyan]{keys_chart}[/cyan]",
        title="[bold green]🎵 Top 10 Most Common Keys[/bold green]",
        border_style="green",
        box=box.ROUNDED
    ))
    
    # Top 10 Meters with bar chart
    top_meters = df['meter'].value_counts().head(10)
    meters_chart = _create_bar_chart(top_meters, max_width=40)
    
    console.print(Panel(
        f"[yellow]{meters_chart}[/yellow]",
        title="[bold blue]🎼 Top 10 Most Common Meters[/bold blue]",
        border_style="blue",
        box=box.ROUNDED
    ))
    
    # Tunes per book table
    book_counts = count_tunes_by_book(df)
    book_table = Table(title="📖 Tunes per Book", box=box.DOUBLE_EDGE, show_header=True, header_style="bold magenta")
    book_table.add_column("Book", justify="center", style="cyan")
    book_table.add_column("Count", justify="center", style="green")
    book_table.add_column("Percentage", justify="center", style="yellow")
    
    total = len(df)
    for book_num, count in book_counts.items():
        percentage = (count / total * 100) if total > 0 else 0
        book_table.add_row(
            str(book_num),
            f"{count:,}",
            f"{percentage:.1f}%"
        )
    
    console.print(book_table)


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
        console.print(Panel.fit("[bold yellow]❌ No tunes found.[/bold yellow]", title=title, border_style="yellow"))
        return

    table = Table(
        title=f"🎵 {title}",
        show_lines=True,
        box=box.ROUNDED,
        title_style="bold magenta",
        header_style="bold cyan"
    )
    table.add_column("ID", style="dim", justify="right", width=6)
    table.add_column("Title", style="bold green", no_wrap=False)
    table.add_column("Book", justify="center", style="cyan", width=6)
    table.add_column("Key", style="yellow", width=8)
    table.add_column("Meter", style="magenta", width=8)

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
    
    # Setup database schema first
    setup_database()
    
    # Find all ABC files to process
    all_files = find_abc_files()
    total_tunes = 0
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("[cyan]{task.fields[info]}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        
        main_task = progress.add_task(
            "[cyan]Processing ABC files...",
            total=len(all_files),
            info="Starting..."
        )
        
        for book_number, file_name, file_path in all_files:
            # Update progress with current file
            progress.update(
                main_task,
                info=f"Book {book_number}: {file_name}"
            )
            
            # Parse and save tunes
            tunes = parse_abc_file(file_path, book_number, file_name)
            for tune in tunes:
                save_tune_to_database(tune)
            
            total_tunes += len(tunes)
            progress.advance(main_task)
        
        # Final update
        progress.update(
            main_task,
            info=f"✓ Loaded {total_tunes} tunes from {len(all_files)} files"
        )
    
    console.print(
        Panel.fit(
            f"[bold green]✓ Successfully loaded {total_tunes} tunes into database![/bold green]",
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
            table = Table(
                title="📚 Tune Counts by Book",
                show_lines=True,
                box=box.DOUBLE_EDGE,
                title_style="bold magenta",
                header_style="bold cyan"
            )
            table.add_column("Book", justify="center", style="cyan")
            table.add_column("Count", justify="center", style="green")
            table.add_column("Bar", justify="left")

            max_count = counts.max() if not counts.empty else 1
            for book_num, count in counts.items():
                bar_length = int((count / max_count) * 30) if max_count > 0 else 0
                bar = "█" * bar_length
                table.add_row(str(book_num), f"{count:,}", f"[yellow]{bar}[/yellow]")
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
            _show_fancy_statistics(df)

        elif choice == "7":
            _render_tunes_table(df, "All tunes")

        elif choice == "8":
            console.print("[bold magenta]Goodbye![/bold magenta]")
            raise SystemExit

        else:
            console.print("[red]Invalid choice! Please enter 1-8.[/red]")

        Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
