import os #for navigating directories & finding files 
import sqlite3 #for creating and querying the SQLite database 
import pandas as pd #for data analysis & filtering with DF


"""Configuration Section"""

# finds the folder where the current python file lives & stores that folder path in the variable this_file_location
# os.path.abspath(__file__) - turns it into an absolute path (a full path from the drive root, like C:\... on Windows
# os.path.dirname  removes the filename part and leaves only the directory path that contains the file.
this_file_location: str = os.path.dirname(os.path.abspath(__file__))

# removes the last part of a path - naviagtes up 3 levels to reach the project root
project_folder: str = os.path.dirname(os.path.dirname(os.path.dirname(this_file_location)))


# joins the folder project_folder with a subfolder called "abc_books"
# os.path.join - automatically uses the right kind of slash depending on your operating system:
abc_folder: str = os.path.join(project_folder, "abc_books")


# combines the folder path with tunes.db (name of the database file)
database_file: str = os.path.join(this_file_location, "tunes.db")

"""
this_file_location = "C:/Users/nada/project/src/scripts"
database_file = "C:/Users/nada/project/tunes.db"

"""


"""STEP 1: FINDING ABC FILES"""

def find_abc_files():

    #initializes an empty list - we'll accumulate results here 
    files_found = []


    # os.listdir(abc_folder) looks inside the folder abc_folder & returns a list of names of everything in that folder 
    # the for loop loops thru each name returned from os.listdir(abc_folder)
    # for each loop, the folder_name contains one item name
    for folder_name in os.listdir(abc_folder):

        # combines the base folder abc_folder with the item name stored in folder_name to make a full path 
        folder_path = os.path.join(abc_folder, folder_name)


        # os.path.isdir(folder_path) - checks if folder_path is actually a directory and not a file
        # folder_name.isdigit() - checks if folder name is made up of only digits e.g. "1"
        if os.path.isdir(folder_path) and folder_name.isdigit():

            #converts "1" into an integer 
            book_num = int(folder_name)


            # os.listdir(folder_path) - returns a list of names of everything inside that folder 
            # for file_name - loops thru each item - each loop file_name is something like tune1.abc
            for file_name in os.listdir(folder_path):
                
                #lowercase search (converts from capital to lower) checks if filename ends with .abc
                if file_name.lower().endswith(".abc"):

                    #combines folder path and filename into a full path
                    file_path = os.path.join(folder_path, file_name)

                    # stores the info in a list as a tuple
                    # item being added is a tuple
                    files_found.append((book_num, file_name,file_path))


    return files_found #gives back full list of all .abc files found in all numbered folders

"""book_num → the book number (integer, e.g. 1)

file_name → the file name only (e.g. "tune1.abc")

file_path → the full path to that file (e.g. "/.../1/tune1.abc")"""


"""STEP 2: PARSE ABC FILES"""

def read_abc_file(file_path, book_num, file_name):

    #list will hold tunes found in this file
    all_tunes = []

    # dictionary to store tune metadata - dict stores key value pairs
    current_tune = {}

    # list to accumulate all lines of the tune
    current_tune_line = []


    # try block tells python to run this block of code and if error happens skip to except block
    # this handles any errors that occur at runtime e.g. no permission to open file or wrong encoding
    try:
        #tries to open the file located at file_path in read mode
        # with...as f: - ensures the file opens successfully & file automatically closes after block ends
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines() #reads entire file into a list of strings
    
    #opens with different encoding if error occurs
    except:
        with open(file_path, "r", encoding="latin-1") as f:
            lines = f.readlines()


    for line in lines:
        line = line.strip() #remove leading/trailing whitespace

        if not line: #skips blank lines
            continue 

        #checks if current line starts with x and if we already have a tune 
        if line.startswith("X:") and current_tune:

            #combines the list of lines into one single string, with each line seperated by a newline
            current_tune["raw_abc"] = "\n".join(current_tune_line)

            #adds current tune (dict) to the list of all the tunes we've had so far
            all_tunes.append(current_tune)

            #reset variables for the next tune
            current_tune = {}
            current_tune_line = []


        if line.startswith("X:"):
            current_tune["reference_number"] = line[2:].strip() #slices the first 2 characters leaving just the number
            current_tune["book_number"] = book_num #stores which book number the tune came from
            current_tune["file_name"] = file_name #stores the file name the tune comes from
        elif line.startswith("T:") and "title" not in current_tune:
            # Only take the first title if there are multiple T: lines
            current_tune["title"] = line[2:].strip()
        elif line.startswith("M:"):
            current_tune["meter"] = line[2:].strip()
        elif line.startswith("K:"):
            current_tune["key_signature"] = line[2:].strip()


        current_tune_line.append(line) #adds the line to the list that stores all the lines of the current tune

    #checks if current_tune exists and is not empty
    if current_tune:
        current_tune["raw_abc"]  = "\n".join(current_tune_line)
        all_tunes.append(current_tune)

    return all_tunes


