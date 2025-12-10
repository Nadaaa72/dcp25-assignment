# Data Centric Programming Assignment 2025

- [Assignment Brief](assignment.md)

Name: Nada Abaasi

Student Number: C24317713

# Screenshots

# Description of the project
his project is a small data-centric application for exploring a collection of traditional tunes stored in ABC notation files.

The program:

- Scans a directory of ABC files organised into numbered “books”.
- Parses each file to extract tune metadata such as:
  - Reference number
  - Title
  - Book number
  - Meter (e.g. `4/4`, `3/4`)
  - Key signature (e.g. `C`, `G`, `Dm`)
- Stores the parsed data in a SQLite database.
- Loads the data into a pandas `DataFrame` for interactive searching and filtering via a command-line menu.

The focus of the assignment is on working with files, a relational database, and tabular data, and on providing a simple but usable text-based interface for exploring the tunes.


# Instructions for use

1. **Set up the environment**

   - Make sure Python is installed.
   - Install the required package `pandas` (inside the project’s virtual environment if provided):
     ```bash
     pip install pandas
     ```
   - `sqlite3` and `os` are part of the Python standard library, so no extra install is needed.

2. **Check the project structure**

   The key parts of the project are:

   - [abc_books/](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/abc_books:0:0-0:0)  
     Contains subfolders named with book numbers (e.g. `1`, `2`, `3`), each holding `.abc` tune files.
   - [dcp25-assignment/blob/main/my_dcp_assignment.py](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/dcp25-assignment/blob/main/my_dcp_assignment.py:0:0-0:0)  
     Main script for loading tunes into a database and exploring them.
   - [tunes.db](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/tunes.db:0:0-0:0)  
     SQLite database file created and used by the script.

3. **Running the program**

   From the project root:

   ```bash
   cd dcp25-assignment/blob/main
   python my_dcp_assignment.py

   you should see:
   A header: ABC Tune Parser
   - A menu with three options:
     - Load tunes from ABC files
     - Explore tunes in a DataFrame
     - Exit

4. **Typical workflow**
 1. choose option 1 to load data:
  -this scans the abc_books directory and loads all tunes into the database
  -parses all .abc files
  -stores the tunes in tunes.db

 2. After the data is loaded, choose option 2:
  -Opens an interactive menu for exploring the tunes.
    -Lets you search by title, filter by book/meter/key, and view statistics.

 3. Choose option 3 to exit the program when you are finished.


# How it works:

1. **Setting up paths**

   The script first figures out where everything is:
   - Where the script itself lives.
   - Where the project root is.
   - Where the [abc_books](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/abc_books:0:0-0:0) folder of tune files is.
   - Where the SQLite database ([tunes.db](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/tunes.db:0:0-0:0)) should be created.

2. **Finding the ABC files**

   The program walks through the [abc_books](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/abc_books:0:0-0:0) folder looking for:
   - Subfolders whose names are numbers (e.g. `1`, `2`, `3`).
   - Inside each of those, any file that ends with `.abc`.
   - It builds a list of every tune file it finds, along with which book it belongs to.

3. **Reading each ABC file**

   For each `.abc` file, the script:
   - Opens the file and reads it line by line.
   - Looks for ABC headers like `X:` (reference number), `T:` (title), `M:` (meter), and `K:` (key).
   - Collects these details for each tune, plus the full raw ABC text.
   - Returns a list of dictionaries—one dictionary per tune.

4. **Storing the data in a database**

   The program uses SQLite to keep the tunes:
   - Creates a table called `tunes` if it doesn’t already exist.
   - Inserts each tune’s details into the table.
   - When you choose “Load ABC files”, it repeats steps 2 and 3 for all files, then saves everything to [tunes.db](cci:7://file:///c:/Users/nadaa/dcp25-assignment-1/tunes.db:0:0-0:0).

5. **Loading the data for analysis**

   When you want to explore the tunes, the script:
   - Reads everything from the `tunes` table into a pandas DataFrame.
   - A DataFrame is like an in‑memory spreadsheet that makes searching and filtering easy.

6. **Searching and filtering**

   Using the DataFrame, you can:
   - Search for titles that contain a word (case‑insensitive).
   - Filter by book number, meter, or key signature.
   - Count how many tunes are in each book.
   - See quick stats like the most common keys and meters.

7. **Interactive menus**

   The program shows two menus:
   - **Top level**: Load data, explore tunes, or quit.
   - **Explore menu**: Choose how you want to search or filter the tunes.
   - It reads your choices, runs the right function, and prints the results in a tidy format.

8. **Putting it all together**

   The [main()](cci:1://file:///c:/Users/nadaa/dcp25-assignment-1/dcp25-assignment/blob/main/my_dcp_assignment.py:456:0-491:41) function ties everything together:
   - Shows the top menu.
   - Calls the right functions based on your choice.
   - Keeps looping until you choose to quit.
   - The `if __name__ == "__main__":` block makes sure the program starts here when you run the script.



# List of files in the project

| Files | Source |
|-----------|-----------|
| my_dcp_assignment.py | Self written (main assignment script) |
| abc_books | Provided ABC data files |
| tunes.db | Generated by the program at runtime |

# References
# References

* Course notes and examples from the Data Centric Programming module (lecturer-provided materials).
* DataCamp “Data Manipulation with pandas” course – for DataFrame operations and filtering techniques.
* ABC notation standard documentation – for understanding the structure and headers of ABC files.


# What I am most proud of in the assignment

# What I am most proud of in the assignment

I’m most proud of building a complete data pipeline from start to finish. At first, I wasn’t sure how to read the ABC files and turn them into something useful, but I ended up writing code that scans the entire directory, parses each file, and stores everything neatly in a database.

I’m also really happy with the interactive menu. It took some trial and error to get the input handling right, but now you can load the data once and then explore the tunes in many ways—by title, book, meter, or key—without having to reload anything each time.

Finally, I’m proud that the program feels responsive and tidy. It prints clear progress messages, handles a few edge cases, and the code is organised into small, readable functions. It feels like a proper little tool rather than just a script that runs once and stops.

# What I learned

I learned how to work with files and folders in Python, especially walking a directory tree and reading many small files. I also got much more comfortable with SQLite—creating tables, inserting data, and reading it back into a program.  

Using pandas was a big step for me. I learned how to load data from a database into a DataFrame and then filter, search, and count rows with simple commands. It showed me how useful pandas is for quick data exploration.  

On the programming side, I practiced organising code into small functions and handling user input in a loop. I also learned a bit about error handling, like what to do when a file can’t be opened or when the user types something unexpected.  

Overall, this assignment helped me see how to build a small data pipeline from raw files all the way to an interactive tool.

