import tkinter as tk
import json
import datetime
import random

# Create main window for the quiz app
root = tk.Tk()
root.title("General Knowledge Quiz")
root.geometry("500x400")

# Initialize user details variables
full_name = ""
email = ""
dob = ""
user_id = ""
score = 0
questions = []
selected_questions = []
start_time = None
end_time = None

# Load quiz questions from JSON file
def load_quiz_questions():
    with open('quiz_questions.json') as f:
        questions = json.load(f)
    return questions

# Generate unique user ID
def generate_unique_id():
    # Implement logic to generate a unique ID based on user information or timestamp
    return 12345678

# Save user data to JSON file
def save_user_data(user_id, full_name, email, dob):
    user_data = {
        "user_id": user_id,
        "full_name": full_name,
        "email": email,
        "dob": dob
    }

    with open('users.json') as f:
        users = json.load(f)

    users[user_id] = user_data

    with open('users.json', 'w') as f:
        json.dump(users, f)

# Register user
def register_user():
    global full_name, email, dob, user_id

    full_name = full_name_entry.get()
    email = email_entry.get()
    dob = dob_entry.get()

    user_id = generate_unique_id()
    save_user_data(user_id, full_name, email, dob)

    # Display message indicating successful registration
    registration_message_label = tk.Label(root, text="Registration successful!")
    registration_message_label.pack()

# Login user
def login_user():
    global user_id

    user_id = user_id_entry.get()

    with open('users.json') as f:
        users = json.load(f)

    if user_id in users:
        # User exists, proceed to the quiz section
        start_quiz()
    else:
        # Invalid user ID, display error message
        login_error_label = tk.Label(root, text="Invalid user ID!")
        login_error_label.pack()

# Start the quiz
def start_quiz():
    global questions, score, start_time

    questions = load_quiz_questions()
    selected_questions = random.sample(questions, 10)
    score = 0
    start_time = datetime.datetime.now()

    # Display first question
    display_question(0)

# Display question and answer choices
def display_question(question_index):
    global questions, selected_questions

    question = selected_questions[question_index]

    question_label = tk.Label(root, text=question["question"])
    question_label.pack()

    for option_index, option in enumerate(question["options"]):
        option_button = tk.Button(root, text=option, command=lambda: check_answer(option_index + 1, question["answer"]))
        option_button.pack()

# Check user's answer and provide feedback
def check_answer(selected_option, correct_answer):
    global score

    if selected_option == correct_answer:
        score += 1
        answer_feedback_label = tk.Label(root, text="Correct")
    else:
        answer_feedback_label = tk.Label(root, text="Incorrect")

    answer_feedback_label.pack()

    # Display next question or quiz summary
    if question_index < len(selected_questions) - 1:
        question_index += 1
        display_question(question_index)
    else:
        end_time = datetime.datetime.now()
        display_quiz_summary(questions, selected_questions, score, start_time, end_time)

# Display quiz summary
def display_quiz_summary(questions, selected_questions, score, start_time, end_time):
    quiz_summary_label = tk.Label(root, text="Quiz Summary:")
    quiz_summary_label.pack()

    total_questions_label = tk.Label(root, text="Total Questions: " + str(len(selected_questions)))
    total_questions_label.pack()

    correct_answers_label = tk.Label(root, text="Correct Answers: " + str(score))
    correct_answers_label.pack()

    incorrect_answers_label = tk.Label(root, text="Incorrect Answers: " + str(len(selected_questions) - score))
    incorrect_answers_label.pack()

    time_taken_label = tk.Label(root, text="Time Taken: " + str(end_time - start_time))
    time_taken_label.pack()

    # Save quiz results to JSON file
    quiz_results = {
        "user_id": user_id,
        "questions": selected_questions,
        "answers": user_answers,
        "score": score,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }

    with open('quiz_results.json') as f:
        quiz_results_list = json.load(f)

    quiz_results_list.append(quiz_results)

    with open('quiz_results.json', 'w') as f:
        json.dump(quiz_results_list, f)
        
        
    # Provide option to go back to main menu or exit
    back_to_main_menu_button = tk.Button(root, text="Back to Main Menu", command=back_to_main_menu)
    back_to_main_menu_button.pack()

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack()

# Main menu function
def back_to_main_menu():
    # Clear the interface
    for widget in root.winfo_children():
        widget.destroy()

    # Display registration and login options
    registration_label = tk.Label(root, text="Registration:")
    registration_label.pack()

    full_name_label = tk.Label(root, text="Full Name:")
    full_name_label.pack()

    full_name_entry = tk.Entry(root)
    full_name_entry.pack()

    email_label = tk.Label(root, text="Email:")
    email_label.pack()

    email_entry = tk.Entry(root)
    email_entry.pack()

    dob_label = tk.Label(root, text="Date of Birth:")
    dob_label.pack()

    dob_entry = tk.Entry(root)
    dob_entry.pack()

    submit_button = tk.Button(root, text="Submit", command=register_user)
    submit_button.pack()

    login_label = tk.Label(root, text="Login:")
    login_label.pack()

    user_id_label = tk.Label(root, text="User ID:")
    user_id_label.pack()

    user_id_entry = tk.Entry(root)
    user_id_entry.pack()

    login_button = tk.Button(root, text="Login", command=login_user)
    login_button.pack()

# Run the main loop
root.mainloop()
