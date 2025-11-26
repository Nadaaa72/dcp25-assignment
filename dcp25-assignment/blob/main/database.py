import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any

def connect_to_database(host: str = 'localhost', 
                       user: str = 'root', 
                       password: str = 'password',
                       database: str = 'abc_tunes')