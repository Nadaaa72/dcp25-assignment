# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name: Nada Abassi

Student Number: C24317713

## Description

This is a Python application that demonstrates file I/O, database operations, and data analysis through parsing ABC music notation files. The program reads ABC files from multiple folders (each representing a different book collection), extracts tune metadata such as title, key signature, and meter, then stores everything in a SQLite database for efficient searching and filtering.

The application showcases several key programming concepts:
- Directory traversal and file system operations
- Text file parsing with pattern matching
- SQL database design and operations
- Data analysis using pandas DataFrames
- Interactive command-line interface design

## How to Run

**Install Required Dependencies:**

```bash
pip install pandas
```

**Run the Application:**

```bash
python assignment.py
```

**First Time Setup:**
When you first run the program, you'll see a main menu with three options:
1. Load ABC files into database (do this first!)
2. Search and browse tunes
3. Quit

Select option 1 to parse all ABC files and populate the database. This only needs to be done once unless you add new ABC files.

After loading, select option 2 to access the search menu where you can filter and analyze the tune collection.

## Example Usage

```
ABC Tune Parser

What do you want to do?
1. Load ABC files into database (do this first!)
2. Search and browse tunes
3. Quit
Choose (1-3): 1

Loading files...
Reading book 0: hnr1.abc...
  Saved 50 tunes
Reading book 1: hnr2.abc...
  Saved 50 tunes
Done! Loaded 100 tunes.

What do you want to do?
1. Load ABC files into database (do this first!)
2. Search and browse tunes
3. Quit
Choose (1-3): 2

Loading tunes...
Loaded 100 tunes!


1. Search by title
2. Filter by book
3. Count tunes per book
4. Filter by meter
5. Filter by key
6. Show statistics
7. View all tunes
8. Exit
--------------------------------------------------
Choose (1-8): 1

Search for: jig

Found 15 tunes:
  - The Irish Washerwoman (Book 0, Key: G)
  - Morrison's Jig (Book 0, Key: Em)
  - The Priest and His Boots (Book 1, Key: D)
  ...
```

## Features

**Search and Filter Options:**
- Search tunes by title (case-insensitive)
- Filter by book number to see all tunes in a collection
- Filter by musical key signature (C, Dm, G major, etc.)
- Filter by meter/time signature (4/4, 3/4, 6/8, etc.)
- View complete tune collection
- Count tunes per book for quick statistics

**Data Analysis:**
- Display summary statistics (total tunes, number of books)
- Show most common keys and meters
- Pandas DataFrame integration for efficient filtering

## Program Structure

The application is organized into five main sections:

**1. Configuration (lines 18-32)**
- Sets up file paths dynamically for portability
- Locates ABC files folder and database location

**2. File Finding (lines 35-67)**
- `find_abc_files()` - Traverses directory structure to locate all .abc files
- Handles numbered folders representing different book collections

**3. File Parsing (lines 70-139)**
- `read_abc_file()` - Parses ABC notation and extracts metadata
- Handles multiple encoding formats (UTF-8 and latin-1)
- Extracts title, key, meter, and reference number from each tune

**4. Database Operations (lines 142-249)**
- `create_database()` - Sets up SQLite schema
- `save_tune()` - Inserts tune records into database
- `load_all_data()` - ETL pipeline that orchestrates file finding, parsing, and loading
- `load_data()` - Retrieves all tunes as a pandas DataFrame

**5. Analysis & UI (lines 252-467)**
- Search functions using pandas string matching and boolean indexing
- Filter functions for book, meter, and key
- Interactive menu system with user input handling
- `main()` - Program entry point

## How It Works

**Data Loading Process:**
1. The program scans the `abc_books` directory to find all .abc files in numbered subfolders (0, 1, 2, etc.)
2. Each numbered folder represents a different book collection
3. The parser reads each file line by line, identifying header fields:
   - `X:` reference number (marks the start of a new tune)
   - `T:` title
   - `M:` meter (time signature)
   - `K:` key signature
