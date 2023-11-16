import tkinter as tk
import json
import datetime




current_user = None
current_question = 0
score = 0
selected_option = None
start_time = None


def save_user_data():
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def start_quiz():
    global current_user, start_time
    name = name_entry.get()
    email = email_entry.get()
    dob = dob_entry.get()

    user_id = len(users) + 1
    current_user = {'id': user_id, 'name': name, 'email': email, 'dob': dob}

    start_time = datetime.datetime.now()
    
    for question in quiz_questions:
        question['selected_option'] = None

    login_frame.pack_forget()
    quiz_frame.pack()

    show_question()

def show_question():
    question_label.config(text=quiz_questions[current_question]['question'])

    for i, option in enumerate(quiz_questions[current_question]['options']):
        option_buttons[i].config(text=option, command=lambda i=i: select_option(i))

    next_button.config(state=tk.DISABLED)

def select_option(option):
    next_button.config(state=tk.NORMAL)
    global selected_option
    selected_option = option
    quiz_questions[current_question]['selected_option'] = option


def next_question():
    global current_question

    quiz_questions[current_question]['selected_option'] = selected_option

    current_question += 1
    if current_question < len(quiz_questions):
        show_question()
    else:
        end_time = datetime.datetime.now()

        score = 0
        for question in quiz_questions:
            if question['selected_option'] == question['answer']:
                score += 1

        session_summary = {
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'time_taken': str(end_time - start_time),
            'score': score,
            'questions_answered': len(quiz_questions),
            'correct_answers': score,
            'answers': []
        }

        for question in quiz_questions:
            selected_answer = "Not answered"
            if question['selected_option'] is not None:
                selected_answer = question['options'][question['selected_option']]

            session_summary['answers'].append({
                'question': question['question'],
                'correct_answer': question['answer'],
                'selected_answer': selected_answer
            })

        current_user['session_summary'] = session_summary

        users[current_user['id']] = current_user
        save_user_data()

        show_summary(score)



def show_summary(score):
    summary_window = tk.Toplevel(root)
    summary_window.title("Quiz Summary")

    summary_label = tk.Label(summary_window, text=f"Your score: {score}/{len(quiz_questions)}")
    summary_label.pack()

    # Create a frame for the scrollable summary
    summary_frame = tk.Frame(summary_window)
    summary_frame.pack()

    # Create a scrollbar for the summary
    scrollbar = tk.Scrollbar(summary_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a text widget to display the summary with scrollbar
    summary_text = tk.Text(summary_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    summary_text.pack()

    scrollbar.config(command=summary_text.yview)

    for answer in current_user['session_summary']['answers']:
        question_text = answer['question'] + '\n'
        correct_answer = "Correct Answer: " + answer['correct_answer'] + '\n'
        selected_answer = "Your Answer: " + answer['selected_answer'] + '\n'

        summary_text.insert(tk.END, question_text)
        summary_text.insert(tk.END, correct_answer)

        if answer['correct_answer'] == answer['selected_answer']:
            summary_text.insert(tk.END, selected_answer, 'correct')
        else:
            summary_text.insert(tk.END, selected_answer, 'incorrect')

        summary_text.insert(tk.END, "\n----------------------------------------\n")

    # Configure text tags for color coding
    summary_text.tag_config('correct', foreground='green')
    summary_text.tag_config('incorrect', foreground='red')

    # Disable text editing in the summary
    summary_text.config(state=tk.DISABLED)
    
    
    

# Load user data from JSON file or create an empty dictionary
try:
    with open('users.json', 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

# Load quiz questions from JSON file
with open('quiz_questions.json', 'r') as file:
    quiz_questions = json.load(file)



root = tk.Tk()
root.title("Python Quiz App")
root.geometry("600x400")  # Set initial window size

login_frame = tk.Frame(root)
login_frame.pack()

name_label = tk.Label(login_frame, text="Full Name:")
name_label.pack()
name_entry = tk.Entry(login_frame)
name_entry.pack()

email_label = tk.Label(login_frame, text="Email:")
email_label.pack()
email_entry = tk.Entry(login_frame)
email_entry.pack()

dob_label = tk.Label(login_frame, text="Date of Birth (YYYY-MM-DD):")
dob_label.pack()
dob_entry = tk.Entry(login_frame)
dob_entry.pack()

start_button = tk.Button(login_frame, text="Start Quiz", command=start_quiz)
start_button.pack()

quiz_frame = tk.Frame(root)

question_label = tk.Label(quiz_frame, text="")
question_label.pack()

option_buttons = []
for i in range(4):
    option_button = tk.Button(quiz_frame)
    option_button.pack()
    option_buttons.append(option_button)

next_button = tk.Button(quiz_frame, text="Next", command=next_question)
next_button.pack()
next_button.config(state=tk.DISABLED)

root.mainloop()
