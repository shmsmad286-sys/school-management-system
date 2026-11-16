import tkinter as tk
from tkinter import ttk, messagebox


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        self._grades = {}

    def add_grade(self, subject, grade):
        self._grades[subject] = grade

    def get_grades(self):
        return dict(self._grades)

    def average(self):
        if not self._grades:
            return 0
        return round(sum(self._grades.values()) / len(self._grades), 1)


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject


class School:
    def __init__(self, name):
        self.name = name
        self.students = []
        self.teachers = []

    def add_student(self, student):
        self.students.append(student)

    def find_student(self, student_id):
        for s in self.students:
            if s.student_id == student_id:
                return s
        return None

    def remove_student(self, student_id):
        self.students = [s for s in self.students if s.student_id != student_id]

    def add_teacher(self, teacher):
        self.teachers.append(teacher)


class App(tk.Tk):
    def __init__(self, school):
        super().__init__()
        self.school = school
        self.title(f"System Management {school.name}")
        self.geometry("720x480")

        tk.Label(self, text=f"🏫 {school.name}", font=("Arial", 18, "bold"),
                 bg="#2c3e50", fg="white", pady=10).pack(fill="x")

        tabs = ttk.Notebook(self)
        tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.students_tab = ttk.Frame(tabs)
        self.teachers_tab = ttk.Frame(tabs)
        self.grades_tab = ttk.Frame(tabs)
        tabs.add(self.students_tab, text="students")
        tabs.add(self.teachers_tab, text="teachers")
        tabs.add(self.grades_tab, text="grades")

        self.build_students_tab()
        self.build_teachers_tab()
        self.build_grades_tab()


    def make_entry(self, parent, label, col):
        ttk.Label(parent, text=label).grid(row=0, column=col * 2, padx=5, pady=8)
        entry = ttk.Entry(parent, width=14)
        entry.grid(row=0, column=col * 2 + 1, padx=5)
        return entry


    def build_students_tab(self):
        form = ttk.Frame(self.students_tab)
        form.pack(fill="x")
        self.s_name = self.make_entry(form, "name", 0)
        self.s_age = self.make_entry(form, "age", 1)
        self.s_id = self.make_entry(form, "student id", 2)

        btns = ttk.Frame(self.students_tab)
        btns.pack(fill="x")
        ttk.Button(btns, text="➕ add", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(btns, text="🗑 delete selected", command=self.delete_student).pack(side="left")

        self.s_table = ttk.Treeview(self.students_tab,
                                    columns=("id", "name", "age", "avg"),
                                    show="headings")
        for col, text in [("id", "student id"), ("name", "name"),
                          ("age", "age"), ("avg", "average")]:
            self.s_table.heading(col, text=text)
            self.s_table.column(col, width=130, anchor="center")
        self.s_table.pack(fill="both", expand=True, pady=10)

    def add_student(self):
        name, age, sid = self.s_name.get(), self.s_age.get(), self.s_id.get()
        if not name or not age.isdigit() or not sid:
            messagebox.showwarning("Important Notice", "Fill in all fields (Age number)")
            return
        if self.school.find_student(sid):
            messagebox.showwarning("Important Notice", "student id already exists")
            return
        self.school.add_student(Student(name, int(age), sid))
        for e in (self.s_name, self.s_age, self.s_id):
            e.delete(0, tk.END)
        self.refresh()

    def delete_student(self):
        selected = self.s_table.selection()
        if not selected:
            return
        sid = self.s_table.item(selected[0])["values"][0]
        self.school.remove_student(str(sid))
        self.refresh()


    def build_teachers_tab(self):
        form = ttk.Frame(self.teachers_tab)
        form.pack(fill="x")
        self.t_name = self.make_entry(form, "name", 0)
        self.t_age = self.make_entry(form, "age", 1)
        self.t_subject = self.make_entry(form, "subject", 2)
        ttk.Button(self.teachers_tab, text="➕ add",
                   command=self.add_teacher).pack(anchor="w", padx=5)

        self.t_table = ttk.Treeview(self.teachers_tab,
                                    columns=("name", "age", "subject"),
                                    show="headings")
        for col, text in [("name", "name"), ("age", "age"), ("subject", "subject")]:
            self.t_table.heading(col, text=text)
            self.t_table.column(col, width=150, anchor="center")
        self.t_table.pack(fill="both", expand=True, pady=10)

    def add_teacher(self):
        name, age, subject = self.t_name.get(), self.t_age.get(), self.t_subject.get()
        if not name or not age.isdigit() or not subject:
            messagebox.showwarning("Important Notice", "Fill in all fields (Age number)")
            return
        self.school.add_teacher(Teacher(name, int(age), subject))
        for e in (self.t_name, self.t_age, self.t_subject):
            e.delete(0, tk.END)
        self.refresh()


    def build_grades_tab(self):
        form = ttk.Frame(self.grades_tab)
        form.pack(fill="x")
        ttk.Label(form, text="student").grid(row=0, column=0, padx=5, pady=8)
        self.g_student = ttk.Combobox(form, state="readonly", width=22)
        self.g_student.grid(row=0, column=1, padx=5)
        self.g_student.bind("<<ComboboxSelected>>", lambda e: self.refresh_grades())
        self.g_subject = self.make_entry(form, "subject", 1)
        self.g_grade = self.make_entry(form, "grade", 2)
        ttk.Button(self.grades_tab, text="➕ add grade",
                   command=self.add_grade).pack(anchor="w", padx=5)

        self.g_table = ttk.Treeview(self.grades_tab, columns=("subject", "grade"),
                                    show="headings")
        self.g_table.heading("subject", text="subject")
        self.g_table.heading("grade", text="grade")
        self.g_table.pack(fill="both", expand=True, pady=10)

    def add_grade(self):
        value = self.g_student.get()
        if not value:
            messagebox.showwarning("Important Notice", "The first student chose")
            return
        student = self.school.find_student(value.split(" - ")[0])
        try:
            grade = float(self.g_grade.get())
        except ValueError:
            messagebox.showwarning("Important Notice", "The grade must be a number.")
            return
        if not self.g_subject.get():
            messagebox.showwarning("Important Notice", "Enter the name of the subject")
            return
        student.add_grade(self.g_subject.get(), grade)
        self.g_subject.delete(0, tk.END)
        self.g_grade.delete(0, tk.END)
        self.refresh()

    def refresh_grades(self):
        self.g_table.delete(*self.g_table.get_children())
        value = self.g_student.get()
        if not value:
            return
        student = self.school.find_student(value.split(" - ")[0])
        for subject, grade in student.get_grades().items():
            self.g_table.insert("", tk.END, values=(subject, grade))

  
    def refresh(self):
        self.s_table.delete(*self.s_table.get_children())
        for s in self.school.students:
            self.s_table.insert("", tk.END,
                                values=(s.student_id, s.name, s.age, s.average()))

        self.t_table.delete(*self.t_table.get_children())
        for t in self.school.teachers:
            self.t_table.insert("", tk.END, values=(t.name, t.age, t.subject))

        self.g_student["values"] = [f"{s.student_id} - {s.name}"
                                    for s in self.school.students]
        self.refresh_grades()


if __name__ == "__main__":
    App(School("WE School")).mainloop()