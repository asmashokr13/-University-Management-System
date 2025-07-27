from abc import ABC, abstractmethod
from datetime import datetime
import socket
import json

class Person(ABC):
    def __init__(self, email, name):
        self.email = email
        self.name = name

    @abstractmethod
    def get_info(self):
        pass


class Student(Person):
    def __init__(self, student_id, name, major, email):
        super().__init__(email, name)
        self._id = student_id
        self._major = major
        self._courses_enrolled = {}

    def get_id(self):
        return self._id

    def enroll_course(self, course_id, course_name):
        if course_id not in self._courses_enrolled:
            self._courses_enrolled[course_id] = {"name": course_name, "grade": None}
            print(f"{self.name} has enrolled in {course_name}")
        else:
            print(f"{self.name} is already enrolled in {course_name}")

    def drop_course(self, course_id):
        if course_id in self._courses_enrolled:
            course_name = self._courses_enrolled[course_id]["name"]  # to display
            del self._courses_enrolled[course_id]
            print(f"{self.name} has dropped {course_name}")
        else:
            print(f"{self.name} is not enrolled in course {course_id}")

    def set_grade(self, course_id, grade):
        if course_id in self._courses_enrolled:
            self._courses_enrolled[course_id]["grade"] = grade  # to update
        else:
            print(f"{self.name} is not enrolled in course {course_id}")

    def view_grades(self):
        if not self._courses_enrolled:
            print(f"{self.name} is not enrolled in any courses.")
        else:
            print(f"Grades for {self.name}:")
            for course_id, details in self._courses_enrolled.items():
                grade = details["grade"] if details["grade"] else "Not graded yet"
                print(f"  {course_id} - {details['name']}: {grade}")

    def get_info(self):
        return {
            "ID": self._id,
            "Name": self.name,
            "Major": self._major,
            "Email": self.email,
            "Courses Enrolled": [
                f"{course_id} - {info['name']}" for course_id, info in self._courses_enrolled.items()
            ]
        }


class Professor(Person):
    def __init__(self, professor_id, name, department, contact_info, email):
        super().__init__(email, name)
        self.professor_id = professor_id
        self.department = department
        self.contact_info = contact_info
        self.courses_taught = []

    def assign_grade(self, student, course_id, grade):
        if course_id in self.courses_taught and course_id in student._courses_enrolled:
            student._courses_enrolled[course_id]["grade"] = grade
            print(f"Grade {grade} assigned to {student.name} for {student._courses_enrolled[course_id]['name']}")
        else:
            print("Cannot assign grade: Course not found or student not enrolled.")

    def view_students(self, students_list):
        print(f"Students in courses taught by {self.name}:")
        found_students = False
        for student in students_list:
            for course_id in student._courses_enrolled:
                if course_id in self.courses_taught:
                    print(f"  {student.name} is enrolled in {student._courses_enrolled[course_id]['name']}")
                    found_students = True

        if not found_students:
            print("No students found in any of the professor's courses.")

    def get_info(self):
        return {
            "ID": self.professor_id,
            "Name": self.name,
            "Email": self.email,
            "Department": self.department,
            "Contact Info": self.contact_info,
            "Courses Taught": self.courses_taught
        }


class Course:
    def __init__(self, course_id, name, department, credits, professor):
        self.course_id = course_id
        self.name = name
        self.department = department
        self.credits = credits
        self.professor = professor
        self.enrolled_students = {}
        professor.courses_taught.append(self.course_id)

    def add_student(self, student):
        if student._id not in self.enrolled_students:
            self.enrolled_students[student._id] = student

    def remove_student(self, student):
        if student._id in self.enrolled_students:
            del self.enrolled_students[student._id]
            del student._courses_enrolled[self.course_id]
            print(f"{student.name} has been removed from {self.name}")
        else:
            print(f"{student.name} is not enrolled in {self.name}")

    def get_course_info(self):
        return {
            "Course ID": self.course_id,
            "Name": self.name,
            "Department": self.department,
            "Credits": self.credits,
            "Professor": self.professor.name,
            "Enrolled Students": list(self.enrolled_students.keys())
        }


class Department:
    def __init__(self, department_id, name, head_of_department):
        self.department_id = department_id
        self.name = name
        self.head_of_department = head_of_department
        self.courses_offered = []
        self.faculty_members = []

    def get_information(self):
        print(f"Department ID : {self.department_id}")
        print(f"Department Name : {self.name}")
        print(f"Head of Department : {self.head_of_department}")

    def list_courses(self, course):
        self.courses_offered.append(course)

    def list_professors(self, professor):
        self.faculty_members.append(professor)


