import tkinter as tk
from tkinter import messagebox
import random
from playsound import playsound
from PIL import Image, ImageTk
import threading
import os

# loading questions from quiz creator
def load_questions(filename="input_questions_answer.txt"):
    questions = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()

        current_question = ""
        current_choices = {}
        current_answer = ""

        for line in lines:
            line = line.strip()

            if line.startswith("Question:"):
                current_question = line.replace("Question:", "").strip()
                current_choices = {}
            elif line.startswith(("a)", "b)", "c)", "d)")):
                key = line[0]
                value = line[2:].strip()
                current_choices[key] = value
            elif line.startswith("Answer Key:"):
                current_answer = line.replace("Answer Key:", "").strip()
            elif line.startswith("-" * 5):
                questions.append({
                    "question": current_question,
                    "choices": current_choices,
                    "answer": current_answer
                })

    except FileNotFoundError:
        print("'input_questions_answer.txt' not found. Please run the quiz creator.py")

    return questions 

# play sound file from folder "sounds"
def play_sound(filename):
    try:
        sound_dir = os.path.join(os.path.dirname(__file__), "sounds")
        path = os.path.join(sound_dir, filename)
        
        # Use threading to play sound without blocking the UI
        threading.Thread(target=lambda: playsound(path), daemon=True).start()
    except Exception as error:
        print(f"[Sound Error] {error}")

# main UI for quiz player
class UI:
    def __init__(self, master):
        # initializinf for color of UI
        root.configure(background='#FFCCCC')
        self.master = master
        self.master.title("QUIZ PLAYER")
        self.master.geometry("600x600")
        self.score = 0
        self.total = 0
        self.questions = load_questions()
        self.current_index = 0
        self.current_question = None

        # set up resource folder
        self.image_dir = os.path.join(os.path.dirname(__file__), "images")
        self.sound_dir = os.path.join(os.path.dirname(__file__), "sounds")
        
        os.makedirs(self.image_dir, exist_ok=True)
        os.makedirs(self.sound_dir, exist_ok=True)
        
        self.images = {
            'correct': self.load_image("correct.png"),
            'wrong': self.load_image("wrong.png")
        }
        
        # question label UI
        self.question_label = tk.Label(
            master,
            text="",
            font=("Cooper Black", 14),
            wraplength=480,
            justify="left",
            foreground="gray20",
            background="#FFCCCC"
        )
        self.question_label.pack(pady=20)

        # creating answer button (color and size)
        self.buttons = {}
        color_map = {
            'a': '#A3C4F3',
            'b': '#A0E7E5',
            'c': '#FFF6A3',
            'd': '#FFAFCC'
        }

        for key in ['a', 'b', 'c', 'd']:
            btn = tk.Button(
                master,
                text="",
                font=("Cooper Black", 12),
                width=30,
                fg="gray20",       
                bg=color_map[key],              
                activebackground="gray20",
                activeforeground="white",
                command=lambda answer_key=key: self.check_answer(answer_key)
                
            )
            btn.pack(pady=5)
            self.buttons[key] = btn
        
        # create score label
        self.score_label = tk.Label(
            master,
            text="Score: 0/0",
            font=("Cooper Black", 12),
            fg="white",
            bg="#FFCCCC"
        )
        self.score_label.pack(pady=10)
        
        # image display (feedback)
        self.image_label = tk.Label(master, bg="#FFCCCC")
        self.image_label.pack(pady=10)

        # create next question button (color and size)
        self.next_button = tk.Button(
            master,
            text="Next Question",
            font=("Cooper Black", 12),
            command=self.next_question,
            fg="white",
            bg="gray20",
            activebackground="gray40"
        )
        self.next_button.pack(pady=10)

        self.next_question()
    
    # load and resize image
    def load_image(self, filename):
        try:
            image_path = os.path.join(self.image_dir, filename)
            img = Image.open(image_path)
            return ImageTk.PhotoImage(img.resize((120, 120)))
        except Exception as error:
            print(f"[Image Error] {error}")
            blank_img = Image.new('RGB', (120, 120), color='#FFCCCC')
            return ImageTk.PhotoImage(blank_img)
    
    # change background color (if correct or wrong)
    def flash_background(self, color, duration=5000):
        original_color = self.master.cget("bg")
        self.master.config(bg=color)
        self.master.after(duration, lambda: self.master.config(bg=original_color))
    
    # display result image (if correct or wrong)
    def show_result_image(self, image_type):

        self.image_label.configure(image=self.images[image_type])
        self.image_label.image = self.images[image_type]

    # load next questions
    def next_question(self):
        if self.current_index >= len(self.questions):
            self.question_label.config(text="Congrats! You finished all the questions!")
            for btn in self.buttons.values():
                btn.config(state="disabled")
            self.next_button.config(state="disabled")
            return
        
        self.image_label.configure(image='') 
        self.image_label.image = None

        self.current_question = self.questions[self.current_index]
        self.current_index += 1

        question_data = self.current_question
        self.question_label.config(text=f"Q: {question_data['question']}")
        for key in ['a', 'b', 'c', 'd']:
            self.buttons[key].config(text=f"{key}) {question_data['choices'][key]}", state="normal")
    
    # check if answer is correct or wrong (add flashing color and image)
    def check_answer(self, selected_key):
        correct = self.current_question['answer']
        if selected_key == correct:
            self.flash_background("#C1E1C1")
            self.show_result_image("correct")
            play_sound("correct.mp3")
            messagebox.showinfo("Result", "Correct!")
            self.score += 1
        else:
            self.flash_background("#FFB3BA")
            self.show_result_image("wrong")
            play_sound("wrong.mp3")
            correct_text = self.current_question['choices'][correct]
            messagebox.showerror("Result", f"Wrong!\nCorrect answer: {correct}) {correct_text}")
              
        self.total += 1
        self.score_label.config(text=f"Score: {self.score}/{self.total}")
        for btn in self.buttons.values():
            btn.config(state="disabled")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = UI(root)
    root.mainloop()