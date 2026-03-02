"""
Flask Web Application for CGPA Calculator
"""

import sys
import os
from flask import Flask, render_template, request, jsonify

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from cgpa_calculator import CGPACalculator, GradingSystem

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')


@app.route('/api/calculate', methods=['POST'])
def calculate_cgpa():
    """
    API endpoint to calculate CGPA.
    
    Expected JSON format:
    {
        "grading_scale": "4.0" or "10.0",
        "subjects": [
            {"name": "Subject1", "marks": 85, "credits": 3},
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'subjects' not in data:
            return jsonify({"error": "Invalid request format"}), 400
        
        subjects_list = data.get('subjects', [])
        
        if not subjects_list:
            return jsonify({"error": "At least one subject is required"}), 400
        
        # Create calculator with 10.0 scale
        grading_system = GradingSystem()
        calculator = CGPACalculator(grading_system)
        
        # Add subjects
        for subject in subjects_list:
            try:
                calculator.add_subject(
                    subject.get('name', 'Unnamed'),
                    float(subject.get('marks', 0)),
                    float(subject.get('credits', 0))
                )
            except ValueError as e:
                return jsonify({"error": f"Invalid subject data: {str(e)}"}), 400
        
        # Get summary
        summary = calculator.get_summary()
        
        return jsonify(summary), 200
    
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


@app.route('/api/grade-info')
def grade_info():
    """Get grade mapping information."""
    try:
        # Always use 10.0 scale
        grading_system = GradingSystem()
        
        grade_info_list = []
        for (min_marks, max_marks), (grade, points) in grading_system.grade_mapping.items():
            grade_info_list.append({
                "range": f"{min_marks}-{max_marks}",
                "grade": grade,
                "points": points
            })
        
        # Sort by marks range
        grade_info_list.sort(key=lambda x: int(x['range'].split('-')[0]), reverse=True)
        
        return jsonify({
            "scale": "10.0",
            "grades": grade_info_list
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
