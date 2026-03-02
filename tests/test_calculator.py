"""
Unit tests for CGPA Calculator
"""

import sys
import os
import unittest

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from grading_system import GradingSystem
from cgpa_calculator import Subject, CGPACalculator


class TestGradingSystem(unittest.TestCase):
    """Test cases for GradingSystem class"""

    def setUp(self):
        """Set up test fixtures"""
        self.gs = GradingSystem()

    def test_grade_point_10_scale(self):
        """Test grade point assignment for 10.0 scale"""
        grade, points = self.gs.get_grade_point(95)
        self.assertEqual(grade, "O")
        self.assertEqual(points, 10.0)

        grade, points = self.gs.get_grade_point(85)
        self.assertEqual(grade, "A+")
        self.assertEqual(points, 9.0)

        grade, points = self.gs.get_grade_point(75)
        self.assertEqual(grade, "A")
        self.assertEqual(points, 8.0)

    def test_invalid_marks(self):
        """Test error handling for invalid marks"""
        with self.assertRaises(ValueError):
            self.gs.get_grade_point(-5)

        with self.assertRaises(ValueError):
            self.gs.get_grade_point(150)

    def test_get_grade(self):
        """Test get_grade method"""
        grade = self.gs.get_grade(88)
        self.assertEqual(grade, "A+")

    def test_get_grade_points(self):
        """Test get_grade_points method"""
        points = self.gs.get_grade_points(75)
        self.assertEqual(points, 8.0)


class TestSubject(unittest.TestCase):
    """Test cases for Subject class"""

    def setUp(self):
        """Set up test fixtures"""
        self.gs = GradingSystem()

    def test_subject_creation(self):
        """Test subject creation"""
        subject = Subject("Mathematics", 85, 3, self.gs)
        self.assertEqual(subject.name, "Mathematics")
        self.assertEqual(subject.marks, 85)
        self.assertEqual(subject.credits, 3)
        self.assertEqual(subject.grade, "A+")

    def test_weighted_points(self):
        """Test weighted points calculation"""
        subject = Subject("Physics", 75, 4, self.gs)
        weighted = subject.get_weighted_points()
        # 75 marks -> 8.0 grade points, 8.0 * 4 = 32.0
        self.assertAlmostEqual(weighted, 32.0, places=1)

    def test_invalid_marks(self):
        """Test error handling for invalid marks"""
        with self.assertRaises(ValueError):
            Subject("Chemistry", 150, 3, self.gs)

    def test_invalid_credits(self):
        """Test error handling for invalid credits"""
        with self.assertRaises(ValueError):
            Subject("Chemistry", 85, -2, self.gs)


class TestCGPACalculator(unittest.TestCase):
    """Test cases for CGPACalculator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.calc = CGPACalculator()

    def test_add_subject(self):
        """Test adding a subject"""
        subject = self.calc.add_subject("Math", 85, 3)
        self.assertEqual(len(self.calc.subjects), 1)
        self.assertEqual(subject.name, "Math")

    def test_add_multiple_subjects(self):
        """Test adding multiple subjects"""
        subjects_data = [
            ("Math", 85, 3),
            ("Physics", 80, 4),
            ("Chemistry", 90, 3)
        ]
        self.calc.add_subjects(subjects_data)
        self.assertEqual(len(self.calc.subjects), 3)

    def test_cgpa_calculation(self):
        """Test CGPA calculation"""
        # Add test subjects with 10.0 scale
        # Math: 85 marks -> A+ (9.0 points) * 3 credits = 27.0
        # Physics: 80 marks -> A+ (9.0 points) * 4 credits = 36.0
        # Chemistry: 90 marks -> O (10.0 points) * 3 credits = 30.0
        # Total: (27.0 + 36.0 + 30.0) / (3 + 4 + 3) = 93.0 / 10 = 9.3
        self.calc.add_subjects([
            ("Math", 85, 3),
            ("Physics", 80, 4),
            ("Chemistry", 90, 3)
        ])
        cgpa = self.calc.calculate_cgpa()
        self.assertAlmostEqual(cgpa, 9.3, places=2)

    def test_cgpa_no_subjects(self):
        """Test CGPA calculation with no subjects"""
        with self.assertRaises(ValueError):
            self.calc.calculate_cgpa()

    def test_summary(self):
        """Test summary generation"""
        self.calc.add_subjects([
            ("Math", 85, 3),
            ("Physics", 80, 4)
        ])
        summary = self.calc.get_summary()

        self.assertIn("subjects", summary)
        self.assertIn("total_credits", summary)
        self.assertIn("total_weighted_points", summary)
        self.assertIn("cgpa", summary)
        self.assertEqual(len(summary["subjects"]), 2)
        self.assertEqual(summary["total_credits"], 7)

    def test_reset(self):
        """Test reset functionality"""
        self.calc.add_subjects([
            ("Math", 85, 3),
            ("Physics", 80, 4)
        ])
        self.assertEqual(len(self.calc.subjects), 2)

        self.calc.reset()
        self.assertEqual(len(self.calc.subjects), 0)


if __name__ == '__main__':
    unittest.main()