class Admin(Person):
    def __init__(self, admin_id, name, role, contact_info, email):
        super().__init__(email, name)
        self.__admin_id = admin_id
        self.role = role
        self.contact_info = contact_info

    def get_admin_id(self):
        return self.__admin_id

    def set_admin_id(self, new_id):
        try:
            if not isinstance(new_id, int):
                raise ValueError("Admin ID must be an integer.")
            self.__admin_id = new_id
        except ValueError as e:
            print("Error:", e)

    def get_info(self):
        return {
            "Admin ID": self.__admin_id,
            "Name": self.name,
            "Role": self.role,
            "Email": self.email,
            "Contact Info": self.contact_info
        }

    def add_student(self, student_name):
        try:
            if not isinstance(student_name, str):
                raise TypeError("Student name must be a string.")
            print(f"Student '{student_name}' has been added.")
        except TypeError as e:
            print("Error:", e)

    def remove_student(self, student_name):
        try:
            if not isinstance(student_name, str):
                raise TypeError("Student name must be a string.")
            print(f"Student '{student_name}' has been removed.")
        except TypeError as e:
            print("Error:", e)

    def assign_professor(self, professor_name, course):
        try:
            if not all(isinstance(arg, str) for arg in [professor_name, course]):
                raise TypeError("Both professor name and course must be strings.")
            print(f"Professor '{professor_name}' assigned to course '{course}'.")
        except TypeError as e:
            print("Error:", e)

    def manage_course(self, *args):
        try:
            if len(args) == 2:
                course_name, action = args
                note = ""
            elif len(args) == 3:
                course_name, action, note = args
            else:
                raise ValueError("manage_course requires 2 or 3 arguments.")

            if action not in ["add", "remove", "update"]:
                raise ValueError("Invalid action. Must be 'add', 'remove', or 'update'.")

            print(f"Course '{course_name}' has been {action}ed. {note}")
        except ValueError as e:
            print("Error:", e)


class ScheduleBase(ABC):

    @abstractmethod
    def assign_schedule(self):
        pass

    @abstractmethod
    def update_schedule(self):
        pass

    @abstractmethod
    def view_schedule(self):
        pass


class Schedule(ScheduleBase):
    def __init__(self, schedule_id, course, professor, time_slot, location):
        self.__schedule_id = schedule_id
        self.__course = course
        self.__professor = professor
        self.__time_slot = time_slot
        self.__location = location

    def get_schedule_id(self):
        return self.__schedule_id

    def get_course(self):
        return self.__course

    def get_professor(self):
        return self.__professor

    def get_time_slot(self):
        return self.__time_slot

    def get_location(self):
        return self.__location

    def set_time_slot(self, time_slot):
        self.__time_slot = time_slot

    def set_location(self, location):
        self.__location = location

    def assign_schedule(self):
        print(
            f"Assigned Schedule:\nCourse: {self.__course.name}, Professor: {self.__professor.name}, Time Slot: {self.__time_slot}, Location: {self.__location}")

    def update_schedule(self, time_slot=None, location=None):
        if time_slot:
            self.__time_slot = time_slot
        if location:
            self.__location = location
        print("Schedule updated successfully.")

    def view_schedule(self):
        return (f"Schedule ID: {self.__schedule_id}, Course: {self.__course.name}, "
                f"Professor: {self.__professor.name}, Time Slot: {self.__time_slot}, "
                f"Location: {self.__location}")


class Classroom:
    def __init__(self, classroom_id, location, capacity):
        self.classroom_id = classroom_id
        self.location = location
        self.capacity = capacity
        self.schedule = []

    def check_availability(self, time_slot):
        for s in self.schedule:
            if s.get_time_slot() == time_slot:
                return False
        return True

    def allocate_class(self, schedule):
        if not self.check_availability(schedule.get_time_slot()):
            print(f"Time slot {schedule.get_time_slot()} is already taken in {self.location}.")
            return
        self.schedule.append(schedule)
        print(f"Class allocated at {self.location} for course {schedule.get_course().name}")

    def get_classroom_info(self):
        return {
            "Classroom ID": self.classroom_id,
            "Location": self.location,
            "Capacity": self.capacity,
            "Schedule": [s.view_schedule() for s in self.schedule]
        }


