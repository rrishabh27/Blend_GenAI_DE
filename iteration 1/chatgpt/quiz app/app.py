import tkinter as tk
from tkinter import messagebox
from random import sample
from datetime import datetime
import json
import uuid  # for generating unique IDs


questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Rome"],
        "correct_answer": "Paris"
    },
    # Add more questions here...
]
# Additional questions
additional_questions1 = [
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Jupiter", "Mars", "Saturn", "Earth"],
        "correct_answer": "Jupiter"
    },
    {
        "question": "Which country is known as the Land of the Rising Sun?",
        "options": ["China", "Japan", "Korea", "Vietnam"],
        "correct_answer": "Japan"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
        "correct_answer": "Leonardo da Vinci"
    },
    {
        "question": "Which ocean is the largest?",
        "options": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
        "correct_answer": "Pacific Ocean"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "options": ["Mark Twain", "Harper Lee", "Charles Dickens", "Jane Austen"],
        "correct_answer": "Harper Lee"
    },
    # Add more questions here
    # ...
]

additional_questions2 = [
    {
        "question": "Which element has the chemical symbol 'Fe'?",
        "options": ["Iron", "Gold", "Silver", "Copper"],
        "correct_answer": "Iron"
    },
    {
        "question": "What is the national flower of Japan?",
        "options": ["Cherry Blossom", "Lotus", "Rose", "Sunflower"],
        "correct_answer": "Cherry Blossom"
    },
    {
        "question": "In which year did the Berlin Wall fall?",
        "options": ["1989", "1991", "1987", "1993"],
        "correct_answer": "1989"
    },
    {
        "question": "Who is the author of the novel 'The Catcher in the Rye'?",
        "options": ["J.D. Salinger", "F. Scott Fitzgerald", "Ernest Hemingway", "George Orwell"],
        "correct_answer": "J.D. Salinger"
    },
    # Add more questions here...
]

questions += additional_questions1


questions += additional_questions2  # Merge additional questions with existing ones


difficulty = 1

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x300")
        
        self.session_data = []  # List to store session details

        self.label_name = tk.Label(root, text="Enter your full name:")
        self.label_name.pack()
        self.entry_name = tk.Entry(root)
        self.entry_name.pack()

        self.label_dob = tk.Label(root, text="Enter your date of birth (YYYY-MM-DD):")
        self.label_dob.pack()
        self.entry_dob = tk.Entry(root)
        self.entry_dob.pack()

        self.start_button = tk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack()

        self.quiz_frame = tk.Frame(root)
        self.label = tk.Label(self.quiz_frame, text="", font=("Arial", 14))
        self.label.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.quiz_frame, text="", width=30, command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.option_buttons.append(btn)
            
        self.selected_answers = [-1] * len(questions)

    def start_quiz(self):
        self.name = self.entry_name.get().strip()
        self.dob = self.entry_dob.get().strip()
        self.user_id = str(uuid.uuid4())
        session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.session_data.append({
            "start_time": session_start_time,
            "name": self.name,
            "dob": self.dob,
            "session_score": 0,  # Initialize session score to zero
            # Add any other important details about the session or the user
        })

        if not self.name or not self.dob:
            messagebox.showwarning("Warning", "Please enter your full name and date of birth.")
        else:
            self.label_name.pack_forget()
            self.entry_name.pack_forget()
            self.label_dob.pack_forget()
            self.entry_dob.pack_forget()
            self.start_button.pack_forget()

            self.quiz_frame.pack(pady=10)
            self.current_question = 0
            self.load_question()

    def load_question(self):
        global difficulty
        if self.current_question < len(questions):
            question_data = questions[self.current_question]
            self.label.config(text=question_data["question"])
            options = sample(question_data["options"], len(question_data["options"]))
            for i in range(4):
                self.option_buttons[i].config(text=options[i])
            self.correct_option = options.index(question_data["correct_answer"])
        else:
            self.show_result()

    def check_answer(self, selected_index):
        global difficulty
        # self.selected_answers[self.current_question - 1] = selected_index
        
        if self.current_question > len(self.selected_answers):
        # Extend the list with placeholder values (-1) for unanswered questions
            self.selected_answers.extend([-1] * (self.current_question - len(self.selected_answers)))

        # Update the selected answer for the current question
        self.selected_answers[self.current_question - 1] = selected_index
        
        if selected_index == self.correct_option:
            self.score = self.score + 1 if hasattr(self, 'score') else 1  # Increment score by 1 for correct answer
        self.current_question += 1
        if self.current_question < len(questions):
            difficulty += 1
            self.load_question()
        else:
            self.show_result()
            self.quiz_frame.pack_forget()  # Hide the play screen after showing the score

    def show_result(self):
        # Calculate total score for the current session
        session_score = sum(1 for idx, answer in enumerate(self.selected_answers) if
                            answer == questions[idx]['correct_answer'])

        # Update session score in session_data for the current session
        self.session_data[-1]['session_score'] = session_score

        # Add the session data to the user details JSON file
        try:
            with open("user_details.json", "r") as file:
                user_details = json.load(file)
        except FileNotFoundError:
            user_details = []

        user_details.extend(self.session_data)  # Add session data to user details

        with open("user_details.json", "w") as file:
            json.dump(user_details, file, indent=4)
            
        self.show_quiz_summary()
        
        
    def show_quiz_summary(self):
        summary_root = tk.Toplevel()
        summary_root.title("Quiz Summary")
        summary_root.geometry("500x400")

        summary_label = tk.Label(summary_root, text="Quiz Summary", font=("Arial", 14))
        summary_label.pack(pady=10)

        # Create a scrollable text area for displaying the quiz summary
        summary_scroll = tk.Scrollbar(summary_root)
        summary_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        summary_text = tk.Text(summary_root, wrap=tk.WORD, yscrollcommand=summary_scroll.set)
        summary_text.pack(expand=True, fill=tk.BOTH)
        summary_scroll.config(command=summary_text.yview)

        total_questions = len(questions)
        total_correct_answers = sum(1 for idx, answer in enumerate(self.selected_answers) if
                                    answer == questions[idx]['correct_answer'])

        summary_text.insert(tk.END, f"Total Questions: {total_questions}\n")
        summary_text.insert(tk.END, f"Total Correct Answers: {total_correct_answers}\n\n")

        # Define text colors for correct and incorrect answers
        summary_text.tag_configure("correct", foreground="green")
        summary_text.tag_configure("incorrect", foreground="red")

        for idx, question in enumerate(questions):
            correct_answer = [question['correct_answer']]
            user_selected_index = self.selected_answers[idx]
            user_answer = question['options'][user_selected_index] if user_selected_index != -1 else "Not Answered"

            summary_text.insert(tk.END, f"Question {idx + 1}: {question['question']}\n")
            summary_text.insert(tk.END, f"Correct Answer: {correct_answer}\n")
            summary_text.insert(tk.END, f"User's Answer: {user_answer}\n")

            # Color-coded display for correct and user answers
            if user_selected_index != -1:
                result = "Correct" if user_answer == correct_answer else "Wrong"
                tag = "correct" if result == "Correct" else "incorrect"

                summary_text.insert(tk.END, f"Result: {result}\n", tag)
            else:
                summary_text.insert(tk.END, "Result: Not Answered\n")

            summary_text.insert(tk.END, "-------------------------\n")

        summary_text.configure(state=tk.DISABLED)  # Disable text editing


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
    app.show_result()  # Display result first
    # app.show_quiz_summary()