4. Extracted data is stored in a SQLite database with this schema:
   - id, book_number, file_name, reference_number, title, meter, key_signature, raw_abc

**Search and Analysis:**
1. When you open the search menu, all tunes are loaded into a pandas DataFrame
2. DataFrame operations enable fast filtering without repeated database queries
3. Boolean indexing lets you filter on any column (book, key, meter, title)
4. Results display immediately with tune details formatted for readability

## Technical Implementation Details

**Libraries Used:**
- `os` - File system navigation and path manipulation
- `sqlite3` - SQLite database operations
- `pandas` - Data analysis and DataFrame operations

**Key Programming Techniques:**
- Directory traversal using `os.listdir()` and `os.path.join()`
- Text parsing with string methods (`startswith()`, slicing)
- Exception handling for file encoding issues
- SQL parameterized queries to prevent injection
- Pandas boolean indexing for filtering
- While loops for menu systems
- Dictionary operations with `.get()` for safe key access

## Database Schema

```sql
CREATE TABLE tunes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_number INTEGER,
    file_name TEXT,
    reference_number TEXT,
    title TEXT,
    meter TEXT,
    key_signature TEXT,
    raw_abc TEXT
)
```

## Screenshots

[Add screenshots of your program running here]

## What I Learned

This project really helped me understand how different programming concepts work together in a real application. Before this, I had learned about files, databases, and data analysis separately, but putting them all together showed me how they connect.

The file parsing was trickier than I expected. ABC files have a specific format, and I had to be careful about detecting when a new tune starts (the X: field) and handling edge cases like files with multiple tunes or missing fields. I also learned about character encoding - some files wouldn't read with UTF-8 and needed latin-1 encoding instead.

Working with SQLite taught me proper database design. I had to think about what columns to include and what data types to use. The parameterized queries (using ? placeholders) were important for security and I made sure to always commit changes and close connections properly.

Pandas was probably the most useful discovery. Instead of writing complex SQL queries or loops to filter data, I could just load everything into a DataFrame and use simple operations like `data[data["key_signature"] == "C"]`. The boolean indexing concept took a bit to understand but once it clicked, it made filtering so much easier.

The menu system taught me about program flow and user input validation. I had to handle invalid inputs gracefully and make sure the user couldn't break the program by entering unexpected values. Using try/except blocks for the numeric inputs was essential.

One challenge was keeping the code organized and readable. I used clear function names, added comments, and grouped related functionality together. Breaking the program into logical steps (find files, parse files, database operations, search operations, UI) made it much easier to debug and explain.

## References

- ABC notation standard: [https://abcnotation.com/](https://abcnotation.com/)
- Python sqlite3 documentation: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
- pandas documentation: [https://pandas.pydata.org/docs/](https://pandas.pydata.org/docs/)
- Assignment specification provided in class

## Project Files

```
dcp25-assignment-2/
├── abc_books/              # ABC music files organized by book number
│   ├── 0/
│   ├── 1/
│   └── 2/
├── dcp25-assignment/
│   └── blob/
│       └── main/
│           ├── assignment.py    # Main application file (475 lines)
│           └── tunes.db        # SQLite database (created on first run)
├── assignment.md           # Assignment specification
└── README.MD              # This file
```

**Note:** The entire application is contained in a single `assignment.py` file for simplicity and ease of understanding. All functionality - file finding, parsing, database operations, data analysis, and user interface - is organized into clear sections within this one file.

## Summary

This project demonstrates a complete data pipeline from file parsing to database storage to interactive querying. The single-file structure makes it easy to understand the full workflow, while the comprehensive comments make the code suitable for demonstration and explanation. The use of pandas for data analysis shows how higher-level tools can simplify complex filtering operations, and the interactive menu provides a user-friendly way to explore the tune collection.

Key takeaways:
- File I/O with multiple encoding support
- Text parsing with pattern recognition
- SQLite database design and operations
- Pandas DataFrames for data analysis
- Interactive CLI with input validation
- Modular code organization within a single file
