import os
import random
import tkinter as tk
from datetime import datetime

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cybersecurity Quiz Game")
        self.root.geometry("1000x600")
        self.root.configure(bg="#1e1e2f")
        
        self.username = ""
        self.category = ""
        self.questions = []
        self.current_question = 0
        self.score = 0
        self.timer_id = None
        self.time_left = 15

        self.selected_answer = tk.StringVar()
        
        self.show_username_input()

    def show_username_input(self):
        self.clear_root()
        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(expand=True)

        tk.Label(frame, text="Enter Your Full Name:", font=("Helvetica", 18), fg="white", bg="#1e1e2f").pack(pady=10)
        self.name_entry = tk.Entry(frame, font=("Helvetica", 16), width=30)
        self.name_entry.pack(pady=10)
        self.name_entry.focus()

        tk.Button(frame, text="Next", font=("Helvetica", 14), command=self.get_username, bg="#4a90e2", fg="white", relief="flat",
                  activebackground="#357ABD", activeforeground="white", width=12).pack(pady=10)

    def get_username(self):
        name = self.name_entry.get().strip()
        if not name:
            return
        self.username = name
        self.show_category_selection()

    def get_categories(self):
        path = "questions"
        if not os.path.exists(path):
            return []
        return [f[:-4] for f in os.listdir(path) if f.endswith('.txt')]

    def show_category_selection(self):
        self.clear_root()
        categories = self.get_categories()
        if not categories:
            tk.Label(self.root, text="No categories found! Add files to 'questions/' folder.", font=("Helvetica", 16), fg="red", bg="#1e1e2f").pack(pady=20)
            return

        label = tk.Label(self.root, text=f"Hello, {self.username}! Select a category:", font=("Helvetica", 20, "bold"), fg="white", bg="#1e1e2f")
        label.pack(pady=25)

        btn_frame = tk.Frame(self.root, bg="#1e1e2f")
        btn_frame.pack()

        for cat in categories:
            btn = tk.Button(btn_frame, text=cat.capitalize(), font=("Helvetica", 18), width=18, height=2,
                            bg="#4a90e2", fg="white", relief="flat",
                            activebackground="#357ABD", activeforeground="white",
                            command=lambda c=cat: self.select_category(c))
            btn.pack(pady=8)

    def select_category(self, category):
        self.category = category
        self.questions = self.load_questions(os.path.join("questions", f"{category}.txt"))
        if not self.questions:
            tk.Label(self.root, text="No questions loaded. Check your file.", fg="red", bg="#1e1e2f", font=("Helvetica", 16)).pack(pady=20)
            return
        random.shuffle(self.questions)
        self.current_question = 0
        self.score = 0
        self.show_quiz_ui()

    def load_questions(self, filename):
        questions = []
        try:
            with open(filename, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) == 6:
                        question = {
                            "prompt": parts[0],
                            "options": parts[1:5],
                            "answer": parts[5].upper()
                        }
                        questions.append(question)
        except FileNotFoundError:
            pass
        return questions

    def show_quiz_ui(self):
        self.clear_root()

        self.quiz_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.quiz_frame.pack(expand=True, fill="both")

        # Show username top right
        user_label = tk.Label(self.quiz_frame, text=f"User: {self.username}", font=("Helvetica", 12), fg="white", bg="#1e1e2f")
        user_label.pack(anchor="ne", padx=15, pady=5)

        # Question number
        self.question_num_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 18, "bold"), fg="white", bg="#1e1e2f")
        self.question_num_label.pack(pady=10)

        # Question prompt
        self.question_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 20), fg="white", bg="#1e1e2f", wraplength=850, justify="left")
        self.question_label.pack(pady=15)

        # Radio buttons for options
        self.selected_answer.set(None)
        self.option_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.quiz_frame, text="", font=("Helvetica", 16), variable=self.selected_answer,
                                value="", bg="#1e1e2f", fg="white", selectcolor="#4a90e2", activebackground="#1e1e2f",
                                activeforeground="white", indicatoron=0, width=40, padx=20, pady=10,
                                command=self.enable_submit)
            rb.pack(pady=6)
            self.option_buttons.append(rb)

        # Timer label
        self.timer_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14, "bold"), fg="#ff6666", bg="#1e1e2f")
        self.timer_label.pack(pady=10)

        # Feedback label
        self.feedback_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 16, "bold"), bg="#1e1e2f")
        self.feedback_label.pack(pady=10)

        # Buttons frame
        btn_frame = tk.Frame(self.quiz_frame, bg="#1e1e2f")
        btn_frame.pack(pady=15)

        self.submit_btn = tk.Button(btn_frame, text="Submit Answer", font=("Helvetica", 16),
                                    command=self.check_answer, width=18, bg="#4a90e2", fg="white", relief="flat",
                                    activebackground="#357ABD", activeforeground="white", state="disabled")
        self.submit_btn.pack(side="left", padx=10)

        self.quit_btn = tk.Button(btn_frame, text="Quit", font=("Helvetica", 16), command=self.root.destroy,
                                  width=10, bg="#d9534f", fg="white", relief="flat",
                                  activebackground="#b52b27", activeforeground="white")
        self.quit_btn.pack(side="left", padx=10)

        self.load_question()

    def load_question(self):
        self.selected_answer.set(None)
        self.submit_btn.config(state="disabled")
        self.feedback_label.config(text="")
        self.time_left = 15

        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        if self.current_question >= len(self.questions):
            self.show_result()
            return

        q = self.questions[self.current_question]
        self.question_num_label.config(text=f"Question {self.current_question + 1} / {len(self.questions)}")
        self.question_label.config(text=q['prompt'])

        for i, option_text in enumerate(q['options']):
            self.option_buttons[i].config(text=option_text, value=option_text[0])

        self.update_timer()

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_left} sec")
        if self.time_left <= 0:
            self.submit_btn.config(state="disabled")
            self.feedback_label.config(text=f"⏰ Time's up! Moving to next question...", fg="#ff6666")
            self.current_question += 1
            self.root.after(1500, self.load_question)
        else:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)

    def enable_submit(self):
        self.submit_btn.config(state="normal")

    def check_answer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        q = self.questions[self.current_question]
        selected = self.selected_answer.get()
        correct = q['answer']

        self.submit_btn.config(state="disabled")

        if selected == correct:
            self.feedback_label.config(text="✅ Correct!", fg="#7CFC00")
            self.score += 1
        else:
            self.feedback_label.config(text=f"❌ Wrong. Correct answer was: {correct}", fg="#ff6666")

        self.current_question += 1
        self.root.after(1500, self.load_question)

    def show_result(self):
        self.clear_root()

        percent = (self.score / len(self.questions)) * 100
        result_text = (
            f"🧠 Quiz Complete!\n\n"
            f"Name: {self.username}\n"
            f"Category: {self.category.capitalize()}\n"
            f"Score: {self.score}/{len(self.questions)} ({percent:.1f}%)\n\n"
        )

        try:
            with open("scores.txt", "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} | {self.username} | {self.category} | {self.score}/{len(self.questions)} ({percent:.1f}%)\n")
        except Exception as e:
            print(f"Error saving score: {e}")

        scoreboard_text = self.get_top_scores_text()

        self.result_frame = tk.Frame(self.root, bg="#1e1e2f")
        self.result_frame.pack(pady=30, fill='both', expand=True)

        tk.Label(self.result_frame, text=result_text, font=('Helvetica', 18), fg="white", bg="#1e1e2f").pack(pady=15)
        tk.Label(self.result_frame, text="🏆 Top 5 Scores:", font=('Helvetica', 16, 'bold'), fg="#ffd700", bg="#1e1e2f").pack(pady=15)

        scoreboard_label = tk.Label(self.result_frame, text=scoreboard_text, font=('Helvetica', 14), fg="white", bg="#1e1e2f", justify="left")
        scoreboard_label.pack(pady=10)

        btn_frame = tk.Frame(self.result_frame, bg="#1e1e2f")
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Play Again",
            font=('Helvetica', 14),
            command=self.play_again,
            width=16,
            bg="#4a90e2",
            fg="white",
            relief="flat",
            activebackground="#357ABD",
            activeforeground="white"
        ).pack(side="left", padx=15)

        tk.Button(
            btn_frame,
            text="Quit",
            font=('Helvetica', 14),
            command=self.root.destroy,
            width=16,
            bg="#d9534f",
            fg="white",
            relief="flat",
            activebackground="#b52b27",
            activeforeground="white"
        ).pack(side="left", padx=15)

    def get_top_scores_text(self):
        if not os.path.exists("scores.txt"):
            return "No scores available yet."
        scores = []
        with open("scores.txt", "r") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 4:
                    timestamp, user, cat, score_str = parts
                    try:
                        score_val = float(score_str.split()[0].split('/')[0])
                        scores.append((score_val, user, cat, score_str, timestamp))
                    except:
                        continue
        scores.sort(key=lambda x: x[0], reverse=True)
        top5 = scores[:5]
        if not top5:
            return "No scores available yet."
        text_lines = []
        for i, (score_val, user, cat, score_str, timestamp) in enumerate(top5, 1):
            text_lines.append(f"{i}. {user} ({cat.capitalize()}) - {score_str} on {timestamp}")
        return "\n".join(text_lines)

    def play_again(self):
        self.show_category_selection()

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