"""STEP 3: DATABASE OPERATIONS"""

def create_database():

    conn = sqlite3.connect(database_file) #connects to database

    cursor = conn.cursor() #enables u to execute SQL commands in the database

    #runs sql commands in sqlite
    #only create table if it doesnt exist
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

    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    
    # '?' placeholder for a value, the code will provide the values separately
    cursor.execute("""
        INSERT INTO tunes (book_number, file_name, reference_number, 
                          title, meter, key_signature, raw_abc)
        VALUES (?, ?, ?, ?, ?, ?, ?) 
    """, (
        
        #retrieves values of the keys (book_number, file_name etc..)
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
    
    create_database()

    #Counter for the total number of tunes loaded across all files.
    total = 0
    
    print("Loading ABC files...")
    
    
    for book_num, file_name, file_path in find_abc_files():
        print(f"Reading book {book_num}: {file_name}...")
        
        # Parse this ABC file to get structured tune data, by returning a list of dictionaries
        tunes = read_abc_file(file_path, book_num, file_name)
        
        # Insert each tune into the database
        for tune in tunes:
            save_tune(tune) #for each tune, it calls this function and inserts the tune into the database
        
        total += len(tunes) #stores the number of tunes
        print(f"  Saved {len(tunes)} tunes")
    
    print(f"\nDone! Loaded {total} tunes.")
    return total


def load_data():
    
    #opens a connection to the sqlite database file stored in database_file
    #allows u to intract with the database
    conn = sqlite3.connect(database_file)
    
    # runs the query on the database connection & converts into a df
    # pandas can directly read SQL query results into a DataFrame
    data = pd.read_sql("SELECT * FROM tunes", conn)
    
    conn.close()
    return data
    



"""STEP 4: DATA ANALYSIS FUNCTIONS"""

def search_by_title(data, search_word):
    """
    Search for tunes with a word in the title (case-insensitive).
    Demonstrates string matching in pandas.
    """
    # .str.contains() checks if each title contains the word you are searching for.
    # case=False makes it case-insensitive ("JIGS" matches "jigs")
    # na=False handles missing values gracefully - if title is missing, it treats it as error instead of throwing an error
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
    Count tunes per book 
    value_counts() is a pandas method for counting occurrences.
    """
    # value_counts() counts how many times each value appears
    # sort_index() sorts in order by index instead of by count
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




"""STEP 5: USER INTERFACE"""

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
    """
    # Loads dataframe stored in 'data'
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
                #searches in title column & Finds rows where the title contains the word the user typed
                #Returns a new DataFrame with only the matching rows
                results = search_by_title(data, word)
                #prints how many matching rows were found
                print(f"\nFound {len(results)} tunes:")
                # .iterrows() loops through DataFrame rows - returns index and row data as a series
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

            # loops over each key value pair in the dict
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

        
        elif choice == "8":  
            print("Bye!")
            break  # Exit the while loop, returning to main menu

        
        else:
            # Handle invalid input
            print("Invalid! Choose 1-8.")
        
        # Pause before showing menu again so user can read results
        input("\nPress Enter to continue...")




"""MAIN PROGRAM - ENTRY POINT"""
def main():
    
    print("ABC Tune Parser")
    print("=" * 40)
    
    # Main program loop (doesn't end on it's own)
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

    
if __name__ == "__main__":
    main()



