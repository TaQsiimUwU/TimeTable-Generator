#!/usr/bin/env python3
"""
Script to convert CSV files in the database directory to a SQLite database.
"""

import sqlite3
import csv
import os
from pathlib import Path

def create_database_from_csvs():
    """Convert all CSV files in the database directory to SQLite tables."""

    # Define paths
    database_dir = Path(__file__).parent / 'database'
    sqlite_db_path = database_dir / 'timetable.db'

    # Remove existing database if it exists
    if sqlite_db_path.exists():
        sqlite_db_path.unlink()
        print(f"Removed existing database: {sqlite_db_path}")

    # Create connection to SQLite database
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    print(f"Created SQLite database: {sqlite_db_path}")

    # Process each CSV file
    csv_files = list(database_dir.glob('*.csv'))

    for csv_file in csv_files:
        print(f"\nProcessing {csv_file.name}...")

        # Extract table name from filename
        table_name = csv_file.stem.replace('TimeTableDB.', '').replace('.', '_')

        # Read CSV file to get headers and data
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)  # Get headers
            raw_rows = list(csv_reader)     # Get all data rows

        if not raw_rows:
            print(f"  Warning: {csv_file.name} is empty, skipping...")
            continue

        # Normalize rows to have the same number of columns as headers
        rows = []
        for row in raw_rows:
            # Pad row with empty strings if it has fewer columns than headers
            while len(row) < len(headers):
                row.append('')
            # Truncate row if it has more columns than headers
            if len(row) > len(headers):
                row = row[:len(headers)]
            rows.append(row)

        # Create table schema based on headers
        # We'll use TEXT for all columns to preserve data integrity
        column_definitions = []
        for header in headers:
            # Clean column names (replace spaces and special chars with underscores)
            clean_header = header.replace(' ', '_').replace('[', '_').replace(']', '_').replace('.', '_')
            column_definitions.append(f'"{clean_header}" TEXT')

        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            {', '.join(column_definitions)}
        )
        '''

        cursor.execute(create_table_sql)
        print(f"  Created table: {table_name}")

        # Insert data
        placeholders = ', '.join(['?' for _ in headers])
        insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'

        cursor.executemany(insert_sql, rows)
        print(f"  Inserted {len(rows)} rows into {table_name}")

        # Create indexes on commonly used columns
        if table_name == 'courses':
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_courses_courseId ON "{table_name}" ("courseId")')
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_courses_type ON "{table_name}" ("type")')
            print("  Created indexes on courseId and type")
        elif table_name == 'instructors':
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_instructors_name ON "{table_name}" ("instructorName")')
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_instructors_role ON "{table_name}" ("role")')
            print("  Created indexes on instructorName and role")
        elif table_name == 'rooms':
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_rooms_roomId ON "{table_name}" ("roomId")')
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_rooms_type ON "{table_name}" ("type")')
            print("  Created indexes on roomId and type")
        elif table_name == 'timeslots':
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_timeslots_day ON "{table_name}" ("day")')
            cursor.execute(f'CREATE INDEX IF NOT EXISTS idx_timeslots_start ON "{table_name}" ("startTime")')
            print("  Created indexes on day and startTime")

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"\n✅ Successfully converted {len(csv_files)} CSV files to SQLite database!")
    print(f"Database location: {sqlite_db_path}")

    # Display database info
    print("\n📊 Database Summary:")
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\"")
        count = cursor.fetchone()[0]
        print(f"  - {table_name}: {count} records")

    conn.close()

if __name__ == "__main__":
    create_database_from_csvs()
