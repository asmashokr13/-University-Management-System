import unittest
from university_management_last_version1 import Student

class TestStudent(unittest.TestCase):

    def setUp(self):
        self.student = Student(student_id=320240092, name="Asma", major="Computer Science", email="asma@gmail.com")

    def test_student_initialization(self):
        self.assertEqual(self.student.get_id(), 320240092)
        self.assertEqual(self.student.name, "Asma")
        self.assertEqual(self.student.email, "asma@gmail.com")

    def test_enroll_course(self):
        self.student.enroll_course("CS101", "Intro to CS")
        info = self.student.get_info()
        self.assertIn("CS101 - Intro to CS", info["Courses Enrolled"])

    def test_enroll_same_course_twice(self):
        self.student.enroll_course("CS101", "Intro to CS")
        self.student.enroll_course("CS101", "Intro to CS")
        self.assertEqual(len(self.student.get_info()["Courses Enrolled"]), 1)

    def test_drop_course(self):
        self.student.enroll_course("CS101", "Intro to CS")
        self.student.drop_course("CS101")
        self.assertNotIn("CS101 - Intro to CS", self.student.get_info()["Courses Enrolled"])

    def test_set_and_view_grade(self):
        self.student.enroll_course("CS101", "Intro to CS")
        self.student.set_grade("CS101", "A")
        course_info = self.student._courses_enrolled["CS101"]
        self.assertEqual(course_info["grade"], "A")

if __name__ == '__main__':
    unittest.main()
