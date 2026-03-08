import requests
import random
import html
EDUCATION_CATEGORY_ID = 9
api_url = f"https://opentdb.com/api.php?amount=10&category={EDUCATION_CATEGORY_ID}&type=multiple"

def get_education_questions():
    response = requests.get(api_url)
    if response.status_code == 200:
        data=response.json()
        if data['response_code'] == 0 and data['results']:
            return data['results']
    return None

def run_quiz():
    questions = get_education_questions()
    if not questions:
        print("Failed to retrieve questions. Please try again later.")
        return
    
    score = 0
    print("Welcome to the Education Quiz!")
    for i,q in enumerate(questions,1):
        question = html.unescape(q['question'])
        correct_answer = html.unescape(q['correct_answer'])
        incorrect_answers = [html.unescape(ans) for ans in q['incorrect_answers']]

        options = incorrect_answers+[correct_answer]
        random.shuffle(options)

        print(f"\nQuestion {i}: {question}")
        for idx, option in enumerate(options,1):
            print(f"{idx}. {option}")
        while True:
            try:
                answer = int(input("Your answer (1-4): "))
                if 1 <= answer <= 4:
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4.")
        if options[answer-1] == correct_answer:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer was: {correct_answer}")       
    print(f"\nQuiz Over! Your final score is {score} out of {len(questions)}.")
if __name__ == "__main__":
    run_quiz()