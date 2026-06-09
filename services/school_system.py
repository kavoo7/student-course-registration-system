import os

from models.student import Student
from models.course import Course


DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
COURSES_FILE = os.path.join(DATA_DIR, "courses.txt")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.txt")


class SchoolSystem:
    def __init__(self):
        self.students = []
        self.courses = []
        self.registrations = []  # list of {"student_id": ..., "course_id": ...}

    # ─────────────────────────────────────────
    # INPUT HELPERS
    # ─────────────────────────────────────────

    def _prompt(self, label):
        """Read a non-empty string from the user."""
        while True:
            value = input(f"  {label}: ").strip()
            if value:
                return value
            print(f"  ⚠  {label} cannot be empty. Please try again.")

    def _prompt_int(self, label, minimum=1):
        """Read an integer >= minimum from the user."""
        while True:
            raw = input(f"  {label}: ").strip()
            if raw.isdigit() and int(raw) >= minimum:
                return int(raw)
            print(f"  ⚠  Please enter a whole number greater than or equal to {minimum}.")

    def _prompt_email(self, label="Email"):
        """Read an email that contains @."""
        while True:
            value = input(f"  {label}: ").strip()
            if value and "@" in value:
                return value
            print("  ⚠  Please enter a valid email address (must contain @).")

    # ─────────────────────────────────────────
    # STUDENT MANAGEMENT
    # ─────────────────────────────────────────

    def add_student(self):
        print("\n  ── Add New Student ──")
        student_id = self._prompt("Student ID").upper()

        if self._find_student_by_id(student_id):
            print(f"\n  ✖  A student with ID '{student_id}' already exists.")
            return

        name = self._prompt("Name")
        email = self._prompt_email()
        phone = self._prompt("Phone Number")

        student = Student(student_id, name, email, phone)
        self.students.append(student)
        print(f"\n  ✔  Student '{name}' added successfully.")

    def view_students(self):
        print("\n  ── All Students ──")
        if not self.students:
            print("  No students found.")
            return
        for i, student in enumerate(self.students, start=1):
            print(f"\n  [{i}]")
            student.display()

    def search_student(self):
        print("\n  ── Search Student ──")
        keyword = self._prompt("Enter Student ID or Name").lower()

        results = [
            s for s in self.students
            if keyword in s.student_id.lower() or keyword in s.name.lower()
        ]

        if not results:
            print("  No matching students found.")
            return

        print(f"\n  Found {len(results)} result(s):")
        for student in results:
            print()
            student.display()

    def _find_student_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    # ─────────────────────────────────────────
    # COURSE MANAGEMENT
    # ─────────────────────────────────────────

    def add_course(self):
        print("\n  ── Add New Course ──")
        course_id = self._prompt("Course ID").upper()

        if self._find_course_by_id(course_id):
            print(f"\n  ✖  A course with ID '{course_id}' already exists.")
            return

        course_name = self._prompt("Course Name")
        trainer = self._prompt("Trainer Name")
        capacity = self._prompt_int("Capacity", minimum=1)

        course = Course(course_id, course_name, trainer, capacity)
        self.courses.append(course)
        print(f"\n  ✔  Course '{course_name}' added successfully.")

    def view_courses(self):
        print("\n  ── All Courses ──")
        if not self.courses:
            print("  No courses found.")
            return
        for i, course in enumerate(self.courses, start=1):
            enrolled = self._enrolled_count(course.course_id)
            print(f"\n  [{i}]")
            course.display()
            print(f"  Enrolled    : {enrolled}/{course.capacity}")

    def _find_course_by_id(self, course_id):
        for course in self.courses:
            if course.course_id == course_id:
                return course
        return None

    def _enrolled_count(self, course_id):
        return sum(1 for r in self.registrations if r["course_id"] == course_id)

    # ─────────────────────────────────────────
    # REGISTRATION MANAGEMENT
    # ─────────────────────────────────────────

    def register_student(self):
        print("\n  ── Register Student to Course ──")

        if not self.students:
            print("  No students available. Please add a student first.")
            return
        if not self.courses:
            print("  No courses available. Please add a course first.")
            return

        student_id = self._prompt("Student ID").upper()
        student = self._find_student_by_id(student_id)
        if not student:
            print(f"\n  ✖  No student found with ID '{student_id}'.")
            return

        course_id = self._prompt("Course ID").upper()
        course = self._find_course_by_id(course_id)
        if not course:
            print(f"\n  ✖  No course found with ID '{course_id}'.")
            return

        # Duplicate check
        already_registered = any(
            r["student_id"] == student_id and r["course_id"] == course_id
            for r in self.registrations
        )
        if already_registered:
            print(f"\n  ✖  {student.name} is already registered for this course.")
            return

        # Capacity check
        if self._enrolled_count(course_id) >= course.capacity:
            print("\n  ✖  Registration failed. This course is already full.")
            return

        self.registrations.append({"student_id": student_id, "course_id": course_id})
        print(f"\n  ✔  {student.name} successfully registered for {course.course_name}.")

    def view_students_in_course(self):
        print("\n  ── Students in a Course ──")

        if not self.courses:
            print("  No courses available.")
            return

        course_id = self._prompt("Course ID").upper()
        course = self._find_course_by_id(course_id)
        if not course:
            print(f"\n  ✖  No course found with ID '{course_id}'.")
            return

        enrolled_ids = [
            r["student_id"] for r in self.registrations if r["course_id"] == course_id
        ]
        enrolled_students = [s for s in self.students if s.student_id in enrolled_ids]

        print(f"\n  Course : {course.course_name} ({course_id})")
        print(f"  Enrolled: {len(enrolled_students)}/{course.capacity}")

        if not enrolled_students:
            print("  No students registered in this course yet.")
            return

        for i, student in enumerate(enrolled_students, start=1):
            print(f"\n  [{i}]")
            student.display()

    def view_courses_for_student(self):
        print("\n  ── Courses for a Student ──")

        if not self.students:
            print("  No students available.")
            return

        student_id = self._prompt("Student ID").upper()
        student = self._find_student_by_id(student_id)
        if not student:
            print(f"\n  ✖  No student found with ID '{student_id}'.")
            return

        registered_ids = [
            r["course_id"] for r in self.registrations if r["student_id"] == student_id
        ]
        registered_courses = [c for c in self.courses if c.course_id in registered_ids]

        print(f"\n  Student : {student.name} ({student_id})")

        if not registered_courses:
            print("  This student has not registered for any courses yet.")
            return

        for i, course in enumerate(registered_courses, start=1):
            print(f"\n  [{i}]")
            course.display()

    # ─────────────────────────────────────────
    # FILE HANDLING
    # ─────────────────────────────────────────

    def save_data(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        try:
            # Save students — one student per line: id,name,email,phone
            with open(STUDENTS_FILE, "w") as f:
                for s in self.students:
                    f.write(f"{s.student_id},{s.name},{s.email},{s.phone_number}\n")

            # Save courses — one course per line: id,name,trainer,capacity
            with open(COURSES_FILE, "w") as f:
                for c in self.courses:
                    f.write(f"{c.course_id},{c.course_name},{c.trainer},{c.capacity}\n")

            # Save registrations — one registration per line: student_id,course_id
            with open(REGISTRATIONS_FILE, "w") as f:
                for r in self.registrations:
                    f.write(f"{r['student_id']},{r['course_id']}\n")

            print("\n  ✔  Data saved successfully.")
        except Exception as e:
            print(f"\n  ✖  Failed to save data: {e}")

    def load_data(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        try:
            # Load students
            if os.path.exists(STUDENTS_FILE):
                with open(STUDENTS_FILE, "r") as f:
                    self.students = []
                    for line in f:
                        line = line.strip()
                        if line:  # skip empty lines
                            student_id, name, email, phone = line.split(",", 3)
                            self.students.append(Student(student_id, name, email, phone))

            # Load courses
            if os.path.exists(COURSES_FILE):
                with open(COURSES_FILE, "r") as f:
                    self.courses = []
                    for line in f:
                        line = line.strip()
                        if line:
                            course_id, course_name, trainer, capacity = line.split(",", 3)
                            self.courses.append(Course(course_id, course_name, trainer, int(capacity)))

            # Load registrations
            if os.path.exists(REGISTRATIONS_FILE):
                with open(REGISTRATIONS_FILE, "r") as f:
                    self.registrations = []
                    for line in f:
                        line = line.strip()
                        if line:
                            student_id, course_id = line.split(",", 1)
                            self.registrations.append({"student_id": student_id, "course_id": course_id})

            if self.students or self.courses:
                print(
                    f"  ✔  Loaded {len(self.students)} student(s) and "
                    f"{len(self.courses)} course(s) from saved data."
                )
        except Exception as e:
            print(f"  ⚠  Could not load saved data: {e}")
