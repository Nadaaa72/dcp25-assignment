"""Legacy monolithic starter code - now refactored into modules.

This file is kept for backward compatibility and delegates to the
modular application architecture.

For the modular implementation, see:
- config.py: Configuration constants
- abc_parser.py: ABC file parsing logic
- db_utils.py: Database operations
- tune_analysis.py: Analysis and query functions
- ui_cli.py: Plain CLI interface
- ui_rich.py: Rich-enhanced terminal UI
- app_main.py: Plain CLI entry point
- app_rich_main.py: Rich UI entry point (RECOMMENDED)
"""

from __future__ import annotations

from app_main import main

if __name__ == "__main__":
    main()
