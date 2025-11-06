import tkinter as tk
from tkinter import messagebox
import random


class ArithmeticQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Quiz state variables
        self.difficulty = None
        self.score = 0
        self.question_count = 0
        self.current_num1 = 0
        self.current_num2 = 0
        self.current_operation = ''
        self.current_answer = 0
        self.attempt = 1  # Track if this is first or second attempt
        
        # Start with the menu
        self.displayMenu()
    
    def displayMenu(self):
        """Display the difficulty level menu at the beginning of the quiz."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(
            self.root,
            text="ARITHMETIC QUIZ",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=30)
        
        # Instructions
        instruction_label = tk.Label(
            self.root,
            text="DIFFICULTY LEVEL",
            font=("Arial", 16, "bold"),
            fg="#34495e"
        )
        instruction_label.pack(pady=10)
        
        # Difficulty buttons
        easy_btn = tk.Button(
            self.root,
            text="1. Easy (Single Digit)",
            font=("Arial", 14),
            width=25,
            bg="#2ecc71",
            fg="white",
            command=lambda: self.startQuiz(1)
        )
        easy_btn.pack(pady=10)
        
        moderate_btn = tk.Button(
            self.root,
            text="2. Moderate (Double Digit)",
            font=("Arial", 14),
            width=25,
            bg="#f39c12",
            fg="white",
            command=lambda: self.startQuiz(2)
        )
        moderate_btn.pack(pady=10)
        
        advanced_btn = tk.Button(
            self.root,
            text="3. Advanced (4-Digit)",
            font=("Arial", 14),
            width=25,
            bg="#e74c3c",
            fg="white",
            command=lambda: self.startQuiz(3)
        )
        advanced_btn.pack(pady=10)
    
    def randomInt(self, difficulty):
        """Generate random integers based on difficulty level.
        Returns a tuple of (min_value, max_value) for the given difficulty."""
        if difficulty == 1:  # Easy: single digit
            return random.randint(0, 9), random.randint(0, 9)
        elif difficulty == 2:  # Moderate: double digit
            return random.randint(10, 99), random.randint(10, 99)
        else:  # Advanced: 4-digit
            return random.randint(1000, 9999), random.randint(1000, 9999)
    
    def decideOperation(self):
        """Randomly decide whether the problem is addition or subtraction.
        Returns '+' or '-'."""
        return random.choice(['+', '-'])
    
    def startQuiz(self, difficulty):
        """Initialize quiz variables and start the quiz."""
        self.difficulty = difficulty
        self.score = 0
        self.question_count = 0
        self.displayProblem()
    
    def displayProblem(self):
        """Display the question to the user and accept their answer."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Check if quiz is complete
        if self.question_count >= 10:
            self.displayResults()
            return
        
        # Generate new problem
        self.current_num1, self.current_num2 = self.randomInt(self.difficulty)
        self.current_operation = self.decideOperation()
        
        if self.current_operation == '+':
            self.current_answer = self.current_num1 + self.current_num2
        else:
            self.current_answer = self.current_num1 - self.current_num2
        
        # Question counter
        counter_label = tk.Label(
            self.root,
            text=f"Question {self.question_count + 1} of 10",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        counter_label.pack(pady=10)
        
        # Score display
        score_label = tk.Label(
            self.root,
            text=f"Score: {self.score} / 100",
            font=("Arial", 12, "bold"),
            fg="#2980b9"
        )
        score_label.pack(pady=5)
        
        # Problem display
        problem_frame = tk.Frame(self.root, bg="#ecf0f1", padx=20, pady=20)
        problem_frame.pack(pady=30)
        
        problem_label = tk.Label(
            problem_frame,
            text=f"{self.current_num1} {self.current_operation} {self.current_num2} =",
            font=("Courier", 28, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        problem_label.pack()
        
        # Answer entry
        self.answer_entry = tk.Entry(
            self.root,
            font=("Arial", 18),
            width=15,
            justify="center"
        )
        self.answer_entry.pack(pady=10)
        self.answer_entry.focus()
        
        # Bind Enter key to submit
        self.answer_entry.bind('<Return>', lambda e: self.checkAnswer())
        
        # Submit button
        submit_btn = tk.Button(
            self.root,
            text="Submit Answer",
            font=("Arial", 14),
            bg="#3498db",
            fg="white",
            width=15,
            command=self.checkAnswer
        )
        submit_btn.pack(pady=10)
        
        # Reset attempt counter for new question
        self.attempt = 1
    
    def checkAnswer(self):
        """Check if the user's answer is correct and provide feedback."""
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number!")
            self.answer_entry.delete(0, tk.END)
            return
        
        self.isCorrect(user_answer)
    
    def isCorrect(self, user_answer):
        """Check whether the user's answer was correct and output appropriate message."""
        if user_answer == self.current_answer:
            # Correct answer
            if self.attempt == 1:
                points = 10
                message = "Excellent! Correct on first try! (+10 points)"
            else:
                points = 5
                message = "Correct! Good job on the second try! (+5 points)"
            
            self.score += points
            messagebox.showinfo("Correct! ✓", message)
            self.question_count += 1
            self.displayProblem()
        else:
            # Wrong answer
            if self.attempt == 1:
                # Give second chance
                self.attempt = 2
                messagebox.showwarning(
                    "Incorrect ✗",
                    "That's not correct. Try again!\nYou have one more attempt."
                )
                self.answer_entry.delete(0, tk.END)
                self.answer_entry.focus()
            else:
                # Second attempt failed
                messagebox.showerror(
                    "Incorrect ✗",
                    f"Sorry, that's incorrect.\nThe correct answer was {self.current_answer}."
                )
                self.question_count += 1
                self.displayProblem()
    
    def displayResults(self):
        """Output the user's final score and ranking."""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Calculate grade
        if self.score >= 90:
            grade = "A+"
            color = "#27ae60"
        elif self.score >= 80:
            grade = "A"
            color = "#2ecc71"
        elif self.score >= 70:
            grade = "B"
            color = "#3498db"
        elif self.score >= 60:
            grade = "C"
            color = "#f39c12"
        else:
            grade = "D"
            color = "#e74c3c"
        
        # Results display
        title_label = tk.Label(
            self.root,
            text="QUIZ COMPLETE!",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=30)
        
        score_frame = tk.Frame(self.root, bg="#ecf0f1", padx=40, pady=30)
        score_frame.pack(pady=20)
        
        score_label = tk.Label(
            score_frame,
            text=f"Your Score: {self.score} / 100",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        )
        score_label.pack()
        
        grade_label = tk.Label(
            score_frame,
            text=f"Grade: {grade}",
            font=("Arial", 28, "bold"),
            bg="#ecf0f1",
            fg=color
        )
        grade_label.pack(pady=10)
        
        # Play again button
        play_again_btn = tk.Button(
            self.root,
            text="Play Again",
            font=("Arial", 14),
            bg="#3498db",
            fg="white",
            width=15,
            command=self.displayMenu
        )
        play_again_btn.pack(pady=10)
        
        # Exit button
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=("Arial", 14),
            bg="#95a5a6",
            fg="white",
            width=15,
            command=self.root.quit
        )
        exit_btn.pack(pady=5)


def main():
    root = tk.Tk()
    app = ArithmeticQuiz(root)
    root.mainloop()


if __name__ == "__main__":
    main()