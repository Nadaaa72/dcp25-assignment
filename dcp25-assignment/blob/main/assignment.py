"""
ABC File Parser 

This program demonstrates file I/O, database operations, and data analysis.
The workflow is:
1. Find ABC music notation files in a folder structure
2. Parse them to extract tune metadata (title, key, meter, etc.)
3. Store everything in a SQLite database
4. Provide an interactive menu for searching and filtering the data
"""

# Import the libraries we need for this project
import os  # for navigating directories and finding files
import sqlite3  # for creating and querying the SQLite database
import pandas as pd  # for data analysis and filtering with DataFrames


# CONFIGURATION SECTION
# These paths locate the data files and database

# Get the directory where this Python file is located
this_file_location: str = os.path.dirname(os.path.abspath(__file__))

# Navigate up 3 levels to reach the project root
# This makes the code portable - works on any computer
project_folder: str = os.path.dirname(os.path.dirname(os.path.dirname(this_file_location)))

# Path to the folder containing ABC music files organized in numbered subfolders
abc_folder: str = os.path.join(project_folder, "abc_books")

# Path where we'll create/access the SQLite database file
database_file: str = os.path.join(this_file_location, "tunes.db")


# STEP 1: FIND ABC FILES
# This demonstrates recursive directory traversal
def find_abc_files():
    """
    Find all .abc files in the abc_books folder.
    
    This shows how to navigate a folder structure programmatically.
    The abc_books folder contains numbered subfolders (0, 1, 2, etc.)
    where each subfolder represents a "book" collection of tunes.
    """
    # Initialize an empty list - we'll accumulate results here
    files_found = []
    
    # os.listdir() returns all items (files and folders) in the directory
    for folder_name in os.listdir(abc_folder):
        # Build the complete path to this item
        folder_path = os.path.join(abc_folder, folder_name)
        
        # We only want folders that have numeric names (representing book numbers)
        # isdigit() checks if the string is all digits like "0", "1", "2"
        if os.path.isdir(folder_path) and folder_name.isdigit():
            book_num = int(folder_name)  # convert "1" to 1
            
            # Now look at every file inside this book folder
            for file_name in os.listdir(folder_path):
                # Filter for only .abc files (case-insensitive check)
                if file_name.lower().endswith(".abc"):
                    file_path = os.path.join(folder_path, file_name)
                    # Store as tuple: (book_number, filename, full_path)
                    # This keeps all related info together
                    files_found.append((book_num, file_name, file_path))
    
    return files_found


# STEP 2: PARSE ABC FILES
# This demonstrates text file parsing and data extraction
def read_abc_file(file_path, book_num, file_name):
    """
    Parse one ABC file and extract tune information.
    
    ABC notation uses header fields like:
    X: reference number
    T: title
    M: meter (time signature)
    K: key signature
    
    This parser extracts those fields and returns structured data.
    """
    # This list will hold all tunes found in this file
    all_tunes = []
    
    # Variables to track the current tune being parsed
    current_tune = {}  # dictionary to store tune metadata
    current_tune_lines = []  # list to accumulate all lines of the tune
    
    # File encoding handling - try UTF-8 first, fallback to latin-1
    # This is important because music files might use special characters
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        with open(file_path, "r", encoding="latin-1") as f:
            lines = f.readlines()
    
    # Process each line of the file
    for line in lines:
        line = line.strip()  # remove leading/trailing whitespace
        
        if not line:  # skip blank lines
            continue
        
        # X: indicates the start of a new tune
        # If we already have tune data, save it before starting the new one
        if line.startswith("X:") and current_tune:
            # Join all lines into a single string for storage
            current_tune["raw_abc"] = "\n".join(current_tune_lines)
            all_tunes.append(current_tune)
            # Reset variables for the next tune
            current_tune = {}
            current_tune_lines = []
        
        # Extract metadata from header fields
        # line[2:] gets everything after the field marker (X:, T:, etc.)
        if line.startswith("X:"):
            current_tune["reference_number"] = line[2:].strip()
            current_tune["book_number"] = book_num
            current_tune["file_name"] = file_name
        elif line.startswith("T:") and "title" not in current_tune:
            # Only take the first title if there are multiple T: lines
            current_tune["title"] = line[2:].strip()
        elif line.startswith("M:"):
            current_tune["meter"] = line[2:].strip()
        elif line.startswith("K:"):
            current_tune["key_signature"] = line[2:].strip()
        
        # Accumulate every line for the raw ABC notation
        current_tune_lines.append(line)
    
    # Don't forget to save the last tune in the file
    if current_tune:
        current_tune["raw_abc"] = "\n".join(current_tune_lines)
        all_tunes.append(current_tune)
    
    return all_tunes


# STEP 3: DATABASE OPERATIONS
# This demonstrates SQL database creation and data persistence

