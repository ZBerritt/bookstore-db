#!/usr/bin/env python3
"""
Database Reset Script for MySQL on Windows
------------------------------------------
This script connects to MySQL, drops the 'bookstore' database if it exists,
recreates it, and runs the SQL files to set up schema and sample data.

Usage: python ./scripts/setup.py

SQL files (setup.sql and sample-data.sql) should be in the same 'scripts' directory.
"""

import os
import sys
import mysql.connector
from mysql.connector import Error
import argparse
from dotenv import load_dotenv

def read_sql_file(file_path):
    """Read SQL commands from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the whole file and split on semicolons (;)
            sql_commands = file.read().split(';')
            # Remove empty commands and strip whitespace
            sql_commands = [cmd.strip() for cmd in sql_commands if cmd.strip()]
            return sql_commands
    except FileNotFoundError:
        print(f"Error: SQL file '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading SQL file: {e}")
        sys.exit(1)

def execute_sql_commands(connection, commands):
    """Execute a list of SQL commands"""
    cursor = connection.cursor()
    for command in commands:
        try:
            if command:  # Skip empty commands
                cursor.execute(command)
                print(f"Successfully executed: {command[:60]}{'...' if len(command) > 60 else ''}")
        except Error as e:
            print(f"Error executing SQL command: {e}")
            print(f"Failed command: {command}")
    cursor.close()

def get_connection(database=None):
    """Connect to MySQL using environment variables"""
    try:
        return mysql.connector.connect(
            host='localhost',
            user=os.environ["DATABASE_USER"],
            password=os.environ["DATABASE_PASSWORD"],
            port='3306',
            database=database
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        sys.exit(1)

def reset_database(setup_file, sample_data_file=None):
    """Reset the bookstore database using the provided SQL files"""
    database_name = 'bookstore'
    
    try:
        # First connect without specifying a database
        connection = get_connection()
        
        if connection.is_connected():
            print(f"Connected to MySQL server on localhost")
            
            cursor = connection.cursor()
            
            # Drop the database if it exists and create it fresh
            print(f"Dropping database '{database_name}' if it exists...")
            cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
            
            print(f"Creating database '{database_name}'...")
            cursor.execute(f"CREATE DATABASE {database_name}")
            
            # Close this cursor and connection
            cursor.close()
            connection.close()
            
            # Reconnect to the newly created database
            connection = get_connection(database_name)
            print(f"Connected to database '{database_name}'")
            
            # Apply schema from setup.sql
            print(f"Applying schema from {setup_file}...")
            schema_commands = read_sql_file(setup_file)
            execute_sql_commands(connection, schema_commands)
            
            # Apply sample data if provided
            if sample_data_file:
                print(f"Loading sample data from {sample_data_file}...")
                data_commands = read_sql_file(sample_data_file)
                execute_sql_commands(connection, data_commands)
            
            connection.commit()
            print("Database reset complete!")
            
    except Error as e:
        print(f"Error with MySQL operation: {e}")
        sys.exit(1)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed.")

def main():
    """Main function to run the script"""
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if required environment variables are set
    if "DATABASE_USER" not in os.environ:
        os.environ["DATABASE_USER"] = input("Database Username: ")
        
    if "DATABASE_PASSWORD" not in os.environ:
        os.environ["DATABASE_PASSWORD"] = input("Database Password: ")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    setup_file = os.path.join(script_dir, 'setup.sql')
    sample_data_file = os.path.join(script_dir, 'sample-data.sql')
    
    # Check if setup.sql exists
    if not os.path.exists(setup_file):
        print(f"Error: Setup SQL file '{setup_file}' not found.")
        sys.exit(1)
    
    # Check if sample-data.sql exists
    if not os.path.exists(sample_data_file):
        print(f"Warning: Sample data SQL file '{sample_data_file}' not found. Proceeding without sample data.")
        sample_data_file = None
    
    # Reset the database
    reset_database(setup_file, sample_data_file)

if __name__ == "__main__":
    main()