import json
import random
import tkinter as tk

def load_data(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def get_user_details():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    details = {"name": name, "email": email}
    return details

def generate_questions(difficulty_levels):
    questions = []
    for difficulty in difficulty_levels:
        for question in question_data[difficulty]:
            options = list(question['options'])
            random.shuffle(options)
            options_string = "\n".join(f"({option}) {answer}" for option, answer in enumerate(options))
            correct_answer = question['correct_answer']
            questions.append({
                "question": question['question'],
                "options": options_string,
                "correct_answer": correct_answer
            })

    return questions


def start_quiz():
    user_details = get_user_details()
    save_data('user_details.json', user_details)

    questions = generate_questions(['easy', 'medium', 'hard'])
    score = 0

    root = tk.Tk()
    root.title("Quiz Application")

    for question in questions:
        question_label = tk.Label(root, text=question['question'], font=('Arial', 12))
        question_label.pack()

        options_frame = tk.Frame(root)
        options_frame.pack()

        answer_var = tk.StringVar()

        correct_answer = question['correct_answer']

        for option_index, option in enumerate(question['options']):
            def handle_option_click(option_value=option):
                check_answer(correct_answer, option_value)

            option_button = tk.Button(options_frame, text=option, command=handle_option_click)
            option_button.pack()

        submit_button = tk.Button(root, text="Submit", command=lambda: check_answer(correct_answer, answer_var.get()))
        submit_button.pack()

        check_answer(correct_answer, answer_var.get())

    quiz_summary_label = tk.Label(root, text=f"Your score is {score} out of {len(questions)}", font=('Arial', 12))
    quiz_summary_label.pack()

    root.mainloop()

def check_answer(correct_answer, user_answer):
    if user_answer == correct_answer:
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is", correct_answer)








easy_questions = [
    {
        "question": "What is the capital of France?",
        "options": [
            "London",
            "Paris",
            "Berlin",
            "Rome"
        ],
        "correct_answer": "Paris"
    },
    {
        "question": "What is the largest country in the world by area?",
        "options": [
            "Russia",
            "China",
            "Canada",
            "United States"
        ],
        "correct_answer": "Russia"
    }
]

question_data = {
    "easy": easy_questions,
    "medium": [],
    "hard": []
}

if __name__ == "__main__":
    start_quiz()
