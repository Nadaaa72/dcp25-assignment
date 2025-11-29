# Starter code for Data Centric Programming Assignment 2025

# os is a module that lets us access the file system

import os 
import sqlite3
from typing import List, Dict
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt 
# sqlite for connecting to sqlite databases

# BASE_DIR is the folder where app.py lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ABC_ROOT points to the abc_books folder
ABC_ROOT = os.path.join(BASE_DIR, "abc_books")

# DB_PATH points to tunes.db (already provided in the assignment)
DB_PATH = os.path.join(BASE_DIR, "tunes.db")


# An example of how to create a table, insert data
# and run a select query
def do_databasse_stuff():

    conn = sqlite3.connect('tunes.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, age INTEGER)')

    # Insert data
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', ('John', 30))

    # Save changes
    conn.commit()

    cursor.execute('SELECT * FROM users')

    # Get all results
    results = cursor.fetchall()

    # Print results
    for row in results:
        print(row)

    # Close
    conn.close()

#hello
books_dir = "abc_books"

def process_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    # list comprehension to strip the \n's
    lines = [line.strip() for line in lines]

    # just print the files for now
    for line in lines:
        # print(line)
        pass


# do_databasse_stuff()

# Iterate over directories in abc_books
for item in os.listdir(books_dir):
    # item is the dir name, this makes it into a path
    item_path = os.path.join(books_dir, item)
    
    # Check if it's a directory and has a numeric name
    if os.path.isdir(item_path) and item.isdigit():
        print(f"Found numbered directory: {item}")
        
        # Iterate over files in the numbered directory
        for file in os.listdir(item_path):
            # Check if file has .abc extension
            if file.endswith('.abc'):
                file_path = os.path.join(item_path, file)
                print(f"  Found abc file: {file}")
                process_file(file_path)


def parse_abc_file(file_path: str, book_number: int, file_name: str) -> List[Dict]:
    """Parse one ABC file and extract all tunes into dictionaries"""
    tunes = []
    current_tune = {}
    tune_lines = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as f:
            lines = [line.strip() for line in f.readlines()]
    
    for line in lines:
        if not line:  # Skip empty lines
            continue
            
        # If we find a new tune (X: field) and we have a current tune, save it
        if line.startswith('X:') and current_tune:
            # Save the previous tune
            current_tune['raw_abc'] = '\n'.join(tune_lines)
            tunes.append(current_tune)
            # Reset for next tune
            current_tune = {}
            tune_lines = []
        
        # Parse header fields
        if line.startswith('X:'):
            current_tune['reference_number'] = line[2:].strip()
            current_tune['book_number'] = book_number
            current_tune['file_name'] = file_name
        elif line.startswith('T:') and 'title' not in current_tune:
            # Use first T: field as main title
            current_tune['title'] = line[2:].strip()
        elif line.startswith('M:'):
            current_tune['meter'] = line[2:].strip()
        elif line.startswith('K:'):
            current_tune['key_signature'] = line[2:].strip()
        
        # Add line to current tune's raw ABC
        tune_lines.append(line)
    
    # Don't forget the last tune in the file
    if current_tune:
        current_tune['raw_abc'] = '\n'.join(tune_lines)
        tunes.append(current_tune)
    
    return tunes

def save_tune_to_database(tune_data: Dict):
    """Save one tune dictionary to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tunes (book_number, file_name, reference_number, title, meter, key_signature, raw_abc)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        tune_data.get('book_number'),
        tune_data.get('file_name', ''),
        tune_data.get('reference_number', ''),
        tune_data.get('title', 'Unknown Title'),
        tune_data.get('meter', ''),
        tune_data.get('key_signature', ''),
        tune_data.get('raw_abc', '')
    ))
    
    conn.commit()
    conn.close()


def load_all_abc_data():
    """Main function to find and parse all ABC files into the database"""
    setup_database()
    
    books_dir = "abc_books"
    total_tunes = 0
    
    print("Starting ABC file processing...")
    
    # Iterate over directories in abc_books
    for item in os.listdir(books_dir):
        # item is the dir name, this makes it into a path
        item_path = os.path.join(books_dir, item)
        
        # Check if it's a directory and has a numeric name
        if os.path.isdir(item_path) and item.isdigit():
            book_number = int(item)
            print(f"Processing book {book_number}...")
            
            # Iterate over files in the numbered directory
            for file in os.listdir(item_path):
                # Check if file has .abc extension
                if file.endswith('.abc'):
                    file_path = os.path.join(item_path, file)
                    print(f"  Parsing: {file}")
                    
                    # Parse the file
                    tunes = parse_abc_file(file_path, book_number, file)
                    
                    # Save each tune to database
                    for tune in tunes:
                        save_tune_to_database(tune)
                    
                    total_tunes += len(tunes)
                    print(f"    Found {len(tunes)} tunes")
    
    print(f"\nCompleted! Processed {total_tunes} total tunes.")
    return total_tunes

def load_tunes_from_database() -> pd.DataFrame:
    """Load all tunes from SQLite into DataFrame"""
    conn = sqlite3.connect(DB_PATH)
    
    query = "SELECT * FROM tunes"
    df = pd.read_sql(query, conn)
    
    conn.close()
    return df

def get_tunes_by_book(df: pd.DataFrame, book_number: int) -> pd.DataFrame:
    """Get all tunes from a specific book"""
    return df[df['book_number'] == book_number]

def get_tunes_by_meter(df: pd.DataFrame, meter: str) -> pd.DataFrame:
    """Get all tunes with specific meter"""
    return df[df['meter'] == meter]

def search_tunes(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search tunes by title (case insensitive)"""
    return df[df['title'].str.contains(search_term, case=False, na=False)]

