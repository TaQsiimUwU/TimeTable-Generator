#!/usr/bin/env python3
"""
Database helper module for the TimeTable application.
Provides easy access to the SQLite database converted from CSV files.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional
import contextlib

class TimeTableDB:
    """Database helper class for timetable management."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database. If None, uses default location.
        """
        if db_path is None:
            db_path = Path(__file__).parent / 'timetable.db'

        self.db_path = str(db_path)
        self._check_database_exists()

    def _check_database_exists(self):
        """Check if database file exists."""
        if not Path(self.db_path).exists():
            raise FileNotFoundError(
                f"Database not found at {self.db_path}. "
                "Please run csv_to_sqlite.py first to create the database."
            )

    @contextlib.contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like row access
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results as list of dictionaries.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of dictionaries representing rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            Number of affected rows
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount

    # Courses methods
    def get_all_courses(self) -> List[Dict[str, Any]]:
        """Get all courses."""
        return self.execute_query("SELECT * FROM courses ORDER BY courseId")

    def get_courses_by_type(self, course_type: str) -> List[Dict[str, Any]]:
        """Get courses by type (Lecture, Lab, Tut)."""
        return self.execute_query(
            "SELECT * FROM courses WHERE type = ? ORDER BY courseId",
            (course_type,)
        )

    def get_courses_by_semester(self, semester: int) -> List[Dict[str, Any]]:
        """Get courses by semester."""
        return self.execute_query(
            "SELECT * FROM courses WHERE semester = ? ORDER BY courseId",
            (str(semester),)
        )

    def get_courses_by_specialization(self, specialization: str) -> List[Dict[str, Any]]:
        """Get courses by specialization."""
        return self.execute_query(
            "SELECT * FROM courses WHERE specialization = ? ORDER BY courseId",
            (specialization,)
        )

    def get_course_by_id(self, course_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific course by ID."""
        results = self.execute_query(
            "SELECT * FROM courses WHERE courseId = ?",
            (course_id,)
        )
        return results[0] if results else None

    # Instructors methods
    def get_all_instructors(self) -> List[Dict[str, Any]]:
        """Get all instructors."""
        return self.execute_query("SELECT * FROM instructors ORDER BY instructorName")

    def get_instructors_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get instructors by role (Prof, Eng)."""
        return self.execute_query(
            "SELECT * FROM instructors WHERE role = ? ORDER BY instructorName",
            (role,)
        )

    def get_instructor_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific instructor by name."""
        results = self.execute_query(
            "SELECT * FROM instructors WHERE instructorName = ?",
            (name,)
        )
        return results[0] if results else None

    def get_instructors_for_course(self, course_id: str) -> List[Dict[str, Any]]:
        """Get instructors qualified to teach a specific course."""
        query = """
        SELECT * FROM instructors
        WHERE qualifiedCourses_0_ = ?
           OR qualifiedCourses_1_ = ?
           OR qualifiedCourses_2_ = ?
           OR qualifiedCourses_3_ = ?
           OR qualifiedCourses_4_ = ?
           OR qualifiedCourses_5_ = ?
        ORDER BY instructorName
        """
        params = (course_id,) * 6
        return self.execute_query(query, params)

    # Rooms methods
    def get_all_rooms(self) -> List[Dict[str, Any]]:
        """Get all rooms."""
        return self.execute_query("SELECT * FROM rooms ORDER BY roomId")

    def get_rooms_by_type(self, room_type: str) -> List[Dict[str, Any]]:
        """Get rooms by type (Lecture, Lab)."""
        return self.execute_query(
            "SELECT * FROM rooms WHERE type = ? ORDER BY roomId",
            (room_type,)
        )

    def get_rooms_by_capacity(self, min_capacity: int) -> List[Dict[str, Any]]:
        """Get rooms with at least the specified capacity."""
        return self.execute_query(
            "SELECT * FROM rooms WHERE CAST(capacity AS INTEGER) >= ? ORDER BY CAST(capacity AS INTEGER)",
            (min_capacity,)
        )

    def get_lab_rooms_by_type(self, lab_type: str) -> List[Dict[str, Any]]:
        """Get lab rooms by lab type."""
        return self.execute_query(
            "SELECT * FROM rooms WHERE type = 'Lab' AND labType = ? ORDER BY roomId",
            (lab_type,)
        )

    # Timeslots methods
    def get_all_timeslots(self) -> List[Dict[str, Any]]:
        """Get all timeslots."""
        return self.execute_query("SELECT * FROM timeslots ORDER BY day, startTime")

    def get_timeslots_by_day(self, day: str) -> List[Dict[str, Any]]:
        """Get timeslots for a specific day."""
        return self.execute_query(
            "SELECT * FROM timeslots WHERE day = ? ORDER BY startTime",
            (day,)
        )

    def get_timeslot_by_id(self, timeslot_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific timeslot by ID."""
        results = self.execute_query(
            "SELECT * FROM timeslots WHERE _id = ?",
            (timeslot_id,)
        )
        return results[0] if results else None

    # Utility methods
    def get_table_stats(self) -> Dict[str, int]:
        """Get row counts for all tables."""
        stats = {}
        tables = ['courses', 'instructors', 'rooms', 'timeslots']

        for table in tables:
            result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
            stats[table] = result[0]['count']

        return stats

    def search_courses(self, search_term: str) -> List[Dict[str, Any]]:
        """Search courses by course ID or name."""
        query = """
        SELECT * FROM courses
        WHERE courseId LIKE ? OR courseName LIKE ?
        ORDER BY courseId
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern))

    def get_courses_with_instructors(self) -> List[Dict[str, Any]]:
        """Get courses with their qualified instructors (complex query example)."""
        query = """
        SELECT DISTINCT
            c.courseId,
            c.courseName,
            c.type,
            c.semester,
            c.specialization,
            i.instructorName,
            i.role
        FROM courses c
        LEFT JOIN instructors i ON (
            i.qualifiedCourses_0_ = c.courseId OR
            i.qualifiedCourses_1_ = c.courseId OR
            i.qualifiedCourses_2_ = c.courseId OR
            i.qualifiedCourses_3_ = c.courseId OR
            i.qualifiedCourses_4_ = c.courseId OR
            i.qualifiedCourses_5_ = c.courseId
        )
        ORDER BY c.courseId, i.instructorName
        """
        return self.execute_query(query)


# Convenience function to get database instance
def get_db(db_path: Optional[str] = None) -> TimeTableDB:
    """Get TimeTableDB instance."""
    return TimeTableDB(db_path)


if __name__ == "__main__":
    # Example usage and testing
    try:
        db = get_db()

        print("🗄️  Database Statistics:")
        stats = db.get_table_stats()
        for table, count in stats.items():
            print(f"  - {table}: {count} records")

        print("\n📚 Sample Courses:")
        courses = db.get_courses_by_type("Lecture")[:5]
        for course in courses:
            print(f"  - {course['courseId']}: {course['courseName']}")

        print("\n👨‍🏫 Sample Instructors:")
        instructors = db.get_instructors_by_role("Prof")[:5]
        for instructor in instructors:
            print(f"  - {instructor['instructorName']} ({instructor['role']})")

        print("\n🏛️ Sample Rooms:")
        rooms = db.get_rooms_by_type("Lecture")[:5]
        for room in rooms:
            print(f"  - {room['roomId']} (Capacity: {room['capacity']})")

        print("\n⏰ Sample Time Slots:")
        timeslots = db.get_timeslots_by_day("Sunday")[:5]
        for slot in timeslots:
            print(f"  - {slot['day']} {slot['startTime']} - {slot['endTime']}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
