import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root is three levels above this file: dcp25-assignment-1
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))

# ABC_ROOT points to the top-level abc_books folder at the project root
ABC_ROOT = os.path.join(PROJECT_ROOT, "abc_books")

# DB_PATH still points to tunes.db next to this module under blob/main
DB_PATH = os.path.join(BASE_DIR, "tunes.db")