class Exam(ABC):
    def __init__(self, exam_id, course, date, duration):
        self.__exam_id = exam_id
        self._course = course
        self.date = date
        self.duration = duration
        self.__student_results = {}

    @abstractmethod
    def schedule_exam(self):
        pass

    @abstractmethod
    def view_exam_info(self):
        pass

    def get_exam_id(self):
        return self.__exam_id

    def set_exam_id(self, new_id):
        self.__exam_id = new_id

    def record_results(self, student_name, score=None):
        try:
            if score is None:
                print(f"No score provided for {student_name}.")
            elif not isinstance(score, (int, float)):
                raise ValueError("Score must be a number!")
            elif score < 0 or score > 100:
                raise ValueError("Score must be between 0 and 100!")
            else:
                self.__student_results[student_name] = score
                print(f"Result recorded for {student_name}: {score}")
        except ValueError as e:
            print(f"Error: {e}")

    def view_results(self):
        if self.__student_results:
            print("Student Results:")
            for student, score in self.__student_results.items():
                print(f"  - {student}: {score}")
        else:
            print("No results recorded yet.")


class FinalExam(Exam):
    def __init__(self, exam_id, course, date, duration, passing_score):
        super().__init__(exam_id, course, date, duration)
        self.passing_score = passing_score

    def schedule_exam(self):
        print(f"Final Exam {self.get_exam_id()} for course '{self._course}' is scheduled on {self.date}.")

    def view_exam_info(self):
        print(f"Final Exam ID: {self.get_exam_id()}")
        print(f"Course: {self._course}")
        print(f"Date: {self.date}")
        print(f"Duration: {self.duration} hours")
        print(f"Passing Score: {self.passing_score}")


class Library:
    def __init__(self, library_id):
        self.__library_id = library_id
        self._books = {}
        self._students_registered = {}

    def get_library_id(self):
        return self.__library_id

    def set_library_id(self, new_id):
        self.__library_id = new_id

    def add_book(self, book_title, author, category, copies=1):
        if book_title in self._books:
            self._books[book_title]["copies"] += copies
        else:
            self._books[book_title] = {
                "author": author,
                "category": category,
                "copies": copies
            }
        print(f"Added {copies} {'copy' if copies == 1 else 'copies'} of '{book_title}' to the library.")

    def register_student(self, student_id, student_name):
        if student_id not in self._students_registered:
            self._students_registered[student_id] = {
                "name": student_name,
                "borrowed_books": []
            }
            print(f"Student '{student_name}' registered in the library.")
        else:
            print(f"Student '{student_name}' is already registered.")

    def borrow_book(self, student_id, book_title):
        try:
            if student_id not in self._students_registered:
                raise ValueError(f"Student with ID '{student_id}' is not registered in the library!")
            if book_title not in self._books or self._books[book_title]["copies"] <= 0:
                raise ValueError(f"Book '{book_title}' is not available.")
            self._books[book_title]["copies"] -= 1
            self._students_registered[student_id]["borrowed_books"].append(book_title)
            print(f"Book '{book_title}' borrowed by {self._students_registered[student_id]['name']}.")
        except ValueError as e:
            print(f"Error: {e}")

    def return_book(self, student_id, book_title):
        try:
            if student_id not in self._students_registered:
                raise ValueError(f"Student with ID '{student_id}' is not registered in the library!")
            if book_title not in self._books:
                raise ValueError(f"Book '{book_title}' does not belong to this library!")
            self._books[book_title]["copies"] += 1
            if book_title in self._students_registered[student_id]["borrowed_books"]:
                self._students_registered[student_id]["borrowed_books"].remove(book_title)
                print(f"Book '{book_title}' returned by {self._students_registered[student_id]['name']}.")
            else:
                print(f"{self._students_registered[student_id]['name']} did not borrow '{book_title}'.")
        except ValueError as e:
            print(f"Error: {e}")

    def check_availability(self, book_title):
        if book_title in self._books and self._books[book_title]["copies"] > 0:
            print(f"'{book_title}' is available. Copies left: {self._books[book_title]['copies']}")
        else:
            print(f"'{book_title}' is not available.")

    def search_book(self, keyword):
        found = False
        for title, details in self._books.items():
            if keyword.lower() in title.lower() or keyword.lower() in details["author"].lower() or keyword.lower() in \
                    details["category"].lower():
                print(f"Found: '{title}' by {details['author']} ({details['category']}) - Copies: {details['copies']}")
                found = True
        if not found:
            print(f"No books found matching '{keyword}'.")


