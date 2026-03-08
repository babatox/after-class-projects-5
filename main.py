import requests
from config import API_KEY
from PIL import Image
import io
import os
from colorama import init, Fore, Style
import json

init(autoreset=True)

def query_api(api_url, payload=None, files=None, method="POST"):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        if method.lower() == "post":
            response = requests.post(api_url, headers=headers, json=payload, files=files)
        else:
            response = requests.get(api_url, headers=headers, params=payload)
        if response.status_code != 200:
            raise Exception(f"Status:{response.status_code}: {response.text}")
        return response.content
    except Exception as e:
        print(f"{Fore.RED}Error during API: {e}")
        raise

def get_basic_caption(image, model="Salesforce/blip-image-captioning-base"):
    print(f"{Fore.YELLOW}==Generating Basic Caption==")
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    buffered.seek(0)
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(api_url, headers=headers, data=buffered.getvalue())
    results = response.json()
    if isinstance(results, dict) and "error" in results:
        return f"Error: {results['error']}"
    caption = results[0]["generated_text"] if isinstance(results, list) and "generated_text" in results[0] else "No caption generated"
    return caption

def generate_text(prompt, model="gpt2", max_tokens=60):
    print(f"{Fore.YELLOW}==Generating Text==")
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
    text_bytes = query_api(api_url, payload=payload)
    try:
        results = json.loads(text_bytes.decode("utf-8"))
    except Exception as e:
        raise Exception(f"Error decoding response: {e}")
    if isinstance(results, dict) and "error" in results:
        raise Exception(results["error"])
    generated_text = results[0]["generated_text"] if isinstance(results, list) and "generated_text" in results[0] else "No text generated"
    return generated_text

def truncate_text(text, word_limit):
    words = text.strip().split()
    return " ".join(words[:word_limit])

def print_menu():
    print(f"{Style.BRIGHT}{Fore.GREEN}==Menu==\nSelect Output type\n1.Caption (5 words)\n2.Description (30 words)\n3.Summary (50 words)\n4.Exit")

def main():
    image_path = input(f"{Fore.YELLOW}Enter the path to the image: ")
    if not os.path.exists(image_path):
        print(f"{Fore.RED}Error: File not found at {image_path}")
        return
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"{Fore.RED}Error opening image: {e}")
        return
    basic_caption = get_basic_caption(image)
    print(f"{Fore.YELLOW}Basic Caption: {basic_caption}\n")
    while True:
        print_menu()
        choice = input(f"{Fore.YELLOW}Enter your choice: ")
        if choice == "1":
            caption = truncate_text(basic_caption, 5)
            print(f"{Fore.YELLOW}Caption: {caption}\n")
        elif choice == "2":
            prompt_text = f"Expand the following caption into a detailed description in exactly 30 words: {basic_caption}"
            try:
                generated = generate_text(prompt_text, max_tokens=40)
                description = truncate_text(generated, 30)
                print(f"{Fore.YELLOW}Description: {description}\n")
            except Exception as e:
                print(f"{Fore.RED}Error generating description: {e}")
        elif choice == "3":
            prompt_text = f"Summarize the following caption into a detailed summary in exactly 50 words: {basic_caption}"
            try:
                generated = generate_text(prompt_text, max_tokens=60)
                summary = truncate_text(generated, 50)
                print(f"{Fore.YELLOW}Summary: {summary}\n")
            except Exception as e:
                print(f"{Fore.RED}Error generating summary: {e}")
        elif choice == "4":
            print(f"{Fore.YELLOW}Exiting...")
            break
        else:
            print(f"{Fore.RED}Invalid choice. Please select a valid option")

if __name__ == "__main__":
    main()