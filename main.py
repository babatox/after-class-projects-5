import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from config import API_KEY

def generate_image_from_prompt(prompt):
    API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3-medium-diffusers"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)
        return image
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise Exception("Failed to generate image")

def post_processing_image(image):
    enhancer = ImageEnhance.Brightness(image)
    bright_image = enhancer.enhance(1.2)

    enhancer = ImageEnhance.Contrast(bright_image)
    contrast_image = enhancer.enhance(1.3)

    soft_focus_image = contrast_image.filter(ImageFilter.GaussianBlur(radius=1))
    return soft_focus_image

def main():
    print("Welcome to our Image Workshop\nType 'exit' to quit.")
    while True:
        user_input = input("Enter a description for the image: ")
        if user_input.lower() == 'exit':
            print("Good bye")
            break

        try:
            print("Generating image...")
            image = generate_image_from_prompt(user_input)
            
            print("Processing image...")
            processed_image = post_processing_image(image)
            processed_image.show()

            save_option = input("Do you want to save the image? (yes/no): ")
            if save_option.lower() == 'yes':
                file_name = input("Enter the file name to save the image: ").strip()
                if not file_name.endswith(".png"):
                    file_name += ".png"
                processed_image.save(file_name)
                print(f"Image saved as {file_name}")
        except Exception as e:
            print(f"An error occurred: {e}\n")

if __name__ == "__main__":
    main()