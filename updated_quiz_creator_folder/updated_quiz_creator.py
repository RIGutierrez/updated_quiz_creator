import os
from playsound import playsound

def clearing_screen_input():
    # clear screen for cleaner look when typing questions
    os.system('cls' if os.name == 'nt' else 'clear')

def play_sound():
    
    # playing sound
    try:
        sound_file = os.path.join(os.path.dirname(__file__), "success_1.mp3")
        playsound(sound_file)
    except Exception as error:
        print(f"[!] Sound error:\n    {error}")

def user_input_question_answers():
    
    # ask user for question and choices
    question = input("Enter your quiz question: ")
    play_sound()
    choices = {}

    for letter in ['a', 'b', 'c', 'd']:
        choices[letter] = input(f"Enter choice {letter.upper()}: ")
        play_sound()
        
    # ask for correct answer
    while True:
        answer = input("Enter the correct answer (a/b/c/d): ").lower()
        if answer in choices:
            break
        print("Invalid input. Please enter one of a, b, c, or d.")

    # add return function for question to return data as dictionary
    return {
        "question": question.strip(),
        "choices" : choices,
        "answer"  : answer
    }

# save the question, choices, and answer key as txt
# take parameters for saving question
def saved_user_questions_answers(data, filename="input_questions_answer.txt"):
    
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"Question: {data['question']}\n")
        for key in ['a', 'b', 'c', 'd']:
            file.write(f"{key}) {data['choices'][key]}\n")
        file.write(f"Answer Key: {data['answer']}\n")
        file.write("-" * 45 + "\n\n")
        
        print("\nYour inputted question has been recorded!\n")
        play_sound()

# use def and make a main loop
def main():
    while True:
        clearing_screen_input()
        question_answers_data = user_input_question_answers()
        saved_user_questions_answers(question_answers_data)

        user_choice = input("Do you want to add more question? (y/n)").strip().lower()
        if user_choice not in ['y', 'yes']:
            print("Exiting... Your questions are ready!\n")
            break

# call main()
main()