def create_database():
    """Create the SQLite database table to store tune information."""
    # sqlite3.connect() creates the database file if it doesn't exist
    # Returns a connection object for interacting with the database
    conn = sqlite3.connect(database_file)
    
    # Cursor object lets us execute SQL commands
    cursor = conn.cursor()
    
    # SQL CREATE TABLE statement - defines the schema
    # IF NOT EXISTS prevents errors if table already exists
    # Each column has a name and data type (INTEGER, TEXT)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tunes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_number INTEGER,
            file_name TEXT,
            reference_number TEXT,
            title TEXT,
            meter TEXT,
            key_signature TEXT,
            raw_abc TEXT
        )
    """)
    
    # commit() saves changes to disk
    conn.commit()
    # Always close connections when done
    conn.close()


def save_tune(tune):
    """Insert one tune record into the database."""
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # SQL INSERT statement - adds a new row to the table
    # ? are placeholders - prevents SQL injection attacks
    # Values get safely substituted from the tuple below
    cursor.execute("""
        INSERT INTO tunes (book_number, file_name, reference_number, 
                          title, meter, key_signature, raw_abc)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        # .get() safely retrieves values from dictionary
        # Second parameter is default value if key doesn't exist
        tune.get("book_number"),
        tune.get("file_name", ""),
        tune.get("reference_number", ""),
        tune.get("title", "Unknown"),
        tune.get("meter", ""),
        tune.get("key_signature", ""),
        tune.get("raw_abc", "")
    ))
    
    conn.commit()
    conn.close()


def load_all_data():
    """
    Main ETL (Extract-Transform-Load) function.
    Orchestrates the entire data loading pipeline.
    """
    # First ensure the database table exists
    create_database()
    total = 0
    
    print("Loading ABC files...")
    
    # This demonstrates the complete workflow:
    # 1. Find files (extraction)
    # 2. Parse files (transformation)
    # 3. Save to database (loading)
    for book_num, file_name, file_path in find_abc_files():
        print(f"Reading book {book_num}: {file_name}...")
        
        # Parse this ABC file to get structured tune data
        tunes = read_abc_file(file_path, book_num, file_name)
        
        # Insert each tune into the database
        for tune in tunes:
            save_tune(tune)
        
        total += len(tunes)
        print(f"  Saved {len(tunes)} tunes")
    
    print(f"\nDone! Loaded {total} tunes.")
    return total


def load_data():
    """
    Load all tunes from database into a pandas DataFrame.
    This enables easy data analysis and filtering.
    """
    conn = sqlite3.connect(database_file)
    
    # pandas can directly read SQL query results into a DataFrame
    # DataFrame is like a spreadsheet - rows and columns of data
    # This makes filtering, sorting, and analyzing much easier than raw SQL
    data = pd.read_sql("SELECT * FROM tunes", conn)
    
    conn.close()
    return data


# STEP 4: DATA ANALYSIS FUNCTIONS
# These demonstrate pandas DataFrame operations for filtering and analysis

def search_by_title(data, search_word):
    """
    Search for tunes with a word in the title (case-insensitive).
    Demonstrates string matching in pandas.
    """
    # .str.contains() searches within text columns
    # case=False makes it case-insensitive ("JIGS" matches "jigs")
    # na=False handles missing values gracefully
    # Returns a filtered DataFrame with only matching rows
    return data[data["title"].str.contains(search_word, case=False, na=False)]


def filter_by_book(data, book_num):
    """
    Filter tunes by book number.
    Demonstrates boolean indexing in pandas.
    """
    # data["book_number"] == book_num creates a True/False mask
    # data[mask] returns only rows where mask is True
    return data[data["book_number"] == book_num]


def filter_by_meter(data, meter):
    """
    Filter tunes by meter/time signature (like 4/4 or 3/4).
    Shows how to filter on any column.
    """
    return data[data["meter"] == meter]


def filter_by_key(data, key):
    """
    Filter tunes by musical key (like C major, D minor).
    Another example of pandas filtering.
    """
    return data[data["key_signature"] == key]


def count_by_book(data):
    """
    Count tunes per book - demonstrates aggregation.
    value_counts() is a pandas method for counting occurrences.
    """
    # value_counts() counts how many times each value appears
    # sort_index() sorts by book number (0, 1, 2, ...) instead of by count
    return data["book_number"].value_counts().sort_index()


def show_stats(data):
    """
    Display summary statistics about the entire collection.
    Demonstrates multiple pandas aggregation methods.
    """
    # len() gives total number of rows
    print(f"Total tunes: {len(data)}")
    
    # nunique() counts unique values (how many different book numbers)
    print(f"Number of books: {data['book_number'].nunique()}")
    
    # value_counts().head(5) shows the 5 most common values
    print(f"\nTop 5 keys:\n{data['key_signature'].value_counts().head(5)}")
    print(f"\nTop 5 meters:\n{data['meter'].value_counts().head(5)}")