def count_tunes_by_book(df: pd.DataFrame) -> pd.Series:
    """Count how many tunes are in each book"""
    return df['book_number'].value_counts().sort_index()

def get_tunes_by_key(df: pd.DataFrame, key_sig: str) -> pd.DataFrame:
    """Get all tunes in a specific key"""
    return df[df['key_signature'] == key_sig]

def show_tune_statistics(df: pd.DataFrame):
    """Display basic statistics about the tunes"""
    print(f"Total number of tunes: {len(df)}")
    print(f"Number of books: {df['book_number'].nunique()}")
    print(f"Most common keys: {df['key_signature'].value_counts().head(5)}")
    print(f"Most common meters: {df['meter'].value_counts().head(5)}")


def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("        ABC TUNE DATABASE EXPLORER")
    print("="*50)
    print("1. Search tunes by title")
    print("2. Show tunes by book number") 
    print("3. Show tune counts by book")
    print("4. Show tunes by meter")
    print("5. Show tunes by key")
    print("6. Show tune statistics")
    print("7. View all tunes")
    print("8. Exit")
    print("-"*50)

def run_user_interface():
    """Main user interface loop"""
    print("Loading data from database...")
    df = load_tunes_from_database()
    print(f"Loaded {len(df)} tunes from database!")
    
    while True:
        show_menu()
        choice = input("Please enter your choice (1-8): ").strip()
        
        if choice == '1':
            search_term = input("Enter title to search for: ").strip()
            if search_term:
                results = search_tunes(df, search_term)
                print(f"\nFound {len(results)} tunes:")
                for _, tune in results.iterrows():
                    print(f"  - '{tune['title']}' (Book {tune['book_number']}, Key: {tune['key_signature']})")
            else:
                print("Please enter a search term!")
                
        elif choice == '2':
            try:
                book_num = int(input("Enter book number: "))
                results = get_tunes_by_book(df, book_num)
                print(f"\nFound {len(results)} tunes in book {book_num}:")
                for _, tune in results.iterrows():
                    print(f"  - '{tune['title']}' (Key: {tune['key_signature']}, Meter: {tune['meter']})")
            except ValueError:
                print("Please enter a valid number!")
                
        elif choice == '3':
            counts = count_tunes_by_book(df)
            print("\nTune counts by book:")
            for book_num, count in counts.items():
                print(f"  Book {book_num}: {count} tunes")
                
        elif choice == '4':
            meter = input("Enter meter to search for (e.g., 4/4, 3/4): ").strip()
            if meter:
                results = get_tunes_by_meter(df, meter)
                print(f"\nFound {len(results)} tunes in {meter} meter:")
                for _, tune in results.iterrows():
                    print(f"  - '{tune['title']}' (Book {tune['book_number']})")
            else:
                print("Please enter a meter!")
                
        elif choice == '5':
            key_sig = input("Enter key to search for (e.g., C, G, Dm): ").strip()
            if key_sig:
                results = get_tunes_by_key(df, key_sig)
                print(f"\nFound {len(results)} tunes in key of {key_sig}:")
                for _, tune in results.iterrows():
                    print(f"  - '{tune['title']}' (Book {tune['book_number']})")
            else:
                print("Please enter a key!")
                
        elif choice == '6':
            show_tune_statistics(df)
            
        elif choice == '7':
            print(f"\nAll {len(df)} tunes:")
            for _, tune in df.iterrows():
                print(f"  - '{tune['title']}' (Book {tune['book_number']}, Key: {tune['key_signature']})")
                
        elif choice == '8':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please enter 1-8.")
        
        input("\nPress Enter to continue...")

def main():
    """Main program entry point"""
    print("ABC File Parser and Analysis System")
    print("="*40)
    
    while True:
        print("\nMain Options:")
        print("1. Load ABC data into database (run this first)")
        print("2. Run user interface")
        print("3. Exit")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == '1':
            print("\nLoading ABC data into database...")
            total_tunes = load_all_abc_data()
            print(f"Successfully loaded {total_tunes} tunes into database!")
            
        elif choice == '2':
            print("\nStarting user interface...")
            run_user_interface()
            
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice! Please enter 1-3.")

# Run the program
if __name__ == "__main__":
    main()
