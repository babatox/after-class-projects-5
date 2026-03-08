import requests
from PIL import Image
from io import BytesIO
from config import API_KEY

API_URL="https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3-medium-diffusers"

def generate_image_from_text(promt: str)->Image.Image:
    header={"Authorization": f"Bearer {API_KEY}"}
    payload={"inputs":promt}

    try:
        response=requests.post(API_URL, headers=header, json=payload,timeout=30)
        response.raise_for_status()

        if 'image' in response.headers.get('Content-Type', ''):
            image=Image.open(BytesIO(response.content))
            return image
        else:
            raise Exception("the response is not an image, might be a error message")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request error: {e}")
    
def main():
    print("==WELCOME TO IMAGE GENERATOR==")
    print("Type 'exit' to quit the program\n")

    while True:
        prompt=input("Enter a description for the image you want to generate:\n ").strip()
        if prompt.lower()=="exit":
            print("Thank you for using oyr program")
            break
        print("generating image.......")                                            
    try:
            image=generate_image_from_text(prompt)
            image.show()

            save_option=input("Do you want to save the image? (yes/no): ").strip().lower()
            if save_option=='yes':
                file_name=input("enter image name: ").strip()
                file_name="".join(c for c in file_name if c.isalnum() or c in ('_',"-")).strip()
                image.save(f"{file_name}.png")
                print(f"image saved as {file_name}.png")
            else:
                print("image not saved")
    except Exception as e:
            print(f"An error occured: {e}")
            
if __name__=="__main__":
    main()


