# ABC Tune Parser - Modular Architecture

This folder contains a clean, modular implementation of the ABC tune parser and analysis system.

## Core Modules

### Configuration
- **`config.py`** - Project paths and constants
  - `BASE_DIR`, `PROJECT_ROOT`, `ABC_ROOT`, `DB_PATH`

### Data Layer
- **`abc_parser.py`** - ABC file parsing logic
  - `find_abc_files()` - Locate all ABC files
  - `parse_abc_file()` - Parse ABC file into tune dictionaries

- **`db_utils.py`** - Database operations
  - `setup_database()` - Create SQLite schema
  - `save_tune_to_database()` - Insert tune records
  - `load_all_abc_data()` - Parse and load all ABC files
  - `load_tunes_from_database()` - Load tunes into DataFrame

### Analysis Layer
- **`tune_analysis.py`** - Query and analysis functions
  - `get_tunes_by_book()` - Filter by book number
  - `get_tunes_by_meter()` - Filter by meter
  - `get_tunes_by_key()` - Filter by key signature
  - `search_tunes()` - Search by title
  - `count_tunes_by_book()` - Count tunes per book
  - `show_tune_statistics()` - Display statistics

### User Interface Layer
- **`ui_cli.py`** - Plain text CLI
  - `show_menu()` - Display menu
  - `run_user_interface()` - Interactive loop

- **`ui_rich.py`** - Rich-enhanced terminal UI ⭐ RECOMMENDED
  - `run_rich_loader()` - Load data with Rich panels
  - `run_rich_ui()` - Interactive UI with tables, colors, panels

### Entry Points
- **`app_main.py`** - Plain CLI entry point
  - `main()` - Start plain text interface

- **`app_rich_main.py`** - Rich UI entry point ⭐ RECOMMENDED
  - `main()` - Start Rich-enhanced interface

### Legacy Files (Kept for Compatibility)
- **`starter_code.py`** - Wrapper delegating to `app_main.py`
- **`database.py`** - Re-exports from new modules for compatibility

---

## How to Run

### Recommended: Rich UI (Impressive Terminal UI)
```powershell
cd C:\Users\nadaa\dcp25-assignment-1
python dcp25-assignment\blob\main\app_rich_main.py
```

### Alternative: Plain CLI
```powershell
cd C:\Users\nadaa\dcp25-assignment-1
python dcp25-assignment\blob\main\app_main.py
```

### Legacy Entry Point
```powershell
cd C:\Users\nadaa\dcp25-assignment-1
python dcp25-assignment\blob\main\starter_code.py
```

---

## First-Time Setup

1. **Install dependencies:**
   ```powershell
   pip install pandas rich
   ```

2. **Load ABC data** (Option 1 in menu):
   - Creates SQLite database
   - Parses all ABC files
   - Inserts tunes into `tunes` table

3. **Explore data** (Option 2 in menu):
   - Search by title, book, meter, key
   - View statistics
   - Browse all tunes

---

## Code Style

All modules use:
- **NumPy-style docstrings** for all public functions
- **Type hints** for parameters and return values
- **Clean separation of concerns** (parsing, database, analysis, UI)

---

## Architecture Benefits

✅ **Modular** - Each module has a single responsibility  
✅ **Testable** - Pure functions, easy to unit test  
✅ **Maintainable** - Small files, clear dependencies  
✅ **Documented** - NumPy docstrings everywhere  
✅ **Extensible** - Easy to add new UIs or analysis functions