class User:
    __logged_in_user = None
    __registered_users = {}

    def __init__(self, user_id, name, role, email, password=None):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.email = email
        self.__password = password

    def login(self, password=None):

        if password is not None and self.__password is not None:
            if password != self.__password:
                print(f"Incorrect password for {self.email}")
                return False

        if User.__logged_in_user is not None:
            print(f"Another user ({User.__logged_in_user.name}) is logged in.")
            return False
        else:
            User.__logged_in_user = self
            print(f"{self.name} logged in.")
            return True

    def logout(self):
        if User.__logged_in_user == self:
            User.__logged_in_user = None
            print(f"{self.name} logged out.")
            return True
        else:
            print("You are not the logged-in user.")
            return False

    def view_dashboard(self):
        print(f"ID: {self.user_id}")
        print(f"Name: {self.name}")
        print(f"Role: {self.role}")
        print(f"Email: {self.email}")

    @classmethod
    def get_logged_in_user(cls):
        return cls.__logged_in_user

    @classmethod
    def get_user_by_email(cls, email):
        return cls.__registered_users.get(email)

    @classmethod
    def register_user(cls, user_id, name, role, email, password):
        if email in cls.__registered_users:
            print(f"Email {email} is already registered.")
            return None

        new_user = User(user_id, name, role, email, password)
        cls.__registered_users[email] = new_user
        print(f"User {name} registered successfully with email {email}.")
        return new_user


class AttendanceRecord(ABC):
    @abstractmethod
    def record_attendance(self):
        pass


