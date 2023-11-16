import tkinter as tk
import random
import json
# import ttk
import datetime
from tkinter import ttk



# Load questions from a JSON file
with open('quiz_questions.json') as f:
    questions = json.load(f)

# Initialize variables
score = 0
difficulty_level = 1
user_details = {}

# Create the main window
root = tk.Tk()
root.title("World General Knowledge Quiz")

# Create a frame to hold the question and answer options
question_frame = tk.Frame(root)
question_frame.pack(fill='both', expand=True)

# Create a label to display the question text
question_label = tk.Label(question_frame, text="")
question_label.pack()

# Create a notebook to hold the answer options
answer_notebook = ttk.Notebook(question_frame)
answer_notebook.pack()

current_question_index = 0

# Create tabs for each answer option
for i, answer in enumerate(questions[current_question_index]['answers']):
    answer_tab = ttk.Frame(answer_notebook)
    answer_label = tk.Label(answer_tab, text=answer)
    answer_label.pack()

    answer_notebook.add(answer_tab, text=answer)
    
    
def load_next_question():
    global score, difficulty_level, idx

    # Load the next question
    next_question = random.choice(questions[1:])
    question_label.config(text=next_question['text'])

    # Shuffle the answer options
    random.shuffle(next_question['answers'])

    # Update the answer options
    for i, answer in enumerate(next_question['answers']):
        answer_notebook.tab(i, text=answer)

def check_answer():
    global score, difficulty_level, current_question_index

    selected_answer = answer_notebook.tab(answer_notebook.index('current'))

    current_question = questions[current_question_index]

    if selected_answer == current_question['answers'][current_question['correct_answer']]:
        print("Correct!")
        score += 1
        difficulty_level += 1
    else:
        print(f"Incorrect. The correct answer is {current_question['answers'][current_question['correct_answer']]}")

    # Clear the answer options before loading the next question
    num_tabs, num_children = answer_notebook.size()
    for i in range(num_tabs):
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












# Create a submit button
submit_button = tk.Button(root, text="Submit Answer", command=check_answer)
submit_button.pack()

# Display the first question
question_label.config(text=questions[0]['text'])

# Shuffle the answer options
random.shuffle(questions[0]['answers'])

# Update the answer options
for i, answer in enumerate(questions[0]['answers']):
    answer_notebook.tab(answer_notebook.index('current'), text=answer)

# Start the quiz loop
root.mainloop()
