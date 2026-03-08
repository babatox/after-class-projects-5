import requests
url='https://api.funfacts.com/facts/human-body '

def get_random_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact = response.json()
        print(f"Did you know\n{fact['text']}")
    else:
        print("Failed to retrieve a fact.")

        while true:
            user_input = input("Would you like to hear a fun fact about the human body? (yes/no): ").strip().lower()
            if user_input == 'yes':
                get_random_fact()
            elif user_input == 'no':
                print("Okay, have a great day!")
                break
            else:
                print("Please enter 'yes' or 'no'.")
                break
            get_random_fact()

