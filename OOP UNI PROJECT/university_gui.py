import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import io
import sys

import university_management_last_version1 as ums


def capture_output(func, *args, **kwargs):
    old_stdout = sys.stdout #print on screen
    sys.stdout = captured_output_io = io.StringIO()  #print in a fake box in memory 
    try:
        func(*args, **kwargs)
    finally:
        sys.stdout = old_stdout
    return captured_output_io.getvalue()


class InputDialog(tk.Toplevel):
    def __init__(self, parent, title, fields):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = {}
        self.entries = {}

        for i, (field_name, field_type) in enumerate(fields):  # field_type is not used but kept for compatibility
            ttk.Label(self, text=f"{field_name}:").grid(row=i, column=0, padx=10, pady=5, sticky="w") # we creat a label
            entry = ttk.Entry(self) # we creat a textbox
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[field_name] = entry

        button_frame = ttk.Frame(self)  #creating frame
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=10)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.wait_window(self) #wait for user input

    def ok_clicked(self):
        for field_name, entry in self.entries.items():
            self.result[field_name] = entry.get()
        self.destroy()

    def cancel_clicked(self):
        self.result = None
        self.destroy()


class UniversityGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("University Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="pink")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.students_tab = ttk.Frame(self.notebook)
        self.professors_tab = ttk.Frame(self.notebook)
        self.courses_tab = ttk.Frame(self.notebook)
        self.departments_tab = ttk.Frame(self.notebook)
        self.admin_tab = ttk.Frame(self.notebook)
        self.classroom_tab = ttk.Frame(self.notebook)
        self.schedule_tab = ttk.Frame(self.notebook)
        self.exam_tab = ttk.Frame(self.notebook)
        self.library_tab = ttk.Frame(self.notebook)
        self.user_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.students_tab, text="Students")
        self.notebook.add(self.professors_tab, text="Professors")
        self.notebook.add(self.courses_tab, text="Courses")
        self.notebook.add(self.departments_tab, text="Departments")
        self.notebook.add(self.admin_tab, text="Administrators")
        self.notebook.add(self.classroom_tab, text="Classrooms")
        self.notebook.add(self.schedule_tab, text="Schedules")
        self.notebook.add(self.exam_tab, text="Exams")
        self.notebook.add(self.library_tab, text="Library")
        self.notebook.add(self.user_tab, text="User")

        self.setup_students_tab()
        self.setup_professors_tab()
        self.setup_courses_tab()
        self.setup_departments_tab()
        self.setup_admin_tab()
        self.setup_classroom_tab()
        self.setup_schedule_tab()
        self.setup_exam_tab()
        self.setup_library_tab()
        self.setup_user_tab()

    def setup_students_tab(self):
        frame = ttk.LabelFrame(self.students_tab, text="Students Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Student", command=self.add_student).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="View Student Info", command=self.view_student_info).grid(row=0, column=1, padx=5,
                                                                                         pady=5)  # Renamed for clarity
        ttk.Button(frame, text="Enroll in Course", command=self.enroll_student).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Drop Course", command=self.drop_student_course).grid(row=1, column=1, padx=5, pady=5)

        self.students_list = tk.Listbox(frame, width=60, height=15)
        self.students_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_students).grid(row=3, column=0, columnspan=2,
                                                                                   padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)  #expand equally
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

    def setup_professors_tab(self):
        frame = ttk.LabelFrame(self.professors_tab, text="Professors Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Professor", command=self.add_professor).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="View Professor Info", command=self.view_professor_info).grid(row=0, column=1, padx=5,
                                                                                             pady=5)

        self.professors_list = tk.Listbox(frame, width=60, height=15)
        self.professors_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_professors).grid(row=2, column=0, columnspan=2,
                                                                                     padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def setup_courses_tab(self):
        frame = ttk.LabelFrame(self.courses_tab, text="Courses Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Course", command=self.add_course).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="View Course Info", command=self.view_course_info).grid(row=0, column=1, padx=5,
                                                                                       pady=5)  # Renamed

        self.courses_list = tk.Listbox(frame, width=60, height=15)
        self.courses_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_courses).grid(row=2, column=0, columnspan=2, padx=5,
                                                                                  pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def setup_departments_tab(self):
        frame = ttk.LabelFrame(self.departments_tab, text="Departments Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Department", command=self.add_department).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="View Department Info", command=self.view_department_info).grid(row=0, column=1, padx=5,
                                                                                               pady=5)

        self.departments_list = tk.Listbox(frame, width=60, height=15)
        self.departments_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_departments).grid(row=2, column=0, columnspan=2,
                                                                                      padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def setup_admin_tab(self):
        frame = ttk.LabelFrame(self.admin_tab, text="Administrators Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Administrator", command=self.add_administrator).grid(row=0, column=0, padx=5,
                                                                                         pady=5)
        ttk.Button(frame, text="View Administrator Info", command=self.view_admin_info).grid(row=0, column=1, padx=5,
                                                                                             pady=5)

        self.admin_list = tk.Listbox(frame, width=60, height=15)
        self.admin_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_administrators).grid(row=2, column=0, columnspan=2,
                                                                                         padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def setup_classroom_tab(self):
        frame = ttk.LabelFrame(self.classroom_tab, text="Classrooms Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Classroom", command=self.add_classroom).grid(row=0, column=0, padx=5, pady=5)
        # Add View Classroom Info if needed

        self.classroom_list = tk.Listbox(frame, width=60, height=15)
        self.classroom_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_classrooms).grid(row=2, column=0, columnspan=2,
                                                                                     padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def setup_schedule_tab(self):
        frame = ttk.LabelFrame(self.schedule_tab, text="Schedules Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Create Schedule", command=self.create_schedule).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Update Schedule", command=self.update_schedule).grid(row=0, column=1, padx=5, pady=5)

        self.schedule_list = tk.Listbox(frame, width=70, height=15)
        self.schedule_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_schedules).grid(row=2, column=0, columnspan=2,
                                                                                    padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(1, weight=1)

    def setup_exam_tab(self):
        frame = ttk.LabelFrame(self.exam_tab, text="Exams Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Exam", command=self.add_exam).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Schedule Exam", command=self.schedule_exam).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame, text="Record Exam Results", command=self.record_exam_results).grid(row=1, column=0, padx=5,
                                                                                             pady=5)
        ttk.Button(frame, text="View Exam Results", command=self.view_exam_results).grid(row=1, column=1, padx=5,
                                                                                         pady=5)

        self.exam_list = tk.Listbox(frame, width=60, height=10)
        self.exam_list.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh List", command=self.refresh_exams).grid(row=3, column=0, columnspan=2, padx=5,
                                                                                pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(2, weight=1)

    def setup_library_tab(self):
        frame = ttk.LabelFrame(self.library_tab, text="Library Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Add Library", command=self.add_library).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Add Book to Library", command=self.add_book_to_library).grid(row=0, column=1, padx=5,
                                                                                             pady=5)
        ttk.Button(frame, text="Register Student (All Libraries)", command=self.register_student_to_all_libraries).grid(
            row=1, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Borrow Book", command=self.borrow_book_from_library).grid(row=1, column=1, padx=5,
                                                                                          pady=5)
        ttk.Button(frame, text="Return Book", command=self.return_book_to_library).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Search Book in Library", command=self.search_book_in_library).grid(row=2, column=1,
                                                                                                   padx=5, pady=5)

        self.library_list_display = tk.Listbox(frame, width=60, height=10)
        self.library_list_display.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        ttk.Button(frame, text="Refresh Libraries List", command=self.refresh_libraries_list_display).grid(row=4,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           padx=5,
                                                                                                           pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(3, weight=1)

    def setup_user_tab(self):
        frame = ttk.LabelFrame(self.user_tab, text="User Management")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        register_frame = ttk.LabelFrame(frame, text="Register")
        register_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        login_frame = ttk.LabelFrame(frame, text="Login/Logout")
        login_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Button(register_frame, text="Register New User", command=self.register_user).pack(pady=10, padx=10,
                                                                                              fill=tk.X)

        ttk.Button(login_frame, text="Login", command=self.login_user).pack(pady=10, padx=10, fill=tk.X)
        ttk.Button(login_frame, text="Logout", command=self.logout_user).pack(pady=10, padx=10, fill=tk.X)
        ttk.Button(login_frame, text="View My Dashboard", command=self.view_dashboard).pack(pady=10, padx=10, fill=tk.X)

        self.user_info_text = tk.Text(frame, width=40, height=10, wrap=tk.WORD)  # Renamed
        self.user_info_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

        self.refresh_user_info_display()

    def register_user(self):
        fields = [("User ID", ""), ("Name", ""), ("Role (student, professor, admin)", ""), ("Email", ""),
                  ("Password", "")]
        dialog = InputDialog(self.root, "Register New User", fields)
        if dialog.result:
            user_id = dialog.result.get("User ID")
            name = dialog.result.get("Name")
            role = dialog.result.get("Role (student, professor, admin)")
            email = dialog.result.get("Email")
            password = dialog.result.get("Password")

            if all([user_id, name, role, email, password]):
                new_user = ums.User.register_user(user_id, name, role, email, password)
                if new_user:
                    messagebox.showinfo("Success", f"User '{name}' registered successfully with email '{email}'.")
            else:
                messagebox.showwarning("Input Error", "All fields are required.")
        self.refresh_user_info_display()

    def login_user(self):
        fields = [("Email", ""), ("Password", "")]
        dialog = InputDialog(self.root, "Login", fields)
        if dialog.result:
            email = dialog.result.get("Email")
            password = dialog.result.get("Password")

            if email and password:
                user = ums.User.get_user_by_email(email)
                if user:
                    if user.login(password):
                        messagebox.showinfo("Login Success", f"Welcome, {user.name}!")

                else:
                    messagebox.showwarning("Login Failed", "User not found. Please register first.")
            else:
                messagebox.showwarning("Input Error", "Email and Password are required.")
        self.refresh_user_info_display()

    def logout_user(self):
        current_user = ums.User.get_logged_in_user()
        if current_user:
            current_user.logout()
        else:
            messagebox.showinfo("Logout", "No user is currently logged in.")
        self.refresh_user_info_display()

    def view_dashboard(self):
        current_user = ums.User.get_logged_in_user()
        if current_user:
            dashboard_text = capture_output(current_user.view_dashboard)

            self.user_info_text.delete(1.0, tk.END)
            self.user_info_text.insert(tk.END, "Current User Dashboard:\n")
            self.user_info_text.insert(tk.END, dashboard_text)
        else:
            messagebox.showinfo("Dashboard", "No user is logged in. Please log in to view dashboard.")
            self.refresh_user_info_display()

    def refresh_user_info_display(self):
        self.user_info_text.delete(1.0, tk.END)
        current_user = ums.User.get_logged_in_user()
        if current_user:
            info = f"Logged in as: {current_user.name}\n"
            info += f"Role: {current_user.role}\n"
            info += f"Email: {current_user.email}\n"
            info += f"User ID: {current_user.user_id}"
            self.user_info_text.insert(tk.END, info)
        else:
            self.user_info_text.insert(tk.END, "No user is currently logged in.")


    def add_student(self):
        fields = [("Name", ""), ("Student ID", ""), ("Major", ""), ("Email", "")]
        dialog = InputDialog(self.root, "Add Student", fields)
        if dialog.result:
            name = dialog.result.get("Name")
            student_id = dialog.result.get("Student ID")
            major = dialog.result.get("Major")
            email = dialog.result.get("Email")
            if name and student_id and major and email:
                if any(s._id == student_id for s in ums.students):
                    messagebox.showerror("Error", f"Student with ID {student_id} already exists.")
                    return
                student = ums.Student(student_id, name, major, email)
                ums.students.append(student)
                messagebox.showinfo("Success", f"Student {name} added.")
                self.refresh_students()
            else:
                messagebox.showwarning("Input Error", "All fields are required.")

    def view_student_info(self):
        if not ums.students: messagebox.showinfo("Info", "No students available."); return
        student_id = simpledialog.askstring("Input", "Enter Student ID:")
        if student_id:
            student = next((s for s in ums.students if s.get_id() == student_id), None)
            if student:
                info = student.get_info()
                result_str = "\n".join([f"{k}: {v}" for k, v in info.items()])
                messagebox.showinfo(f"Info for {student.name}", result_str)
            else:
                messagebox.showerror("Error", "Student not found.")

    def enroll_student(self):
        if not ums.students: messagebox.showinfo("Info", "No students available."); return
        if not ums.courses: messagebox.showinfo("Info", "No courses available."); return

        fields = [("Student ID", ""), ("Course ID", "")]
        dialog = InputDialog(self.root, "Enroll Student", fields)
        if dialog.result:
            student_id = dialog.result.get("Student ID")
            course_id = dialog.result.get("Course ID")
            student = next((s for s in ums.students if s.get_id() == student_id), None)
            course = next((c for c in ums.courses if c.course_id == course_id), None)

            if student and course:
                capture_output(student.enroll_course, course.course_id, course.name)
                course.add_student(student)
                messagebox.showinfo("Enrollment", f"Enrollment process for {student.name} in {course.name} attempted.")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Invalid Student ID or Course ID.")

    def drop_student_course(self):
        if not ums.students: messagebox.showinfo("Info", "No students available."); return
        if not ums.courses: messagebox.showinfo("Info", "No courses available."); return

        fields = [("Student ID", ""), ("Course ID", "")]
        dialog = InputDialog(self.root, "Drop Course", fields)
        if dialog.result:
            student_id = dialog.result.get("Student ID")
            course_id = dialog.result.get("Course ID")
            student = next((s for s in ums.students if s.get_id() == student_id), None)
            course = next((c for c in ums.courses if c.course_id == course_id), None)
            if student and course:
                capture_output(student.drop_course, course.course_id)
                capture_output(course.remove_student, student)
                messagebox.showinfo("Drop Course",
                                    f"Drop course process for {student.name} from {course.name} attempted.")
                self.refresh_students()
            else:
                messagebox.showerror("Error", "Invalid Student ID or Course ID.")

    def refresh_students(self):
        self.students_list.delete(0, tk.END)
        for s in ums.students:
            self.students_list.insert(tk.END, f"{s.get_id()} - {s.name} ({s._major})")

    def add_professor(self):
        fields = [("Name", ""), ("Professor ID", ""), ("Department", ""), ("Contact Info", ""), ("Email", "")]
        dialog = InputDialog(self.root, "Add Professor", fields)
        if dialog.result:
            name = dialog.result.get("Name")
            prof_id = dialog.result.get("Professor ID")
            dept_name = dialog.result.get("Department")
            contact = dialog.result.get("Contact Info")
            email = dialog.result.get("Email")
            if all([name, prof_id, dept_name, contact, email]):
                if any(p.professor_id == prof_id for p in ums.professors):
                    messagebox.showerror("Error", f"Professor with ID {prof_id} already exists.")
                    return
                prof = ums.Professor(prof_id, name, dept_name, contact, email)
                ums.professors.append(prof)
                # link to department
                department_obj = next((d for d in ums.departments if d.name == dept_name), None)
                if department_obj:
                    department_obj.list_professors(prof)
                else:
                    messagebox.showwarning("Warning",
                                           f"Department '{dept_name}' not found. Professor added but not linked to a department list.")
                messagebox.showinfo("Success", f"Professor {name} added.")
                self.refresh_professors()
            else:
                messagebox.showwarning("Input Error", "All fields are required.")

    def view_professor_info(self):
        if not ums.professors: messagebox.showinfo("Info", "No professors available."); return
        prof_id = simpledialog.askstring("Input", "Enter Professor ID:")
        if prof_id:
            professor = next((p for p in ums.professors if p.professor_id == prof_id), None)
            if professor:
                info = professor.get_info()
                result_str = "\n".join([f"{k}: {v}" for k, v in info.items()])
                messagebox.showinfo(f"Info for {professor.name}", result_str)
            else:
                messagebox.showerror("Error", "Professor not found.")

    def refresh_professors(self):
        self.professors_list.delete(0, tk.END)
        for p in ums.professors:
            self.professors_list.insert(tk.END, f"{p.professor_id} - {p.name} ({p.department})")


    def add_course(self):
        if not ums.professors: 
            messagebox.showinfo("Info", "Add a professor first."); 
            return

        fields = [("Name", ""), ("Course ID", ""), ("Department", ""), ("Credits", "")]
        dialog = InputDialog(self.root, "Add Course", fields)
        if not dialog.result: 
            return

        name = dialog.result.get("Name")
        course_id = dialog.result.get("Course ID")
        dept_name = dialog.result.get("Department")
        credits_str = dialog.result.get("Credits")

        if not all([name, course_id, dept_name, credits_str]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        if any(c.course_id == course_id for c in ums.courses):
            messagebox.showerror("Error", f"Course with ID {course_id} already exists.")
            return

        try:
            credits = int(credits_str)
        except ValueError:
            messagebox.showerror("Input Error", "Credits must be a number.")
            return

        selected_professor = self._select_item_dialog(ums.professors, "Select Professor for Course", 
                                                     lambda p: f"{p.name} (ID: {p.professor_id})")
        
        if not selected_professor:
            messagebox.showinfo("Cancelled", "Course addition cancelled - no professor selected.")
            return

        course = ums.Course(course_id, name, dept_name, credits, selected_professor)
        ums.courses.append(course)

        department_obj = next((d for d in ums.departments if d.name == dept_name), None)
        if department_obj:
            department_obj.list_courses(course)
        else:
            messagebox.showwarning("Warning", 
                                 f"Department '{dept_name}' not found. Course added but not linked to a department list.")
        
        messagebox.showinfo("Success", f"Course {name} added with professor {selected_professor.name}.")
        self.refresh_courses()

    def view_course_info(self):
        if not ums.courses: messagebox.showinfo("Info", "No courses available."); return
        course_id = simpledialog.askstring("Input", "Enter Course ID:")
        if course_id:
            course = next((c for c in ums.courses if c.course_id == course_id), None)
            if course:
                info = course.get_course_info()
                result_str = "\n".join([f"{k}: {v}" for k, v in info.items()])
                messagebox.showinfo(f"Info for {course.name}", result_str)
            else:
                messagebox.showerror("Error", "Course not found.")

    def refresh_courses(self):
        self.courses_list.delete(0, tk.END)
        for c in ums.courses:
            prof_name = c.professor.name if c.professor else  "Not Available"
            self.courses_list.insert(tk.END, f"{c.course_id} - {c.name} ({c.department}) - Prof: {prof_name}")

    def add_department(self):
        fields = [("Department ID", ""), ("Name", ""), ("Head of Department", "")]
        dialog = InputDialog(self.root, "Add Department", fields)
        if dialog.result:
            dept_id = dialog.result.get("Department ID")
            name = dialog.result.get("Name")
            hod = dialog.result.get("Head of Department")
            if all([dept_id, name, hod]):
                if any(d.department_id == dept_id for d in ums.departments):
                    messagebox.showerror("Error", f"Department with ID {dept_id} already exists.")
                    return
                dept = ums.Department(dept_id, name, hod)
                ums.departments.append(dept)
                messagebox.showinfo("Success", f"Department {name} added.")
                self.refresh_departments()
            else:
                messagebox.showwarning("Input Error", "All fields are required.")

    def view_department_info(self):
        if not ums.departments: messagebox.showinfo("Info", "No departments available."); return

        dept_select_window = tk.Toplevel(self.root)
        dept_select_window.title("Select Department")
        dept_select_window.geometry("300x250")
        dept_select_window.transient(self.root)
        dept_select_window.grab_set()
        ttk.Label(dept_select_window, text="Select Department:").pack(pady=5)
        dept_lb = tk.Listbox(dept_select_window)
        for dept in ums.departments:
            dept_lb.insert(tk.END, f"{dept.name} (ID: {dept.department_id})")
        dept_lb.pack(pady=5, fill=tk.BOTH, expand=True)

        temp_storage = {}

        def on_select():
            try:
                idx = dept_lb.curselection()[0]
                temp_storage['department'] = ums.departments[idx]
                dept_select_window.destroy()
            except IndexError:
                messagebox.showerror("Selection Error", "Please select a department.", parent=dept_select_window)

        ttk.Button(dept_select_window, text="View Info", command=on_select).pack(pady=5)
        self.root.wait_window(dept_select_window)

        department = temp_storage.get('department')
        if department:
            info_str = f"Department ID: {department.department_id}\n"
            info_str += f"Name: {department.name}\n"
            info_str += f"Head: {department.head_of_department}\n"
            info_str += f"Courses Offered: {len(department.courses_offered)}\n"
            info_str += f"Faculty Members: {len(department.faculty_members)}"
            messagebox.showinfo(f"Info for {department.name}", info_str)

    def refresh_departments(self):
        self.departments_list.delete(0, tk.END)
        for d in ums.departments:
            self.departments_list.insert(tk.END, f"{d.department_id} - {d.name} (HOD: {d.head_of_department})")


    def add_administrator(self):
        fields = [("Name", ""), ("Admin ID (number)", ""), ("Role", ""), ("Contact Info", ""), ("Email", "")]
        dialog = InputDialog(self.root, "Add Administrator", fields)
        if dialog.result:
            name = dialog.result.get("Name")
            admin_id_str = dialog.result.get("Admin ID (number)")
            role = dialog.result.get("Role")
            contact = dialog.result.get("Contact Info")
            email = dialog.result.get("Email")
            if all([name, admin_id_str, role, contact, email]):
                try:
                    admin_id = int(admin_id_str)
                    if any(a.get_admin_id() == admin_id for a in ums.administrators):
                        messagebox.showerror("Error", f"Administrator with ID {admin_id} already exists.")
                        return
                    admin = ums.Admin(admin_id, name, role, contact, email)
                    ums.administrators.append(admin)
                    messagebox.showinfo("Success", f"Administrator {name} added.")
                    self.refresh_administrators()
                except ValueError:
                    messagebox.showerror("Input Error", "Admin ID must be an integer.")
            else:
                messagebox.showwarning("Input Error", "All fields are required.")

    def view_admin_info(self):
        if not ums.administrators: messagebox.showinfo("Info", "No administrators available."); return
        admin_select_window = tk.Toplevel(self.root)
        admin_id_str = simpledialog.askstring("Input", "Enter Admin ID:")
        if admin_id_str:
            try:
                admin_id = int(admin_id_str)
                admin = next((a for a in ums.administrators if a.get_admin_id() == admin_id), None)
                if admin:
                    info = admin.get_info()
                    result_str = "\n".join([f"{k}: {v}" for k, v in info.items()])
                    messagebox.showinfo(f"Info for {admin.name}", result_str)
                else:
                    messagebox.showerror("Error", "Administrator not found.")
            except ValueError:
                messagebox.showerror("Input Error", "Admin ID must be an integer.")

    def refresh_administrators(self):
        self.admin_list.delete(0, tk.END)
        for a in ums.administrators:
            self.admin_list.insert(tk.END, f"{a.get_admin_id()} - {a.name} ({a.role})")

    def add_classroom(self):
        fields = [("Classroom ID", ""), ("Location", ""), ("Capacity (number)", "")]
        dialog = InputDialog(self.root, "Add Classroom", fields)
        if dialog.result:
            class_id = dialog.result.get("Classroom ID")
            location = dialog.result.get("Location")
            capacity_str = dialog.result.get("Capacity (number)")
            if all([class_id, location, capacity_str]):
                try:
                    capacity = int(capacity_str)
                    if any(cr.classroom_id == class_id for cr in ums.classrooms):
                        messagebox.showerror("Error", f"Classroom with ID {class_id} already exists.")
                        return
                    classroom = ums.Classroom(class_id, location, capacity)
                    ums.classrooms.append(classroom)
                    messagebox.showinfo("Success", f"Classroom {class_id} at {location} added.")
                    self.refresh_classrooms()
                except ValueError:
                    messagebox.showerror("Input Error", "Capacity must be an integer.")
            else:
                messagebox.showwarning("Input Error", "All fields are required.")

    def refresh_classrooms(self):
        self.classroom_list.delete(0, tk.END)
        for cr in ums.classrooms:
            self.classroom_list.insert(tk.END, f"{cr.classroom_id} - {cr.location} (Cap: {cr.capacity})")

    def create_schedule(self):
        if not ums.courses: messagebox.showinfo("Info", "Add courses first."); return
        if not ums.professors: messagebox.showinfo("Info", "Add professors first."); return
        if not ums.classrooms: messagebox.showinfo("Info", "Add classrooms first."); return

        fields1 = [("Schedule ID", ""), ("Time Slot (e.g., Mon 9-11)", "")]
        dialog1 = InputDialog(self.root, "Schedule Details", fields1)
        if not dialog1.result: return
        schedule_id = dialog1.result.get("Schedule ID")
        time_slot = dialog1.result.get("Time Slot (e.g., Mon 9-11)")
        if not all([schedule_id, time_slot]):
            messagebox.showwarning("Input Error", "Schedule ID and Time Slot are required.");
            return
        if any(s.get_schedule_id() == schedule_id for s in ums.schedules):
            messagebox.showerror("Error", f"Schedule with ID {schedule_id} already exists.");
            return

        selected_course = self._select_item_dialog(ums.courses, "Select Course",
                                                   lambda c: f"{c.name} (ID: {c.course_id})")
        if not selected_course: return

        selected_professor = self._select_item_dialog(ums.professors, "Select Professor",
                                                      lambda p: f"{p.name} (ID: {p.professor_id})")
        if not selected_professor: return

        selected_classroom = self._select_item_dialog(ums.classrooms, "Select Classroom",
                                                      lambda cr: f"{cr.location} (ID: {cr.classroom_id})")
        if not selected_classroom: return

        # create schedule
        schedule_obj = ums.Schedule(schedule_id, selected_course, selected_professor, time_slot,
                                    selected_classroom.location)
        ums.schedules.append(schedule_obj)

        output = capture_output(selected_classroom.allocate_class, schedule_obj)
        messagebox.showinfo("Schedule Creation", output.strip())
        self.refresh_schedules()

    def _select_item_dialog(self, item_list, title, display_func):
        if not item_list: return None

        select_window = tk.Toplevel(self.root)
        select_window.title(title)
        select_window.geometry("400x300")
        select_window.transient(self.root)
        select_window.grab_set()
        ttk.Label(select_window, text=f"{title}:").pack(pady=5)
        lb = tk.Listbox(select_window, width=50, height=10)
        for item in item_list:
            lb.insert(tk.END, display_func(item))
        lb.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        storage = {}

        def on_select_action():
            try:
                idx = lb.curselection()[0]
                storage['selected'] = item_list[idx]
                select_window.destroy()
            except IndexError:
                messagebox.showerror("Error", "Please make a selection.", parent=select_window)

        ttk.Button(select_window, text="Select", command=on_select_action).pack(pady=10)
        self.root.wait_window(select_window)
        return storage.get('selected')

    def update_schedule(self):
        if not ums.schedules: messagebox.showinfo("Info", "No schedules to update."); return

        selected_schedule = self._select_item_dialog(ums.schedules, "Select Schedule to Update",
                                                     lambda s: s.view_schedule())
        if not selected_schedule: return

        fields = [("New Time Slot (optional)", ""), ("New Location (optional, from existing classrooms)", "")]
        dialog = InputDialog(self.root, f"Update Schedule {selected_schedule.get_schedule_id()}", fields)
        if dialog.result:
            new_time_slot = dialog.result.get("New Time Slot (optional)")
            new_location_str = dialog.result.get("New Location (optional, from existing classrooms)")

            if not new_time_slot and not new_location_str:
                messagebox.showinfo("Update Schedule", "No changes specified.");
                return

            output = capture_output(selected_schedule.update_schedule,
                                    new_time_slot if new_time_slot else None,
                                    new_location_str if new_location_str else None)
            messagebox.showinfo("Schedule Update", output.strip())
            self.refresh_schedules()

    def refresh_schedules(self):
        self.schedule_list.delete(0, tk.END)
        for s in ums.schedules:
            self.schedule_list.insert(tk.END, s.view_schedule())

    def add_exam(self):
        if not ums.courses: messagebox.showinfo("Info", "Add courses first."); return

        selected_course = self._select_item_dialog(ums.courses, "Select Course for Exam",
                                                   lambda c: f"{c.name} (ID: {c.course_id})")
        if not selected_course: return

        fields = [("Exam ID", ""), ("Date (YYYY-MM-DD)", ""), ("Duration (hours)", ""), ("Passing Score", "")]
        dialog = InputDialog(self.root, f"Add Exam for {selected_course.name}", fields)
        if dialog.result:
            exam_id = dialog.result.get("Exam ID")
            date = dialog.result.get("Date (YYYY-MM-DD)")
            duration_str = dialog.result.get("Duration (hours)")
            passing_score_str = dialog.result.get("Passing Score")
            if not all([exam_id, date, duration_str, passing_score_str]):
                messagebox.showwarning("Input Error", "All fields are required.");
                return
            if any(e.get_exam_id() == exam_id for e in ums.exams):
                messagebox.showerror("Error", f"Exam with ID {exam_id} already exists.");
                return

            try:
                duration = float(duration_str)
                passing_score = float(passing_score_str)
                exam = ums.FinalExam(exam_id, selected_course.name, date, duration, passing_score)
                ums.exams.append(exam)
                messagebox.showinfo("Success", f"Exam {exam_id} for course {selected_course.name} added.")
                self.refresh_exams()
            except ValueError:
                messagebox.showerror("Input Error", "Duration and Passing Score must be numbers.")

    def schedule_exam(self):
        if not ums.exams: messagebox.showinfo("Info", "No exams to schedule."); return

        selected_exam = self._select_item_dialog(ums.exams, "Select Exam to Schedule",
                                                 lambda e: f"{e.get_exam_id()} for {e._course}")
        if not selected_exam: return

        output = capture_output(selected_exam.schedule_exam)
        messagebox.showinfo("Schedule Exam", output.strip())

    def record_exam_results(self):
        if not ums.exams: messagebox.showinfo("Info", "No exams available."); return

        selected_exam = self._select_item_dialog(ums.exams, "Select Exam to Record Results",
                                                 lambda e: f"{e.get_exam_id()} for {e._course}")
        if not selected_exam: return

        fields = [("Student Name", ""), ("Score (0-100)", "")]
        dialog = InputDialog(self.root, f"Record Results for Exam {selected_exam.get_exam_id()}", fields)
        if dialog.result:
            student_name = dialog.result.get("Student Name")
            score_str = dialog.result.get("Score (0-100)")
            if student_name and score_str:
                try:
                    score = float(score_str)
                    output = capture_output(selected_exam.record_results, student_name, score)
                    messagebox.showinfo("Record Results", output.strip())
                except ValueError:
                    messagebox.showerror("Input Error", "Score must be a number.")
            else:
                messagebox.showwarning("Input Error", "Student Name and Score are required.")

    def view_exam_results(self):
        if not ums.exams: messagebox.showinfo("Info", "No exams available."); return

        selected_exam = self._select_item_dialog(ums.exams, "Select Exam to View Results",
                                                 lambda e: f"{e.get_exam_id()} for {e._course}")
        if not selected_exam: return

        output = capture_output(selected_exam.view_results)  # view_results prints
        messagebox.showinfo(f"Results for Exam {selected_exam.get_exam_id()}",
                            output.strip() if output.strip() else "No results recorded yet.")

    def refresh_exams(self):
        self.exam_list.delete(0, tk.END)
        for e in ums.exams:
            self.exam_list.insert(tk.END, f"{e.get_exam_id()} - Course: {e._course} (Date: {e.date})")

    def add_library(self):
        fields = [("Library ID", "")]
        dialog = InputDialog(self.root, "Add Library", fields)
        if dialog.result:
            lib_id = dialog.result.get("Library ID")
            if lib_id:
                if any(l.get_library_id() == lib_id for l in ums.libraries):
                    messagebox.showerror("Error", f"Library with ID {lib_id} already exists.")
                    return
                lib = ums.Library(lib_id)
                ums.libraries.append(lib)
                messagebox.showinfo("Success", f"Library {lib_id} added.")
                self.refresh_libraries_list_display()
            else:
                messagebox.showwarning("Input Error", "Library ID is required.")

    def _get_selected_library(self, action_title):
        if not ums.libraries:
            messagebox.showinfo("Info", "No libraries available. Add a library first.")
            return None
        if len(ums.libraries) == 1:
            return ums.libraries[0]

        return self._select_item_dialog(ums.libraries, f"{action_title} - Select Library",
                                        lambda l: f"ID: {l.get_library_id()}")

    def add_book_to_library(self):
        selected_library = self._get_selected_library("Add Book")
        if not selected_library: return

        fields = [("Book Title", ""), ("Author", ""), ("Category", ""), ("Copies (number, default 1)", "")]
        dialog = InputDialog(self.root, f"Add Book to Library {selected_library.get_library_id()}", fields)
        if dialog.result:
            title = dialog.result.get("Book Title")
            author = dialog.result.get("Author")
            category = dialog.result.get("Category")
            copies_str = dialog.result.get("Copies (number, default 1)") or "1"  # Default to 1
            if all([title, author, category]):
                try:
                    copies = int(copies_str)
                    output = capture_output(selected_library.add_book, title, author, category, copies)
                    messagebox.showinfo("Add Book", output.strip())
                except ValueError:
                    messagebox.showerror("Input Error", "Copies must be an integer.")
            else:
                messagebox.showwarning("Input Error", "Title, Author, and Category are required.")

    def register_student_to_all_libraries(self):
        if not ums.libraries: messagebox.showinfo("Info", "No libraries available."); return

        fields = [("Student ID", ""), ("Student Name", "")]
        dialog = InputDialog(self.root, "Register Student to Libraries", fields)
        if dialog.result:
            student_id = dialog.result.get("Student ID")
            student_name = dialog.result.get("Student Name")
            if student_id and student_name:
                full_output = []
                for lib in ums.libraries:
                    output = capture_output(lib.register_student, student_id, student_name)
                    full_output.append(f"Library {lib.get_library_id()}: {output.strip()}")
                messagebox.showinfo("Student Registration", "\n".join(full_output))
            else:
                messagebox.showwarning("Input Error", "Student ID and Name are required.")

    def borrow_book_from_library(self):
        selected_library = self._get_selected_library("Borrow Book")
        if not selected_library: return

        fields = [("Student ID (must be registered in library)", ""), ("Book Title", "")]
        dialog = InputDialog(self.root, f"Borrow Book from Library {selected_library.get_library_id()}", fields)
        if dialog.result:
            student_id = dialog.result.get("Student ID (must be registered in library)")
            title = dialog.result.get("Book Title")
            if student_id and title:
                output = capture_output(selected_library.borrow_book, student_id, title)
                messagebox.showinfo("Borrow Book", output.strip())
            else:
                messagebox.showwarning("Input Error", "Student ID and Book Title are required.")

    def return_book_to_library(self):
        selected_library = self._get_selected_library("Return Book")
        if not selected_library: return

        fields = [("Student ID", ""), ("Book Title", "")]
        dialog = InputDialog(self.root, f"Return Book to Library {selected_library.get_library_id()}", fields)
        if dialog.result:
            student_id = dialog.result.get("Student ID")
            title = dialog.result.get("Book Title")
            if student_id and title:
                output = capture_output(selected_library.return_book, student_id, title)
                messagebox.showinfo("Return Book", output.strip())
            else:
                messagebox.showwarning("Input Error", "Student ID and Book Title are required.")

    def search_book_in_library(self):
        selected_library = self._get_selected_library("Search Book")
        if not selected_library: return

        keyword = simpledialog.askstring("Search Book",
                                         f"Enter keyword for Library {selected_library.get_library_id()}:")
        if keyword:
            output = capture_output(selected_library.search_book, keyword)
            messagebox.showinfo("Search Results", output.strip() if output.strip() else "No matching books found.")

    def refresh_libraries_list_display(self):
        self.library_list_display.delete(0, tk.END)
        for lib in ums.libraries:
            self.library_list_display.insert(tk.END, f"Library ID: {lib.get_library_id()}")


if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityGUI(root)
    root.mainloop()
