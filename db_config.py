# db_config.py
# Database connection configuration for Estate X

import mysql.connector

import os

def get_db_connection():
    """Returns a new MySQL database connection."""
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),         
        password=os.getenv("DB_PASSWORD", "system"), 
        database=os.getenv("DB_NAME", "estate_x")
    )
    return connection