# STEP 5: USER INTERFACE
# Interactive command-line menu system

def show_menu():
    """Display the menu options to the user."""
    print("\n" + "=" * 50)
    print("        ABC TUNE EXPLORER")
    print("=" * 50)
    print("1. Search by title")
    print("2. Filter by book")
    print("3. Count tunes per book")
    print("4. Filter by meter")
    print("5. Filter by key")
    print("6. Show statistics")
    print("7. View all tunes")
    print("8. Exit")
    print("-" * 50)


def run_menu():
    """
    Interactive menu loop for searching and browsing tunes.
    Demonstrates user input handling and program flow control.
    """
    # Load all data into memory for fast filtering
    print("Loading tunes...")
    data = load_data()
    print(f"Loaded {len(data)} tunes!")
    
    # Infinite loop - keeps showing menu until user chooses to exit
    while True:
        show_menu()
        choice = input("Choose (1-8): ").strip()
        
        # Handle each menu option with if/elif chain
        if choice == "1":  # Search by title
            word = input("Search for: ").strip()
            if word:
                results = search_by_title(data, word)
                print(f"\nFound {len(results)} tunes:")
                # .iterrows() loops through DataFrame rows
                # _ is convention for unused variable (the index)
                for _, tune in results.iterrows():
                    print(f"  - {tune['title']} (Book {tune['book_number']}, Key: {tune['key_signature']})")
            else:
                print("Enter a search word!")
        
        elif choice == "2":  # Filter by book
            try:
                # Convert string input to integer
                num = int(input("Book number: "))
                results = filter_by_book(data, num)
                print(f"\nFound {len(results)} tunes in book {num}:")
                for _, tune in results.iterrows():
                    print(f"  - {tune['title']} (Key: {tune['key_signature']}, Meter: {tune['meter']})")
            except:
                # Catch any errors (non-numeric input, etc.)
                print("Enter a valid number!")
        
        elif choice == "3":  # Count per book
            counts = count_by_book(data)
            print("\nTunes per book:")
            # .items() gives (key, value) pairs from the Series
            for book, count in counts.items():
                print(f"  Book {book}: {count} tunes")
        
        elif choice == "4":  # Filter by meter
            meter = input("Meter (e.g., 4/4, 3/4): ").strip()
            if meter:
                results = filter_by_meter(data, meter)
                print(f"\nFound {len(results)} tunes in {meter}:")
                for _, tune in results.iterrows():
                    print(f"  - {tune['title']} (Book {tune['book_number']})")
            else:
                print("Enter a meter!")
        
        elif choice == "5":  # Filter by key
            key = input("Key (e.g., C, G, Dm): ").strip()
            if key:
                results = filter_by_key(data, key)
                print(f"\nFound {len(results)} tunes in {key}:")
                for _, tune in results.iterrows():
                    print(f"  - {tune['title']} (Book {tune['book_number']})")
            else:
                print("Enter a key!")
        
        elif choice == "6":  # Show statistics
            show_stats(data)
        
        elif choice == "7":  # Show all tunes
            print(f"\nAll {len(data)} tunes:")
            for _, tune in data.iterrows():
                print(f"  - {tune['title']} (Book {tune['book_number']}, Key: {tune['key_signature']})")
        
        elif choice == "8":  # Exit
            print("Bye!")
            break  # Exit the while loop, returning to main menu
        
        else:
            # Handle invalid input
            print("Invalid! Choose 1-8.")
        
        # Pause before showing menu again so user can read results
        input("\nPress Enter to continue...")


# MAIN PROGRAM - Entry Point
# This is where execution begins

def main():
    """
    Main entry point - orchestrates the top-level program flow.
    Provides two main operations: loading data and searching data.
    """
    print("ABC Tune Parser")
    print("=" * 40)
    
    # Main program loop
    while True:
        # Display top-level menu
        print("\nWhat do you want to do?")
        print("1. Load ABC files into database (do this first!)")
        print("2. Search and browse tunes")
        print("3. Quit")
        
        choice = input("Choose (1-3): ").strip()
        
        if choice == "1":
            # Option 1: Run the ETL pipeline
            # This finds, parses, and loads all ABC files into the database
            print("\nLoading files...")
            total = load_all_data()
            print(f"Done! Loaded {total} tunes.")
        
        elif choice == "2":
            # Option 2: Open the search/browse interface
            # This loads data from the database and provides filtering options
            print("\nOpening search menu...")
            run_menu()
        
        elif choice == "3":
            # Option 3: Exit the program
            print("Bye!")
            break  # Exit the while loop, terminating the program
        
        else:
            # Handle invalid input
            print("Invalid! Choose 1-3.")


# Python idiom: only run main() if this file is executed directly
# If this file is imported as a module, main() won't run automatically
# __name__ == "__main__" is True when running the file directly
# __name__ == "assignment" (or module name) when imported
if __name__ == "__main__":
    main()
