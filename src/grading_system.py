"""
Grading System Module
Maps marks to grade points based on standard grading scales.
"""

class GradingSystem:
    """
    Handles grade point assignment based on marks.
    Uses 10.0 scale grading system.
    """
    
    # Grade mapping: marks range -> (grade, grade_point)
    GRADE_MAPPING_10_SCALE = {
        (90, 100): ("O", 10.0),
        (80, 89): ("A+", 9.0),
        (70, 79): ("A", 8.0),
        (60, 69): ("B+", 7.0),
        (50, 59): ("B", 6.0),
        (40, 49): ("C", 5.0),
        (0, 39): ("F", 0.0),
    }
    
    def __init__(self):
        """
        Initialize grading system with 10.0 scale.
        """
        self.scale = "10.0"
        self.grade_mapping = self.GRADE_MAPPING_10_SCALE
    
    def get_grade_point(self, marks):
        """
        Get grade point for given marks.
        
        Args:
            marks: Student's marks (0-100)
            
        Returns:
            Tuple of (grade, grade_point)
        """
        if not isinstance(marks, (int, float)) or marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100")
        
        marks = float(marks)
        
        for (min_marks, max_marks), (grade, points) in self.grade_mapping.items():
            if min_marks <= marks <= max_marks:
                return grade, points
        
        raise ValueError(f"Unable to determine grade for marks: {marks}")
    
    def get_grade(self, marks):
        """Get only the grade letter for given marks."""
        grade, _ = self.get_grade_point(marks)
        return grade
    
    def get_grade_points(self, marks):
        """Get only the grade points for given marks."""
        _, points = self.get_grade_point(marks)
        return points
