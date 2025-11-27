import tkinter as tk
from tkinter import messagebox
import random
import os


class JokeTellerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke Telling Assistant")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f0f0")
        
        # Joke data
        self.jokes = []
        self.current_joke = None
        self.punchline_shown = False
        
        # Load jokes from the file
        self.load_jokes()
        
        # Create UI
        self.create_widgets()
    
    def load_jokes(self):
        """Load jokes from the randomJokes.txt file."""
        try:
            # Try to load from resources folder
            file_path = os.path.join("resources", "randomJokes.txt")
            
            # If resources folder doesn't exist, try current directory
            if not os.path.exists(file_path):
                file_path = "randomJokes.txt"
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
                for line in lines:
                    line = line.strip()
                    # Skip empty lines
                    if not line:
                        continue
                    
                    # Remove leading dash if present
                    if line.startswith('-'):
                        line = line[1:].strip()
                    
                    # Split by question mark to separate setup and punchline
                    if '?' in line:
                        parts = line.split('?', 1)
                        setup = parts[0].strip() + '?'
                        punchline = parts[1].strip()
                        self.jokes.append({'setup': setup, 'punchline': punchline})
            
            if not self.jokes:
                # If no jokes loaded, add some default jokes
                self.add_default_jokes()
                
        except FileNotFoundError:
            messagebox.showwarning(
                "File Not Found",
                "randomJokes.txt file not found. Using default jokes."
            )
            self.add_default_jokes()
    
    def add_default_jokes(self):
        """Add default jokes if file is not found."""
        self.jokes = [
            {
                'setup': 'Why did the chicken cross the road?',
                'punchline': 'To get to the other side.'
            },
            {
                'setup': 'What happens if you boil a clown?',
                'punchline': 'You get a laughing stock.'
            },
            {
                'setup': 'Why don\'t scientists trust atoms?',
                'punchline': 'Because they make up everything.'
            },
            {
                'setup': 'What do you call a bear with no teeth?',
                'punchline': 'A gummy bear.'
            },
            {
                'setup': 'Why did the scarecrow win an award?',
                'punchline': 'He was outstanding in his field.'
            },
            {
                'setup': 'What do you call fake spaghetti?',
                'punchline': 'An impasta!'
            }
        ]
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Title
        title_label = tk.Label(
            self.root,
            text="🎭 Joke Telling Assistant 🎭",
            font=("Arial", 22, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=30)
        
        # Alexa image/icon placeholder
        alexa_label = tk.Label(
            self.root,
            text="🤖",
            font=("Arial", 48),
            bg="#f0f0f0"
        )
        alexa_label.pack(pady=10)
        
        # Main button - Alexa tell me a joke
        self.alexa_button = tk.Button(
            self.root,
            text="Alexa, tell me a Joke",
            font=("Arial", 16, "bold"),
            bg="#3498db",
            fg="white",
            width=25,
            height=2,
            command=self.tell_joke,
            cursor="hand2"
        )
        self.alexa_button.pack(pady=20)
        
        # Frame for joke display
        self.joke_frame = tk.Frame(self.root, bg="#ffffff", relief=tk.RAISED, bd=2)
        self.joke_frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Setup label (initially hidden)
        self.setup_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Arial", 14, "italic"),
            bg="#ffffff",
            fg="#2c3e50",
            wraplength=500,
            justify=tk.LEFT,
            pady=20
        )
        self.setup_label.pack()
        
        # Punchline label (initially hidden)
        self.punchline_label = tk.Label(
            self.joke_frame,
            text="",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="#e74c3c",
            wraplength=500,
            justify=tk.LEFT,
            pady=10
        )
        self.punchline_label.pack()
        
        # Button frame
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        
        # Show Punchline button (initially hidden)
        self.punchline_button = tk.Button(
            button_frame,
            text="Show Punchline",
            font=("Arial", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.show_punchline,
            cursor="hand2"
        )
        self.punchline_button.pack(side=tk.LEFT, padx=5)
        self.punchline_button.pack_forget()  # Hide initially
        
        # Next Joke button (initially hidden)
        self.next_button = tk.Button(
            button_frame,
            text="Next Joke",
            font=("Arial", 12, "bold"),
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.next_joke,
            cursor="hand2"
        )
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack_forget()  # Hide initially
        
        # Quit button
        quit_button = tk.Button(
            self.root,
            text="Quit",
            font=("Arial", 12),
            bg="#95a5a6",
            fg="white",
            width=15,
            command=self.root.quit,
            cursor="hand2"
        )
        quit_button.pack(pady=10)
    
    def tell_joke(self):
        """Select and display a random joke setup."""
        if not self.jokes:
            messagebox.showerror("Error", "No jokes available!")
            return
        
        # Select random joke
        self.current_joke = random.choice(self.jokes)
        self.punchline_shown = False
        
        # Display setup
        self.setup_label.config(text=self.current_joke['setup'])
        self.punchline_label.config(text="")
        
        # Show punchline button, hide Next Joke button
        self.punchline_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack_forget()
        
        # Hide the Alexa button after first joke
        self.alexa_button.pack_forget()
    
    def show_punchline(self):
        """Display the punchline of the current joke."""
        if self.current_joke and not self.punchline_shown:
            self.punchline_label.config(text=self.current_joke['punchline'])
            self.punchline_shown = True
            
            # Hide punchline button, show Next Joke button
            self.punchline_button.pack_forget()
            self.next_button.pack(side=tk.LEFT, padx=5)
    
    def next_joke(self):
        """Request another random joke."""
        self.tell_joke()


def main():
    root = tk.Tk()
    app = JokeTellerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()