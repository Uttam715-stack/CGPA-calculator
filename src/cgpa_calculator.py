"""
CGPA Calculator Module
Calculates CGPA based on marks, credits, and grading system.
"""

from grading_system import GradingSystem


class Subject:
    """Represents a subject/course with marks and credits."""
    
    def __init__(self, name, marks, credits, grading_system=None):
        """
        Initialize a subject.
        
        Args:
            name: Subject name
            marks: Marks obtained (0-100)
            credits: Credit hours for the subject
            grading_system: GradingSystem instance (uses 10.0 scale by default)
        """
        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100")
        if credits <= 0:
            raise ValueError("Credits must be positive")
        
        self.name = name
        self.marks = float(marks)
        self.credits = float(credits)
        self.grading_system = grading_system or GradingSystem()
        
        # Calculate grade and grade points
        self.grade, self.grade_points = self.grading_system.get_grade_point(self.marks)
    
    def get_weighted_points(self):
        """Calculate weighted grade points (grade_points * credits)."""
        return self.grade_points * self.credits
    
    def __repr__(self):
        return (f"Subject(name='{self.name}', marks={self.marks}, "
                f"credits={self.credits}, grade='{self.grade}', "
                f"grade_points={self.grade_points})")


class CGPACalculator:
    """Calculates CGPA for a student across multiple subjects."""
    
    def __init__(self, grading_system=None):
        """
        Initialize CGPA calculator.
        
        Args:
            grading_system: GradingSystem instance (uses 10.0 scale by default)
        """
        self.grading_system = grading_system or GradingSystem()
        self.subjects = []
    
    def add_subject(self, name, marks, credits):
        """
        Add a subject to the calculation.
        
        Args:
            name: Subject name
            marks: Marks obtained (0-100)
            credits: Credit hours for the subject
        """
        subject = Subject(name, marks, credits, self.grading_system)
        self.subjects.append(subject)
        return subject
    
    def add_subjects(self, subjects_list):
        """
        Add multiple subjects at once.
        
        Args:
            subjects_list: List of tuples (name, marks, credits)
        """
        for name, marks, credits in subjects_list:
            self.add_subject(name, marks, credits)
    
    def calculate_cgpa(self):
        """
        Calculate CGPA.
        
        Returns:
            CGPA value (rounded to 2 decimal places)
        """
        if not self.subjects:
            raise ValueError("No subjects added")
        
        total_weighted_points = sum(s.get_weighted_points() for s in self.subjects)
        total_credits = sum(s.credits for s in self.subjects)
        
        if total_credits == 0:
            raise ValueError("Total credits cannot be zero")
        
        cgpa = total_weighted_points / total_credits
        return round(cgpa, 2)
    
    def get_summary(self):
        """
        Get detailed summary of all subjects and CGPA.
        
        Returns:
            Dictionary with subject details and CGPA
        """
        if not self.subjects:
            return {"error": "No subjects added"}
        
        cgpa = self.calculate_cgpa()
        
        subjects_data = []
        for subject in self.subjects:
            subjects_data.append({
                "name": subject.name,
                "marks": subject.marks,
                "grade": subject.grade,
                "grade_points": subject.grade_points,
                "credits": subject.credits,
                "weighted_points": subject.get_weighted_points()
            })
        
        total_credits = sum(s.credits for s in self.subjects)
        total_weighted_points = sum(s.get_weighted_points() for s in self.subjects)
        
        return {
            "subjects": subjects_data,
            "total_credits": total_credits,
            "total_weighted_points": total_weighted_points,
            "cgpa": cgpa,
            "grading_scale": self.grading_system.scale
        }
    
    def reset(self):
        """Clear all subjects."""
        self.subjects = []
    
    def __repr__(self):
        return f"CGPACalculator(subjects={len(self.subjects)}, cgpa={self.calculate_cgpa() if self.subjects else 'N/A'})"
