"""Rich-based application entry point.

Use this module to start the application with a Rich-enhanced
terminal UI.
"""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from ui_rich import run_rich_loader, run_rich_ui


console = Console()


def main() -> None:
    """Run the Rich-styled main menu.

    Returns
    -------
    None
        The function runs until the user chooses to exit.
    """
    console.print(Panel.fit("[bold cyan]ABC File Parser and Analysis System[/bold cyan]"))

    while True:
        console.print(
            Panel(
                """[bold]Main Options[/bold]\n\n
[1] Load ABC data into database (run this first)\n
[2] Run Rich user interface\n
[3] Exit""",
                border_style="cyan",
            )
        )

        choice = Prompt.ask("[bold]Choose option (1-3)[/bold]")

        if choice == "1":
            run_rich_loader()
        elif choice == "2":
            run_rich_ui()
        elif choice == "3":
            console.print("[bold magenta]Goodbye![/bold magenta]")
            break
        else:
            console.print("[red]Invalid choice! Please enter 1-3.[/red]")


if __name__ == "__main__":
    main()
