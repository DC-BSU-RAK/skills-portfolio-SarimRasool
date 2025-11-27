import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os


class Student:
    """Class to represent a student and their marks."""
    
    def __init__(self, student_code, name, course1, course2, course3, exam):
        self.student_code = student_code
        self.name = name
        self.course1 = int(course1)
        self.course2 = int(course2)
        self.course3 = int(course3)
        self.exam = int(exam)
    
    def get_total_coursework(self):
        """Calculate total coursework marks (out of 60)."""
        return self.course1 + self.course2 + self.course3
    
    def get_overall_percentage(self):
        """Calculate overall percentage (coursework + exam out of 160)."""
        total = self.get_total_coursework() + self.exam
        return (total / 160) * 100
    
    def get_grade(self):
        """Determine grade based on overall percentage."""
        percentage = self.get_overall_percentage()
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def get_formatted_record(self):
        """Return formatted string of student record."""
        return (f"Student Name: {self.name}\n"
                f"Student Number: {self.student_code}\n"
                f"Total Coursework Mark: {self.get_total_coursework()} / 60\n"
                f"Exam Mark: {self.exam} / 100\n"
                f"Overall Percentage: {self.get_overall_percentage():.2f}%\n"
                f"Grade: {self.get_grade()}\n")


class StudentMarksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management System")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.root.config(bg="#f5f5f5")
        
        self.students = []
        self.load_student_data()
        self.create_widgets()
    
    def load_student_data(self):
        """Load student data from studentMarks.txt file."""
        try:
            # Try to load from resources folder
            file_path = os.path.join("resources", "studentMarks.txt")
            
            # If resources folder doesn't exist, try current directory
            if not os.path.exists(file_path):
                file_path = "studentMarks.txt"
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                if not lines:
                    raise ValueError("File is empty")
                
                # First line is the number of students
                num_students = int(lines[0].strip())
                
                # Read each student's data
                for i in range(1, num_students + 1):
                    if i < len(lines):
                        line = lines[i].strip()
                        parts = line.split(',')
                        
                        if len(parts) >= 6:
                            student_code = parts[0].strip()
                            name = parts[1].strip()
                            course1 = parts[2].strip()
                            course2 = parts[3].strip()
                            course3 = parts[4].strip()
                            exam = parts[5].strip()
                            
                            student = Student(student_code, name, course1, course2, course3, exam)
                            self.students.append(student)
            
            if not self.students:
                self.add_sample_data()
                
        except FileNotFoundError:
            messagebox.showwarning(
                "File Not Found",
                "studentMarks.txt file not found. Using sample data."
            )
            self.add_sample_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading file: {str(e)}\nUsing sample data.")
            self.add_sample_data()
    
    def add_sample_data(self):
        """Add sample student data if file is not found."""
        sample_data = [
            ("101345", "John Curry", "8", "15", "7", "45"),
            ("2345", "Sam Sturtivant", "14", "15", "14", "77"),
            ("9876", "Lee Scott", "17", "11", "16", "99"),
            ("3724", "Matt Thompson", "19", "11", "15", "81"),
            ("1212", "Ron Herrema", "14", "17", "18", "66"),
            ("8439", "Jake Hobbs", "10", "11", "10", "43"),
            ("2344", "Jo Hyde", "6", "15", "10", "55"),
            ("9384", "Gareth Southgate", "5", "6", "8", "33"),
            ("8327", "Alan Shearer", "20", "20", "20", "100"),
            ("2983", "Les Ferdinand", "15", "17", "18", "92"),
        ]
        
        for data in sample_data:
            student = Student(*data)
            self.students.append(student)
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", pady=15)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="📚 Student Marks Management System 📚",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack()
        
        # Info label
        info_label = tk.Label(
            self.root,
            text=f"Total Students: {len(self.students)}",
            font=("Arial", 12),
            bg="#f5f5f5",
            fg="#34495e"
        )
        info_label.pack(pady=10)
        
        # Menu buttons frame
        menu_frame = tk.Frame(self.root, bg="#f5f5f5")
        menu_frame.pack(pady=20)
        
        # Button 1 - View all students
        btn1 = tk.Button(
            menu_frame,
            text="1. View All Student Records",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=30,
            height=2,
            command=self.view_all_students,
            cursor="hand2"
        )
        btn1.grid(row=0, column=0, padx=10, pady=10)
        
        # Button 2 - View individual student
        btn2 = tk.Button(
            menu_frame,
            text="2. View Individual Student Record",
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            width=30,
            height=2,
            command=self.view_individual_student,
            cursor="hand2"
        )
        btn2.grid(row=0, column=1, padx=10, pady=10)
        
        # Button 3 - Highest score
        btn3 = tk.Button(
            menu_frame,
            text="3. Show Student with Highest Score",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=30,
            height=2,
            command=self.show_highest_score,
            cursor="hand2"
        )
        btn3.grid(row=1, column=0, padx=10, pady=10)
        
        # Button 4 - Lowest score
        btn4 = tk.Button(
            menu_frame,
            text="4. Show Student with Lowest Score",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            width=30,
            height=2,
            command=self.show_lowest_score,
            cursor="hand2"
        )
        btn4.grid(row=1, column=1, padx=10, pady=10)
        
        # Output part
        output_frame = tk.LabelFrame(
            self.root,
            text="Results",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50",
            padx=10,
            pady=10
        )
        output_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Scrolled text widget for output
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            font=("Courier", 10),
            bg="#ffffff",
            fg="#2c3e50",
            wrap=tk.WORD,
            height=15
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Quit button
        quit_btn = tk.Button(
            self.root,
            text="Quit",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            width=15,
            command=self.root.quit,
            cursor="hand2"
        )
        quit_btn.pack(pady=10)
    
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)
    
    def display_output(self, text):
        """Display text in the output area."""
        self.clear_output()
        self.output_text.insert(tk.END, text)
    
    def view_all_students(self):
        """Display all student records."""
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        
        output = "=" * 80 + "\n"
        output += "ALL STUDENT RECORDS\n"
        output += "=" * 80 + "\n\n"
        
        total_percentage = 0
        
        for i, student in enumerate(self.students, 1):
            output += f"STUDENT {i}:\n"
            output += "-" * 80 + "\n"
            output += student.get_formatted_record()
            output += "\n"
            total_percentage += student.get_overall_percentage()
        
        # Summary
        average_percentage = total_percentage / len(self.students)
        output += "=" * 80 + "\n"
        output += "SUMMARY\n"
        output += "=" * 80 + "\n"
        output += f"Number of Students: {len(self.students)}\n"
        output += f"Average Percentage Mark: {average_percentage:.2f}%\n"
        
        self.display_output(output)
    
    def view_individual_student(self):
        """Allow user to select and view an individual student's record."""
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        
        # Create a new window for student selection
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Student")
        select_window.geometry("400x500")
        select_window.config(bg="#f5f5f5")
        
        # Title
        title_label = tk.Label(
            select_window,
            text="Select a Student",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            fg="#2c3e50"
        )
        title_label.pack(pady=20)
        
        # Search frame
        search_frame = tk.Frame(select_window, bg="#f5f5f5")
        search_frame.pack(pady=10)
        
        tk.Label(
            search_frame,
            text="Search:",
            font=("Arial", 11),
            bg="#f5f5f5"
        ).pack(side=tk.LEFT, padx=5)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=search_var,
            font=("Arial", 11),
            width=25
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Listbox with students
        listbox_frame = tk.Frame(select_window, bg="#f5f5f5")
        listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        student_listbox = tk.Listbox(
            listbox_frame,
            font=("Courier", 10),
            yscrollcommand=scrollbar.set,
            height=15
        )
        student_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=student_listbox.yview)
        
        # Populate listbox
        def populate_listbox(filter_text=""):
            student_listbox.delete(0, tk.END)
            for student in self.students:
                display_text = f"{student.student_code} - {student.name}"
                if filter_text.lower() in display_text.lower():
                    student_listbox.insert(tk.END, display_text)
        
        populate_listbox()
        
        # Search functionality
        def on_search(*args):
            populate_listbox(search_var.get())
        
        search_var.trace('w', on_search)
        
        # Select button
        def on_select():
            selection = student_listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a student.")
                return
            
            selected_text = student_listbox.get(selection[0])
            student_code = selected_text.split(' - ')[0]
            
            # Find the student
            selected_student = None
            for student in self.students:
                if student.student_code == student_code:
                    selected_student = student
                    break
            
            if selected_student:
                output = "=" * 80 + "\n"
                output += "INDIVIDUAL STUDENT RECORD\n"
                output += "=" * 80 + "\n\n"
                output += selected_student.get_formatted_record()
                self.display_output(output)
                select_window.destroy()
        
        select_btn = tk.Button(
            select_window,
            text="View Selected Student",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            command=on_select,
            cursor="hand2"
        )
        select_btn.pack(pady=10)
    
    def show_highest_score(self):
        """Display the student with the highest overall mark."""
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        
        highest_student = max(self.students, key=lambda s: s.get_overall_percentage())
        
        output = "=" * 80 + "\n"
        output += "STUDENT WITH HIGHEST OVERALL MARK\n"
        output += "=" * 80 + "\n\n"
        output += highest_student.get_formatted_record()
        
        self.display_output(output)
    
    def show_lowest_score(self):
        """Display the student with the lowest overall mark."""
        if not self.students:
            messagebox.showinfo("No Data", "No student records available.")
            return
        
        lowest_student = min(self.students, key=lambda s: s.get_overall_percentage())
        
        output = "=" * 80 + "\n"
        output += "STUDENT WITH LOWEST OVERALL MARK\n"
        output += "=" * 80 + "\n\n"
        output += lowest_student.get_formatted_record()
        
        self.display_output(output)


def main():
    root = tk.Tk()
    app = StudentMarksApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()