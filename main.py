import requests
from config import API_KEY

API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_KEY}"}

def summarized_text(text):
    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 100,
            "min_length": 30,
            "do_sample": False
        }
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]["summary_text"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

def main():
    print("--- Summarize Your Text ---")
    print("Type your text and press Enter to summarize.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input(">> Paste or type your text here: ").strip()

        if user_input.lower() == "quit":
            print("Exiting...")
            break

        if not user_input:
            print("Please enter some text to summarize.\n")
            continue

        print("Summarizing...")
        summary = summarized_text(user_input)

        print("\n--- SUMMARY ---")
        print(summary)
        print()

if __name__ == "__main__":
    main()
