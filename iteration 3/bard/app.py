import json
import time
import tkinter as tk

# Load questions from JSON file
with open('questions.json') as f:
    questions_data = json.load(f)
questions = questions_data['questions']

# Initialize variables
user_details = {}
start_time = 0
end_time = 0
total_time = 0
correct_answers = 0
incorrect_answers = 0

# Create the main window for GUI
window = tk.Tk()
window.title("Quiz App")

# Function to display welcome message and collect user details
def start_quiz():
    global user_details

    welcome_label = tk.Label(window, text="Welcome to the Quiz!", font=("Arial", 18))
    welcome_label.pack(pady=20)

    name_label = tk.Label(window, text="Enter your name:", font=("Arial", 12))
    name_label.pack(pady=5)
    name_entry = tk.Entry(window)
    name_entry.pack()

    email_label = tk.Label(window, text="Enter your email:", font=("Arial", 12))
    email_label.pack(pady=5)
    email_entry = tk.Entry(window)
    email_entry.pack()

    start_button = tk.Button(window, text="Start Quiz", font=("Arial", 12), command=start_questions)
    start_button.pack(pady=20)

    # Store user details in a dictionary
    user_details['name'] = name_entry.get()
    user_details['email'] = email_entry.get()
    start_questions()

# Function to display questions and handle user responses
def start_questions():
    global start_time, correct_answers, incorrect_answers

    # Initialize answer tracking variable
    answer_var = tk.StringVar()

    start_time = time.time()

    for index, question in enumerate(questions):
        question_text = tk.Label(window, text=question['text'], font=("Arial", 12))
        question_text.pack(pady=10)

        answer_options = []
        for option in question['options']:
            answer_radiobutton = tk.Radiobutton(window, text=option['text'], variable=answer_var, value=option['value'])
            answer_options.append(answer_radiobutton)
            answer_radiobutton.pack()

        # Check user's answer against the correct answer
        if answer_var.get() == question['answer']:
            correct_answers += 1
        else:
            incorrect_answers += 1

        # Clear radio button selection for the next question
        answer_var.set(None)

        # Remove question and answer options from the pack to avoid cluttering the window
        for widget in question_text, *answer_options:
            widget.pack_forget()

    # Quiz completed, display quiz summary
    end_time = time.time()
    total_time = end_time - start_time
    show_quiz_summary()

# Function to display quiz summary
def show_quiz_summary():
    summary_label = tk.Label(window, text="Quiz Summary", font=("Arial", 18))
    summary_label.pack(pady=20)

    correct_label = tk.Label(window, text="Correct Answers:", font=("Arial", 12))
    correct_label.pack(pady=5)
    correct_answer_count = tk.Label(window, text=correct_answers, font=("Arial", 12))
    correct_answer_count.pack()

    incorrect_label = tk.Label(window, text="Incorrect Answers:", font=("Arial", 12))
    incorrect_label.pack(pady=5)
    incorrect_answer_count = tk.Label(window, text=incorrect_answers)
    incorrect_answer_count.pack()

    time_taken_label = tk.Label(window, text="Total Time Taken:", font=("Arial", 12))
    time_taken_label.pack(pady=5)
    time_taken = tk.Label(window, text=f"{total_time:.2f} seconds", font=("Arial", 12))
    time_taken.pack()

    # Save user details, quiz summary, and timestamp in a JSON file
    with open('quiz_results.json', 'w') as f:
        quiz_results = {
            "user_details": user_details,
            "start_time": start_time,
            "end_time": end_time,
            "total_time": total_time,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
        }
        json.dump(quiz_results, f, indent=4)

# Keep the main window running until the user closes it
start_quiz()
window.mainloop()

