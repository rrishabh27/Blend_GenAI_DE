import tkinter as tk
from tkinter import ttk
import random

# Define questions and their answers
questions = [
    {"text": "What is the capital of France?", "answers": ["Paris", "Berlin", "London", "Rome"], "correct_answer": 0},
    {"text": "What is the capital of Germany?", "answers": ["London", "Paris", "Berlin", "Rome"], "correct_answer": 2},
    {"text": "What is the capital of the United Kingdom?", "answers": ["Rome", "Berlin", "London", "Paris"], "correct_answer": 2},
    {"text": "What is the capital of Italy?", "answers": ["Paris", "Berlin", "Rome", "London"], "correct_answer": 2},
]

# Initialize variables
score = 0
difficulty_level = 1
current_question_index = 0

# Create the main window
root = tk.Tk()
root.title("Capital Quiz")

# Create the question label
question_label = ttk.Label(root, text=questions[0]['text'])
question_label.pack()

# Create the answer notebook
answer_notebook = ttk.Notebook(root)
answer_notebook.pack()

# Create the answer tabs
answer_tab1 = ttk.Frame(answer_notebook)
answer_tab2 = ttk.Frame(answer_notebook)
answer_tab3 = ttk.Frame(answer_notebook)
answer_tab4 = ttk.Frame(answer_notebook)

# Add the answer options to the answer tabs
answer_label1 = ttk.Label(answer_tab1, text=questions[0]['answers'][0])
answer_label1.pack()
answer_label2 = ttk.Label(answer_tab2, text=questions[0]['answers'][1])
answer_label2.pack()
answer_label3 = ttk.Label(answer_tab3, text=questions[0]['answers'][2])
answer_label3.pack()
answer_label4 = ttk.Label(answer_tab4, text=questions[0]['answers'][3])
answer_label4.pack()

# Add the answer tabs to the notebook
answer_notebook.add(answer_tab1, text=questions[0]['answers'][0])
answer_notebook.add(answer_tab2, text=questions[0]['answers'][1])
answer_notebook.add(answer_tab3, text=questions[0]['answers'][2])
answer_notebook.add(answer_tab4, text=questions[0]['answers'][3])

# Define the check_answer function
def check_answer():
    global score, difficulty_level, current_question_index

    selected_answer = answer_notebook.tab(answer_notebook.index('current'))
    answer_tab = selected_answer
    current_question = questions[current_question_index]

    if selected_answer == current_question['answers'][current_question['correct_answer']]:
        print("Correct!")
        score += 1
        difficulty_level += 1
    else:
        print(f"Incorrect. The correct answer is {current_question['answers'][current_question['correct_answer']]}")

    # Clear the answer options before loading the next question
    for i in range(answer_notebook.size()):
        answer_notebook.forget(i)

    # Load the next question
    if current_question_index < len(questions) - 1:
        current_question_index += 1
        question_label.config(text=questions[current_question_index]['text'])

        # Generate a new set of answer options
        new_answer_options = list(current_question['answers'])
        correct_answer_index = new_answer_options.index(current_question['answers'][current_question['correct_answer']])
        random.shuffle(new_answer_options)
        new_answer_options[correct_answer_index] = current_question['answers'][current_question['correct_answer']]

        # Update the answer options
        for i, answer in enumerate(new_answer_options):
            answer_notebook.add(answer_tab, text=answer)

# Bind the check_answer function to the Return key
root.bind('<Return>', check_answer)

# Start the main loop
root.mainloop()
