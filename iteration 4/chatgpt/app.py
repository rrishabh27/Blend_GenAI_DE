import json
import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self):
        self.score = 0
        self.questions = self.load_questions()
        self.user_answers = []
        self.q_index = 0

        self.root = tk.Tk()
        self.root.title("Python Quiz App")
        self.details = {}

        self.create_user_details_widgets()

    def load_questions(self):
        with open('quiz_questions.json', 'r') as file:
            questions = json.load(file)
        return questions

    def save_user_details(self):
        self.details['name'] = self.name_entry.get()
        self.details['age'] = self.age_entry.get()
        self.save_user_details_to_file()
        self.user_details_frame.destroy()
        self.init_quiz()

    def save_user_details_to_file(self):
        with open('user_details.json', 'w') as file:
            json.dump(self.details, file, indent=4)

    def create_user_details_widgets(self):
        self.user_details_frame = tk.Frame(self.root)
        self.user_details_frame.pack()

        tk.Label(self.user_details_frame, text="Enter your name: ").pack()
        self.name_entry = tk.Entry(self.user_details_frame)
        self.name_entry.pack()

        tk.Label(self.user_details_frame, text="Enter your age: ").pack()
        self.age_entry = tk.Entry(self.user_details_frame)
        self.age_entry.pack()

        tk.Button(self.user_details_frame, text="Save Details", command=self.save_user_details).pack()

    def init_quiz(self):
        self.question_label = tk.Label(self.root, text=self.questions[self.q_index]['question'])
        self.question_label.pack()

        self.option_buttons = []
        for option in self.questions[self.q_index]['options']:
            button = tk.Button(self.root, text=option, command=lambda opt=option: self.submit_answer(opt))
            self.option_buttons.append(button)
            button.pack()

    def submit_answer(self, selected_option):
        if selected_option == self.questions[self.q_index]['answer']:
            self.score += 1
        self.user_answers.append({
            "question": self.questions[self.q_index]['question'],
            "selected_option": selected_option,
            "correct_answer": self.questions[self.q_index]['answer']
        })
        self.next_question()

    def next_question(self):
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)
        if self.q_index < len(self.questions) - 1:
            self.q_index += 1
            self.question_label.config(text=self.questions[self.q_index]['question'])
            for i, option in enumerate(self.questions[self.q_index]['options']):
                self.option_buttons[i].config(text=option, state=tk.NORMAL)
        else:
            self.quiz_completed()

    def quiz_completed(self):
        messagebox.showinfo("Quiz Summary", f"Total Score: {self.score}/{len(self.questions)}")
        self.save_user_details_to_file()
        self.root.destroy()

# Starting the quiz
QuizApp()
