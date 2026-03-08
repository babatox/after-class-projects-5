import requests

def random_jokes():
    url = "https://official-joke-api.appspot.com/jokes/random"
    response = requests.get(url)
    
    if response.status_code == 200:
        joke_data = response.json()
        
        print(f"Full JSON response: {joke_data}")
        return f"{joke_data['setup']}\n{joke_data['punchline']}"
    else:
        return f"Error: {response.status_code}"

def main():
    print("Welcome to the Random Joke Generator!")
    while True:
        user_input = input("Press Enter to get a joke, or type 'exit' to quit: ")
        if user_input.lower().strip() == 'exit':
            print("Goodbye!")
            break
        joke = random_jokes()
        print(joke)

if __name__ == "__main__":
    main()