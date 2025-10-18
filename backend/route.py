from flask import Blueprint, jsonify, request
import sys
import os
from pathlib import Path

# Add the backend directory to the path to import database_helper
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database.database_helper import get_db

api = Blueprint('api', __name__)

# Initialize database
try:
    db = get_db()
except FileNotFoundError:
    print("⚠️  Database not found. Please run csv_to_sqlite.py first.")
    db = None

@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    if db is None:
        return jsonify({
            'status': 'error',
            'message': 'Database not available. Please run csv_to_sqlite.py first.'
        }), 500

    try:
        stats = db.get_table_stats()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database error: {str(e)}'
        }), 500

# Courses endpoints
@api.route('/courses', methods=['GET'])
def get_courses():
    """Get all courses or filter by parameters."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        course_type = request.args.get('type')
        semester = request.args.get('semester')
        specialization = request.args.get('specialization')
        search = request.args.get('search')

        if search:
            courses = db.search_courses(search)
        elif course_type:
            courses = db.get_courses_by_type(course_type)
        elif semester:
            courses = db.get_courses_by_semester(int(semester))
        elif specialization:
            courses = db.get_courses_by_specialization(specialization)
        else:
            courses = db.get_all_courses()

        return jsonify({
            'success': True,
            'data': courses,
            'count': len(courses)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/courses/<course_id>', methods=['GET'])
def get_course(course_id):
    """Get a specific course by ID."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        course = db.get_course_by_id(course_id)
        if course:
            return jsonify({
                'success': True,
                'data': course
            })
        else:
            return jsonify({'error': 'Course not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Instructors endpoints
@api.route('/instructors', methods=['GET'])
def get_instructors():
    """Get all instructors or filter by role."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        role = request.args.get('role')
        course_id = request.args.get('course')

        if course_id:
            instructors = db.get_instructors_for_course(course_id)
        elif role:
            instructors = db.get_instructors_by_role(role)
        else:
            instructors = db.get_all_instructors()

        return jsonify({
            'success': True,
            'data': instructors,
            'count': len(instructors)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/instructors/<instructor_name>', methods=['GET'])
def get_instructor(instructor_name):
    """Get a specific instructor by name."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        instructor = db.get_instructor_by_name(instructor_name)
        if instructor:
            return jsonify({
                'success': True,
                'data': instructor
            })
        else:
            return jsonify({'error': 'Instructor not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rooms endpoints
@api.route('/rooms', methods=['GET'])
def get_rooms():
    """Get all rooms or filter by parameters."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        room_type = request.args.get('type')
        min_capacity = request.args.get('min_capacity')
        lab_type = request.args.get('lab_type')

        if lab_type:
            rooms = db.get_lab_rooms_by_type(lab_type)
        elif min_capacity:
            rooms = db.get_rooms_by_capacity(int(min_capacity))
        elif room_type:
            rooms = db.get_rooms_by_type(room_type)
        else:
            rooms = db.get_all_rooms()

        return jsonify({
            'success': True,
            'data': rooms,
            'count': len(rooms)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Timeslots endpoints
@api.route('/timeslots', methods=['GET'])
def get_timeslots():
    """Get all timeslots or filter by day."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        day = request.args.get('day')

        if day:
            timeslots = db.get_timeslots_by_day(day)
        else:
            timeslots = db.get_all_timeslots()

        return jsonify({
            'success': True,
            'data': timeslots,
            'count': len(timeslots)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Complex queries
@api.route('/courses-with-instructors', methods=['GET'])
def get_courses_with_instructors():
    """Get courses with their qualified instructors."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        data = db.get_courses_with_instructors()
        return jsonify({
            'success': True,
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Statistics endpoint
@api.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics."""
    if db is None:
        return jsonify({'error': 'Database not available'}), 500

    try:
        stats = db.get_table_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

