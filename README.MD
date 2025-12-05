# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name:

Student Number: 

## Description

This is a Python application that parses ABC music notation files and stores them in a database for analysis. The project reads ABC files from multiple folders (each representing a different book collection), extracts tune information like title, key, meter, and the music notation itself, then saves everything to a SQLite database. After loading the data, you can search and analyze the tunes using either a basic command-line interface or a more visually appealing interface built with the Rich library.

## How to Run

First, make sure you have the required packages installed:

```bash
pip install pandas rich
```

Then you can run the application in two ways:

**Basic version:**
```bash
python app_main.py
```

**Rich version (with better formatting):**
```bash
python app_rich_main.py
```

When you start the application, you'll see a menu with three options:
1. Load ABC data into database - Run this first to parse all the ABC files and populate the database
2. Run user interface - Opens the interactive menu where you can search and analyze tunes
3. Exit

## Features

The application lets you do the following:

- View all tunes from a specific book
- Search for tunes by title
- Filter tunes by musical key (like C major, D minor, etc.)
- Filter tunes by time signature/meter
- See statistics about the tune collection
- Export search results to CSV files

## Project Structure

| File | Purpose |
|------|---------|
| app_main.py | Main entry point for the basic CLI version |
| app_rich_main.py | Main entry point for the Rich-enhanced version |
| abc_parser.py | Functions to find and parse ABC files |
| db_utils.py | Database setup and data loading functions |
| ui_cli.py | Basic command-line user interface |
| ui_rich.py | Enhanced terminal UI using Rich library |
| tune_analysis.py | Data analysis functions using pandas |
| config.py | Configuration for file paths |
| tunes.db | SQLite database file (created after first load) |

## How It Works

The program works in stages. First, it scans the abc_books directory to find all .abc files organized in numbered folders (0, 1, 2, etc.). Each folder represents a book collection. Then it parses each ABC file, extracting information from the header fields like X (reference number), T (title), K (key), M (meter), and the actual music notation. This data gets stored in a SQLite database with columns for book number, filename, tune ID, title, key, meter, and the ABC notation.

Once the database is populated, the UI loads everything into a pandas DataFrame which makes it easy to filter and analyze the data. The basic CLI shows results as plain text while the Rich version adds colors, tables, and progress bars to make it look nicer.

## Screenshots

[Add your screenshots here]

## References

- ABC notation standard: [https://abcnotation.com/](https://abcnotation.com/)
- pandas documentation for data analysis
- Rich library for terminal formatting
- Assignment specification and starter code provided in class

## What I Learned

Working on this project gave me hands-on experience with several important concepts. I got more comfortable with file I/O operations, especially recursively scanning directories and parsing structured text files. The database work helped me understand how to properly design a schema and use SQL with Python through sqlite3. Using pandas for data analysis was interesting because it makes filtering and grouping data much easier than doing it manually with loops.

I also learned about code organization - splitting functionality into separate modules makes the code easier to work with and debug. The Rich library was new to me and it showed me how much better a terminal application can look with some formatting. Overall, this assignment connected a lot of different topics we've covered in the course into one practical application.

## Challenges and Solutions

[Add any specific challenges you faced and how you solved them]