class Attendance(AttendanceRecord):
    def __init__(self, student, course, date, status="Absent"):
        self.__student = student
        self.__course = course
        self.__date = None
        self.set_date(date)
        self.__status = status if status in ["Present", "Absent"] else "Absent"

    def get_student(self):
        return self.__student

    def get_course(self):
        return self.__course

    def get_date(self):
        return self.__date

    def set_date(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            self.__date = value
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

    def get_status(self):
        return self.__status

    def set_status(self, new_status):
        if new_status not in ["Present", "Absent"]:
            raise ValueError("Status must be 'Present' or 'Absent'")
        self.__status = new_status

    def record_attendance(self):
        print(f"Attendance recorded for {self.__student.name} in {self.__course.name}")

    def get_attendance_info(self):
        return {
            "Student": self.__student.name,
            "Student ID": self.__student.get_id(),
            "Course": self.__course.name,
            "Course ID": self.__course.course_id,
            "Date": self.__date,
            "Status": self.__status
        }


class AttendanceReport:
    def __init__(self):
        self.attendance_records = []

    def add_attendance(self, attendance_obj):
        if isinstance(attendance_obj, Attendance):
            self.attendance_records.append(attendance_obj)
        else:
            raise TypeError("Only Attendance objects can be added")

    def get_student_attendance(self, student):
        records = [record.get_attendance_info()
                   for record in self.attendance_records
                   if record.get_student().get_id() == student.get_id()]

        if not records:
            print(f"No attendance records found for {student.name}")
            return []

        print(f"\nAttendance Report for {student.name} (ID: {student.get_id()}):")
        for record in records:
            print(f"- Course: {record['Course']} | Date: {record['Date']} | Status: {record['Status']}")

        return records

    def get_course_attendance(self, course):
        records = [record.get_attendance_info()
                   for record in self.attendance_records
                   if record.get_course().course_id == course.course_id]

        if not records:
            print(f"No attendance records found for course {course.name}")
            return []

        print(f"\nAttendance Report for Course '{course.name}' (ID: {course.course_id}):")
        for record in records:
            print(f"- Student: {record['Student']} | Date: {record['Date']} | Status: {record['Status']}")

        return records

    def calculate_attendance_percentage(self, student, course=None):
        total_days = 0
        present_days = 0

        for record in self.attendance_records:
            if record.get_student().get_id() == student.get_id():
                if course is None or record.get_course().course_id == course.course_id:
                    total_days += 1
                    if record.get_status() == "Present":
                        present_days += 1

        if total_days == 0:
            print(f"No attendance records found for {student.name}")
            return 0

        percentage = (present_days / total_days) * 100
        course_info = f"in {course.name}" if course else "across all courses"
        print(f"{student.name} has attended {present_days} out of {total_days} days {course_info}. ({percentage:.2f}%)")

        return percentage


class AttendanceProxy:
    def __init__(self, user_role):
        self.user_role = user_role.lower()
        self.attendance_records = []

    def add_record(self, attendance_obj):
        if self.user_role not in ["admin", "professor"]:
            raise PermissionError("Unauthorized: Only admins and professors can add attendance")

        if not isinstance(attendance_obj, Attendance):
            raise TypeError("Only Attendance objects can be added")

        self.attendance_records.append(attendance_obj)
        print("Attendance record added successfully")

    def view_records(self, student=None, course=None):
        if not self.attendance_records:
            print("No attendance records available")
            return []

        filtered_records = []
        for record in self.attendance_records:
            if (student is None or record.get_student().get_id() == student.get_id()) and \
                    (course is None or record.get_course().course_id == course.course_id):
                filtered_records.append(record.get_attendance_info())

        if not filtered_records:
            print("No matching records found")
            return []

        for record in filtered_records:
            print(f"Student: {record['Student']} | Course: {record['Course']} | "
                  f"Date: {record['Date']} | Status: {record['Status']}")

        return filtered_records

    def update_status(self, student_id, date, new_status):
        if self.user_role not in ["admin", "professor"]:
            print("Unauthorized: Only admins and professors can update attendance")
            return False

        from datetime import datetime
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD")
            return False

        if new_status not in ["Present", "Absent"]:
            print("Invalid status. Must be 'Present' or 'Absent'")
            return False

        updated = False
        for record in self.attendance_records:
            if (record.get_student().get_id() == student_id and
                    record.get_date() == date):
                record.set_status(new_status)
                updated = True
                print(f"Attendance status for {record.get_student().name} updated to {new_status}")

        if not updated:
            print("No matching attendance record found")
            return False

        return True


students = []
courses = []
professors = []
departments = []
administrators = []
classrooms = []
schedules = []
exams = []
libraries = []
attendance_records = []
attendance_reports = []
attendance_proxies = []
users = []

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 3000


def handle_client(conn, addr):
    ip = addr[0]  # get the client's ip address
    print(f"[+] Connected: {ip}")

    with conn:  # automatically close the connection when done
        while True:  # keep listening to this client until they quit or disconnect
            try:
                data = conn.recv(1024)
                if not data: # the client disconnected
                    print(f"[-] Disconnected: {ip}")
                    break

                msg = data.decode().strip()
                print(f"[{ip}] -> {msg}")  # Show what the client sent


                parts = msg.split(' ', 1)
                cmd = parts[0].upper()
                args = parts[1] if len(parts) > 1 else ""
                resp = "ERROR: Unknown command"

                if cmd == "QUIT":
                    resp = "INFO: Disconnecting."
                    conn.sendall(resp.encode())
                    break

                elif cmd == "GET_STUDENT_COUNT":
                    resp = f"COUNT: {len(students)}"

                elif cmd == "ADD_STUDENT":
                    try:

                        s_id, name, major, email = args.split(',')

                        if any(s.get_id() == s_id for s in students):
                            resp = f"ERROR: Student with ID {s_id} already exists."
                        else:
                            students.append(Student(s_id, name, major, email))
                            resp = f"SUCCESS: Student {name} added."
                    except:
                        resp = "ERROR: Invalid ADD_STUDENT format. Use id,name,major,email"

                elif cmd == "GET_STUDENT_INFO":
                    s_id = args.strip()
                    student = next((s for s in students if s.get_id() == s_id), None)
                    if student:
                        # convert student info to JSON string to send
                        resp = json.dumps(student.get_info())
                    else:
                        resp = f"ERROR: Student with ID {s_id} not found."

                conn.sendall(resp.encode())
                print(f"[{ip}] <- {resp[:100]}...")

            except ConnectionResetError:
                print(f"[!] Connection reset: {ip}")
                break

            except Exception as e:
                print(f"[!] Error with {ip}: {e}")
                try:
                    conn.sendall(f"ERROR: Server error - {e}".encode())
                except:
                    pass
                break


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   #Automatically closes the socket when done
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((SERVER_HOST, SERVER_PORT))
            s.listen()
            print(f"Server listening at {SERVER_HOST}:{SERVER_PORT}")

            while True:
                conn, addr = s.accept()
                handle_client(conn, addr)

        except OSError as e:
            # If port is already in use or other socket errors
            print(f"Port error: {e}")

        except KeyboardInterrupt:
            print("\nServer interrupted.")

        finally:
            print("Server stopped.")

def main_cli():
    while True:
        print("\nUniversity Management System")
        print("1. Add Student")
        print("2. Add Professor")
        print("3. Add Course")
        print("4. Enroll Student in Course")
        print("5. Remove Student from Course")
        print("6. Show Student Courses")
        print("7. Show Course Students")
        print("8. Add Department")
        print("9. Show Department Info")
        print("10. Add Administrator")
        print("11. Show Administrator Info")
        print("12. Add Classroom")
        print("13. Create Schedule")
        print("14. Update Schedule")
        print("15. View All Schedules")
        print("16. Add Exam")
        print("17. Schedule Exam")
        print("18. Record Exam Results")
        print("19. View Exam Results")
        print("20. Add Library")
        print("21. Add Book to Library")
        print("22. Register Student to Library")
        print("23. Borrow Book from Library")
        print("24. Return Book to Library")
        print("25. Search Book in Library")
        print("26. Record Attendance")
        print("27. View Student Attendance")
        print("28. View Course Attendance")
        print("29. Calculate Attendance Percentage")
        print("30. Update Attendance Status")
        print("31. Login")
        print("32. Logout")
        print("33. View Dashboard")
        print("34. Register User")
        print("35. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter student name: ")
            student_id = input("Enter student ID: ")
            major = input("Enter student major: ")
            email = input("Enter student email: ")
            students.append(Student(student_id, name, major, email))
            print("Student added successfully!")

        elif choice == "2":
            name = input("Enter professor name: ")
            professor_id = input("Enter professor ID: ")
            department = input("Enter department: ")
            contact_info = input("Enter contact info: ")
            email = input("Enter professor email: ")
            prof = Professor(professor_id, name, department, contact_info, email)
            professors.append(prof)

            dept = next((d for d in departments if d.name == department), None)
            if dept:
                dept.list_professors(prof)

            print("Professor added successfully!")


        elif choice == "3":
            if not professors:
                print("No professors available. Add a professor first.")
                continue
            name = input("Enter course name: ")
            course_id = input("Enter course ID: ")
            department = input("Enter course department: ")
            credits = input("Enter course credits: ")
            try:
                prof_index = int(input(f"Select a professor (0-{len(professors) - 1}): "))
                if 0 <= prof_index < len(professors):
                    course = Course(course_id, name, department, credits, professors[prof_index])
                    courses.append(course)

                    dept = next((d for d in departments if d.name == department), None)
                    if dept:
                        dept.list_courses(course)

                    print("Course added successfully!")
                else:
                    print("Invalid professor index.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "4":
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            student = next((s for s in students if s._id == student_id), None)
            course = next((c for c in courses if c.course_id == course_id), None)
            if student and course:
                student.enroll_course(course.course_id, course.name)
                course.add_student(student)
            else:
                print("Invalid student ID or course ID.")

        elif choice == "5":
            student_id = input("Enter student ID: ")
            course_id = input("Enter course ID: ")
            student = next((s for s in students if s._id == student_id), None)
            course = next((c for c in courses if c.course_id == course_id), None)
            if student and course:
                course.remove_student(student)
            else:
                print("Invalid student ID or course ID.")

        elif choice == "6":
            student_id = input("Enter student ID: ")
            student = next((s for s in students if s._id == student_id), None)
            if student:
                print(student.get_info())
            else:
                print("Student not found.")

        elif choice == "7":
            course_id = input("Enter course ID: ")
            course = next((c for c in courses if c.course_id == course_id), None)
            if course:
                print(course.get_course_info())
            else:
                print("Course not found.")

        elif choice == "8":
            name = input("Enter department name: ")
            department_id = input("Enter department ID: ")
            head_of_department = input("Enter head of department: ")
            department = Department(department_id, name, head_of_department)
            departments.append(department)
            print("Department added successfully!")

        elif choice == "9":
            if not departments:
                print("No departments added yet.")
                continue
            for idx, dept in enumerate(departments):
                print(f"{idx}. {dept.name}")
            try:
                dep_idx = int(input(f"Select a department (0-{len(departments) - 1}): "))
                if 0 <= dep_idx < len(departments):
                    departments[dep_idx].get_information()
                else:
                    print("Invalid department index.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        elif choice == "10":
            name = input("Enter administrator name: ")
            admin_id = int(input("Enter administrator ID: "))
            role = input("Enter role: ")
            contact_info = input("Enter contact info: ")
            email = input("Enter email: ")
            administrators.append(Admin(admin_id, name, role, contact_info, email))
            print("Administrator added successfully!")
        elif choice == "11":
            if not administrators:
                print("No administrators added yet.")
                continue
            for admin in administrators:
                print(admin.get_info())

        elif choice == "12":
            classroom_id = input("Enter classroom ID: ")
            location = input("Enter classroom location: ")
            capacity = input("Enter classroom capacity: ")
            classrooms.append(Classroom(classroom_id, location, capacity))
            print("Classroom added successfully!")

        elif choice == "13":
            if not courses or not professors or not classrooms:
                print("Need at least one course, professor, and classroom to create schedule.")
                continue

            print("Available courses:")
            for idx, course in enumerate(courses):
                print(f"{idx}. {course.name} (ID: {course.course_id})")
            course_idx = int(input("Select course: "))

            print("Available professors:")
            for idx, prof in enumerate(professors):
                print(f"{idx}. {prof.name}")
            prof_idx = int(input("Select professor: "))

            print("Available classrooms:")
            for idx, room in enumerate(classrooms):
                print(f"{idx}. {room.location} (Capacity: {room.capacity})")
            room_idx = int(input("Select classroom: "))

            time_slot = input("Enter time slot (e.g., 'Mon 9-11'): ")
            schedule_id = f"sch_{len(schedules) + 1}"

            schedule = Schedule(schedule_id, courses[course_idx], professors[prof_idx], time_slot,
                                classrooms[room_idx].location)
            schedules.append(schedule)
            classrooms[room_idx].allocate_class(schedule)
            print("Schedule created successfully!")

        elif choice == "14":
            if not schedules:
                print("No schedules available to update.")
                continue

            for idx, s in enumerate(schedules):
                print(f"{idx}. {s.view_schedule()}")

            sched_idx = int(input("Select schedule to update: "))
            time_slot = input("Enter new time slot (leave blank to keep current): ")
            location = input("Enter new location (leave blank to keep current): ")

            if time_slot or location:
                schedules[sched_idx].update_schedule(time_slot if time_slot else None,
                                                     location if location else None)
                print("Schedule updated successfully!")
            else:
                print("No changes made.")

        elif choice == "15":
            if not schedules:
                print("No schedules available.")
                continue

            for s in schedules:
                print(s.view_schedule())

        elif choice == "16":
            if not courses:
                print("No courses available. Add a course first.")
                continue

            print("Available courses:")
            for idx, course in enumerate(courses):
                print(f"{idx}. {course.name}")

            course_idx = int(input("Select course: "))
            exam_id = f"exam_{len(exams) + 1}"
            date = input("Enter exam date (YYYY-MM-DD): ")
            duration = input("Enter exam duration (hours): ")
            passing_score = input("Enter passing score: ")

            exam = FinalExam(exam_id, courses[course_idx].name, date, duration, passing_score)
            exams.append(exam)
            print("Exam added successfully!")

        elif choice == "17":
            if not exams:
                print("No exams available to schedule.")
                continue

            for idx, exam in enumerate(exams):
                print(f"{idx}. {exam._course} on {exam.date}")

            exam_idx = int(input("Select exam to schedule: "))
            exams[exam_idx].schedule_exam()

        elif choice == "18":
            if not exams or not students:
                print("Need at least one exam and one student to record results.")
                continue

            print("Available exams:")
            for idx, exam in enumerate(exams):
                print(f"{idx}. {exam._course}")
            exam_idx = int(input("Select exam: "))

            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name}")
            student_idx = int(input("Select student: "))

            score = float(input("Enter score (0-100): "))
            exams[exam_idx].record_results(students[student_idx].name, score)

        elif choice == "19":
            if not exams:
                print("No exams available.")
                continue

            for idx, exam in enumerate(exams):
                print(f"{idx}. {exam._course}")

            exam_idx = int(input("Select exam to view results: "))
            exams[exam_idx].view_results()

        elif choice == "20":
            library_id = input("Enter library ID: ")
            libraries.append(Library(library_id))
            print("Library added successfully!")

        elif choice == "21":
            if not libraries:
                print("No libraries available. Add a library first.")
                continue

            library_idx = 0
            title = input("Enter book title: ")
            author = input("Enter author: ")
            category = input("Enter category: ")
            copies = int(input("Enter number of copies: "))

            libraries[library_idx].add_book(title, author, category, copies)

        elif choice == "22":
            if not libraries or not students:
                print("Need at least one library and one student to register.")
                continue

            library_idx = 0
            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name} (ID: {student._id})")
            student_idx = int(input("Select student: "))

            libraries[library_idx].register_student(students[student_idx]._id, students[student_idx].name)

        elif choice == "23":
            if not libraries or not students:
                print("Need at least one library and one student.")
                continue

            library_idx = 0
            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name}")
            student_idx = int(input("Select student: "))

            book_title = input("Enter book title to borrow: ")
            libraries[library_idx].borrow_book(students[student_idx]._id, book_title)

        elif choice == "24":
            if not libraries or not students:
                print("Need at least one library and one student.")
                continue

            library_idx = 0
            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name}")
            student_idx = int(input("Select student: "))

            book_title = input("Enter book title to return: ")
            libraries[library_idx].return_book(students[student_idx]._id, book_title)

        elif choice == "25":
            if not libraries:
                print("No libraries available.")
                continue

            library_idx = 0
            keyword = input("Enter search keyword (title/author/category): ")
            libraries[library_idx].search_book(keyword)

        elif choice == "26":
            if not students or not courses:
                print("Need at least one student and one course.")
                continue

            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name}")
            student_idx = int(input("Select student: "))

            print("Available courses:")
            for idx, course in enumerate(courses):
                print(f"{idx}. {course.name}")
            course_idx = int(input("Select course: "))

            date = input("Enter date (YYYY-MM-DD): ")
            status = input("Enter status (Present/Absent): ")

            try:
                attendance = Attendance(students[student_idx], courses[course_idx], date, status)
                attendance_records.append(attendance)

                if not attendance_reports:
                    attendance_reports.append(AttendanceReport())
                attendance_reports[0].add_attendance(attendance)

                print("Attendance recorded successfully!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "27":
            if not students or not attendance_reports:
                print("No students or attendance records available.")
                continue

            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name}")
            student_idx = int(input("Select student: "))

            attendance_reports[0].get_student_attendance(students[student_idx])

        elif choice == "28":
            if not courses or not attendance_reports:
                print("No courses or attendance records available.")
                continue

            print("Available courses:")
            for idx, course in enumerate(courses):
                print(f"{idx}. {course.name}")
            course_idx = int(input("Select course: "))

            attendance_reports[0].get_course_attendance(courses[course_idx])

        elif choice == "29":
            if not students or not attendance_reports:
                print("No students or attendance records available.")
                continue

            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name}")
            student_idx = int(input("Select student: "))

            print("Available courses (or skip for all courses):")
            for idx, course in enumerate(courses):
                print(f"{idx}. {course.name}")
            course_choice = input("Enter course index or press Enter for all: ")

            if course_choice:
                course_idx = int(course_choice)
                attendance_reports[0].calculate_attendance_percentage(
                    students[student_idx], courses[course_idx])
            else:
                attendance_reports[0].calculate_attendance_percentage(students[student_idx])


        elif choice == "30":
            if not attendance_records:
                print("No attendance records available.")
                continue

            role = input("Enter your role (admin/professor): ")
            proxy = AttendanceProxy(role)
            proxy.attendance_records = attendance_records

            print("Available students:")
            for idx, student in enumerate(students):
                print(f"{idx}. {student.name} (ID: {student._id})")
            student_idx = int(input("Select student: "))

            date = input("Enter date (YYYY-MM-DD) to update: ")
            new_status = input("Enter new status (Present/Absent): ")
            success = proxy.update_status(students[student_idx]._id, date, new_status)
            if success and attendance_reports:
                print("Attendance status updated in records and reports.")

        elif choice == "31":
            email = input("Enter your email: ")
            password = input("Enter your password: ")

            user = User.get_user_by_email(email)
            if not user:
                print("User not found. Please register first.")
                continue

            if user.login(password):
                print("Login successful.")
            else:
                print("Login failed.")

        elif choice == "32":
            current_user = User.get_logged_in_user()
            if current_user:
                current_user.logout()
            else:
                print("No user is currently logged in.")

        elif choice == "33":
            current_user = User.get_logged_in_user()
            if current_user:
                current_user.view_dashboard()
            else:
                print("No user is currently logged in.")

        elif choice == "34":
            print("Select user type:")
            print("1. Student")
            print("2. Professor")
            print("3. Administrator")
            role_choice = input("Enter choice: ")

            role_map = {"1": "student", "2": "professor", "3": "admin"}
            role = role_map.get(role_choice)
            if not role:
                print("Invalid role choice.")
                continue

            user_id = input("Enter user ID: ")
            name = input("Enter name: ")
            email = input("Enter email: ")
            password = input("Enter password: ")

            user = User.register_user(user_id, name, role, email, password)
            if user:
                print("You can now log in using your credentials.")


        elif choice == "35":
            print("Exiting University Management System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Run as:")
    print("1. Command-Line Interface (CLI)")
    print("2. Network Server")
    mode = input("Enter choice (1 or 2): ")

    if mode == '1':
        main_cli()
    elif mode == '2':
        start_server()
    else:
        print("Invalid choice. Exiting.")
