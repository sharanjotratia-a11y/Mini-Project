import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# -------------------------------
# DATABASE SETUP
# -------------------------------
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    StudentID INTEGER PRIMARY KEY,
    Name TEXT,
    Age INTEGER,
    Gender TEXT,
    Email TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Courses (
    CourseID INTEGER PRIMARY KEY,
    CourseName TEXT,
    Duration INTEGER
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Enrollments (
    EnrollmentID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    CourseID INTEGER,
    Grade TEXT,
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (CourseID) REFERENCES Courses(CourseID)
)
""")
conn.commit()

# -------------------------------
# GUI SETUP
# -------------------------------
root = tk.Tk()
root.title("🌟 Student Management System 🌟")
root.geometry("1000x600")
root.configure(bg="#f5f5f5")

# Style for Treeview
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#f0f0f0",
                foreground="black",
                rowheight=25,
                fieldbackground="#f0f0f0",
                font=("Arial", 10))
style.map('Treeview', background=[('selected', '#4CAF50')])
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="#ffffff", background="#4CAF50")

# Tabs
tab_control = ttk.Notebook(root)
students_tab = ttk.Frame(tab_control)
courses_tab = ttk.Frame(tab_control)
enrollments_tab = ttk.Frame(tab_control)

tab_control.add(students_tab, text='👨‍🎓 Students')
tab_control.add(courses_tab, text='📚 Courses')
tab_control.add(enrollments_tab, text='📝 Enrollments')
tab_control.pack(expand=1, fill='both')

# -------------------------------
# FUNCTIONS
# -------------------------------
def fetch_students():
    for row in students_tree.get_children():
        students_tree.delete(row)
    cursor.execute("SELECT * FROM Students")
    for row in cursor.fetchall():
        students_tree.insert("", "end", values=row)

def add_student():
    try:
        cursor.execute("INSERT INTO Students (StudentID, Name, Age, Gender, Email) VALUES (?, ?, ?, ?, ?)",
                       (int(student_id.get()), name.get(), int(age.get()), gender.get(), email.get()))
        conn.commit()
        fetch_students()
        messagebox.showinfo("Success", "Student added successfully!")
        # Clear input fields
        student_id.delete(0, tk.END)
        name.delete(0, tk.END)
        age.delete(0, tk.END)
        gender.delete(0, tk.END)
        email.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def fetch_courses():
    for row in courses_tree.get_children():
        courses_tree.delete(row)
    cursor.execute("SELECT * FROM Courses")
    for row in cursor.fetchall():
        courses_tree.insert("", "end", values=row)

def add_course():
    try:
        cursor.execute("INSERT INTO Courses (CourseID, CourseName, Duration) VALUES (?, ?, ?)",
                       (int(course_id.get()), course_name.get(), int(duration.get())))
        conn.commit()
        fetch_courses()
        messagebox.showinfo("Success", "Course added successfully!")
        # Clear input fields
        course_id.delete(0, tk.END)
        course_name.delete(0, tk.END)
        duration.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def fetch_enrollments():
    for row in enrollments_tree.get_children():
        enrollments_tree.delete(row)
    cursor.execute("""
        SELECT e.EnrollmentID, s.Name, c.CourseName, e.Grade
        FROM Enrollments e
        JOIN Students s ON e.StudentID = s.StudentID
        JOIN Courses c ON e.CourseID = c.CourseID
    """)
    for row in cursor.fetchall():
        enrollments_tree.insert("", "end", values=row)

def add_enrollment():
    try:
        cursor.execute("INSERT INTO Enrollments (EnrollmentID, StudentID, CourseID, Grade) VALUES (?, ?, ?, ?)",
                       (int(enroll_id.get()), int(student_sel.get()), int(course_sel.get()), grade.get()))
        conn.commit()
        fetch_enrollments()
        messagebox.showinfo("Success", "Enrollment added successfully!")
        # Clear input fields
        enroll_id.delete(0, tk.END)
        student_sel.delete(0, tk.END)
        course_sel.delete(0, tk.END)
        grade.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Button Hover Effect
def on_enter(e):
    e.widget['background'] = '#45a049'
def on_leave(e):
    e.widget['background'] = '#4CAF50'

# -------------------------------
# STUDENTS TAB
# -------------------------------
students_frame = tk.Frame(students_tab, bg="#e0f7fa", pady=10)
students_frame.pack(fill="x")

tk.Label(students_frame, text="ID", bg="#e0f7fa").grid(row=0, column=0, padx=5)
student_id = tk.Entry(students_frame, width=10)
student_id.grid(row=0, column=1, padx=5)

tk.Label(students_frame, text="Name", bg="#e0f7fa").grid(row=0, column=2, padx=5)
name = tk.Entry(students_frame, width=20)
name.grid(row=0, column=3, padx=5)

tk.Label(students_frame, text="Age", bg="#e0f7fa").grid(row=0, column=4, padx=5)
age = tk.Entry(students_frame, width=5)
age.grid(row=0, column=5, padx=5)

tk.Label(students_frame, text="Gender", bg="#e0f7fa").grid(row=0, column=6, padx=5)
gender = tk.Entry(students_frame, width=10)
gender.grid(row=0, column=7, padx=5)

tk.Label(students_frame, text="Email", bg="#e0f7fa").grid(row=0, column=8, padx=5)
email = tk.Entry(students_frame, width=20)
email.grid(row=0, column=9, padx=5)

add_stu_btn = tk.Button(students_frame, text="Add Student", bg="#4CAF50", fg="white", command=add_student)
add_stu_btn.grid(row=0, column=10, padx=10)
add_stu_btn.bind("<Enter>", on_enter)
add_stu_btn.bind("<Leave>", on_leave)

students_tree = ttk.Treeview(students_tab, columns=("ID","Name","Age","Gender","Email"), show="headings")
for col in ("ID","Name","Age","Gender","Email"):
    students_tree.heading(col, text=col)
students_tree.pack(fill="both", expand=True, pady=10, padx=10)
fetch_students()

# -------------------------------
# COURSES TAB
# -------------------------------
courses_frame = tk.Frame(courses_tab, bg="#fff3e0", pady=10)
courses_frame.pack(fill="x")

tk.Label(courses_frame, text="Course ID", bg="#fff3e0").grid(row=0, column=0, padx=5)
course_id = tk.Entry(courses_frame, width=10)
course_id.grid(row=0, column=1, padx=5)

tk.Label(courses_frame, text="Course Name", bg="#fff3e0").grid(row=0, column=2, padx=5)
course_name = tk.Entry(courses_frame, width=20)
course_name.grid(row=0, column=3, padx=5)

tk.Label(courses_frame, text="Duration", bg="#fff3e0").grid(row=0, column=4, padx=5)
duration = tk.Entry(courses_frame, width=10)
duration.grid(row=0, column=5, padx=5)

add_course_btn = tk.Button(courses_frame, text="Add Course", bg="#FF9800", fg="white", command=add_course)
add_course_btn.grid(row=0, column=6, padx=10)
add_course_btn.bind("<Enter>", lambda e: add_course_btn.config(bg="#fb8c00"))
add_course_btn.bind("<Leave>", lambda e: add_course_btn.config(bg="#FF9800"))

courses_tree = ttk.Treeview(courses_tab, columns=("ID","CourseName","Duration"), show="headings")
for col in ("ID","CourseName","Duration"):
    courses_tree.heading(col, text=col)
courses_tree.pack(fill="both", expand=True, pady=10, padx=10)
fetch_courses()

# -------------------------------
# ENROLLMENTS TAB
# -------------------------------
enroll_frame = tk.Frame(enrollments_tab, bg="#e8f5e9", pady=10)
enroll_frame.pack(fill="x")

tk.Label(enroll_frame, text="Enrollment ID", bg="#e8f5e9").grid(row=0, column=0, padx=5)
enroll_id = tk.Entry(enroll_frame, width=10)
enroll_id.grid(row=0, column=1, padx=5)

tk.Label(enroll_frame, text="Student ID", bg="#e8f5e9").grid(row=0, column=2, padx=5)
student_sel = tk.Entry(enroll_frame, width=10)
student_sel.grid(row=0, column=3, padx=5)

tk.Label(enroll_frame, text="Course ID", bg="#e8f5e9").grid(row=0, column=4, padx=5)
course_sel = tk.Entry(enroll_frame, width=10)
course_sel.grid(row=0, column=5, padx=5)

tk.Label(enroll_frame, text="Grade", bg="#e8f5e9").grid(row=0, column=6, padx=5)
grade = tk.Entry(enroll_frame, width=5)
grade.grid(row=0, column=7, padx=5)

add_enroll_btn = tk.Button(enroll_frame, text="Add Enrollment", bg="#2196F3", fg="white", command=add_enrollment)
add_enroll_btn.grid(row=0, column=8, padx=10)
add_enroll_btn.bind("<Enter>", lambda e: add_enroll_btn.config(bg="#1976D2"))
add_enroll_btn.bind("<Leave>", lambda e: add_enroll_btn.config(bg="#2196F3"))

enrollments_tree = ttk.Treeview(enrollments_tab, columns=("EnrollmentID","Student","Course","Grade"), show="headings")
for col in ("EnrollmentID","Student","Course","Grade"):
    enrollments_tree.heading(col, text=col)
enrollments_tree.pack(fill="both", expand=True, pady=10, padx=10)
fetch_enrollments()

# -------------------------------
# RUN APP
# -------------------------------
root.mainloop()
