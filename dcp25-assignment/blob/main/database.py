import os 
import sqlite3
from typing import List, Dict
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ABC_ROOT points to the abc_books folder
ABC_ROOT = os.path.join(BASE_DIR, "abc_books")

# DB_PATH points to tunes.db (already provided in the assignment)
DB_PATH = os.path.join(BASE_DIR, "tunes.db")

#--------------STEP 1: FINDING ALL ABC FILES
def find_abc_files(root_dir: str) -> List[tuple]:
    """
    Walk through abc_books folder.
    Return a list of (book_name, full_path) for each .abc file.
    book_name will be the folder name, e.g. "1", "2", ...
    """
    abc_files = []
    for item in os.listdir(root_dir):
        book_path = os.path.join(root_dir, item)
        if os.path.isdir(book_path):
            # Treat folder name as book name
            book_name = item
            for filename in os.listdir(book_path):
                if filename.lower().endswith(".abc"):
                    full_path = os.path.join(book_path, filename)
                    abc_files.append((book_name, full_path))
    return abc_files