import sys
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QLineEdit,
    QMessageBox,
)


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Quiz App')
        self.layout = QVBoxLayout()

        self.name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.layout.addWidget(QLabel("Enter your name:", self))
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(QLabel("Enter your email:", self))
        self.layout.addWidget(self.email_input)

        self.start_button = QPushButton('Start Quiz', self)
        self.start_button.clicked.connect(self.start_quiz)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)
        self.show()

    def start_quiz(self):
        self.name = self.name_input.text().strip()
        self.email = self.email_input.text().strip()

        if not self.name or not self.email:
            QMessageBox.warning(self, 'Missing Information', 'Please enter name and email.')
            return

        self.name_input.setDisabled(True)
        self.email_input.setDisabled(True)
        self.start_button.setDisabled(True)

        self.quiz_data = self.load_questions()
        self.current_question = 0
        self.correct_answers = 0
        self.user_answers = []

        self.show_question()

    def load_questions(self):
        try:
            with open('data/questions.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            QMessageBox.warning(self, 'File Not Found', 'Questions file not found!')
            sys.exit()

    def show_question(self):
        if self.current_question < len(self.quiz_data):
            question = self.quiz_data[self.current_question]
            self.question_label = QLabel(question['question'], self)
            self.layout.addWidget(self.question_label)

            self.radio_buttons = []
            for i, option in enumerate(question['options']):
                radio_btn = QRadioButton(option, self)
                radio_btn.setChecked(False)
                self.radio_buttons.append(radio_btn)
                self.layout.addWidget(radio_btn)

            next_button = QPushButton('Next', self)
            next_button.clicked.connect(self.next_question)
            self.layout.addWidget(next_button)

        else:
            self.show_summary()

    def next_question(self):
        selected_option = None
        for i, radio_btn in enumerate(self.radio_buttons):
            if radio_btn.isChecked():
                selected_option = i
                break

        if selected_option is not None:
            self.user_answers.append(selected_option)
            correct_answer = self.quiz_data[self.current_question]['correct_option']
            if selected_option == correct_answer:
                self.correct_answers += 1

            self.current_question += 1
            self.clear_layout()
            self.show_question()
        else:
            QMessageBox.warning(self, 'No Answer Selected', 'Please select an answer!')

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def show_summary(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(minutes=15)  # Replace with actual start time

        time_taken = end_time - start_time

        quiz_summary = {
            'name': self.name,
            'email': self.email,
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'time_taken': str(time_taken),
            'total_questions': len(self.quiz_data),
            'correct_answers': self.correct_answers,
            'user_answers': self.user_answers,
        }

        with open('data/quiz_records.json', 'a') as file:
            json.dump(quiz_summary, file, indent=4)

        self.layout.addWidget(QLabel('Quiz Summary:\n', self))
        for i, question in enumerate(self.quiz_data):
            question_text = QLabel(f"{i + 1}. {question['question']}", self)
            self.layout.addWidget(question_text)

            correct_answer = question['correct_option']
            chosen_answer = self.user_answers[i] if i < len(self.user_answers) else None

            answer_label = QLabel(f"Correct Answer: {question['options'][correct_answer]}", self)
            self.layout.addWidget(answer_label)

            chosen_label = QLabel(f"Chosen Answer: {question['options'][chosen_answer]}" if chosen_answer is not None else "Chosen Answer: Not answered", self)
            chosen_label.setStyleSheet(
                'color: green;' if chosen_answer == correct_answer else 'color: red;'
            )
            self.layout.addWidget(chosen_label)

            self.layout.addWidget(QLabel('-----------------------------------', self))

        exit_button = QPushButton('Exit', self)
        exit_button.clicked.connect(self.close)
        self.layout.addWidget(exit_button)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            'Exit Confirmation',
            'Are you sure you want to exit?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    quiz_app = QuizApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
