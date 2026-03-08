import requests
import os
from config import API_KEY

MODEL_ID="Salesforce/blip-image-captioning-base"
URL = f"https://api-inference.huggingface.co/pipeline/image-to-text/{MODEL_ID}"

header={
    "Authorization":f"Bearer {API_KEY}"
}

def caption_single_image():
    
    image_source = os.path.join(os.path.dirname(__file__), "R.jpg")

    try:
        with open(image_source,"rb") as f:
            image_byte=f.read()
    except Exception as e:
        print(f"could not load image from {image_source}\nError:{e}")
        return

    try:
        response=requests.post(URL,headers=header,data=image_byte)
        results=response.json()
    except Exception as e:
        print(f"Request failed or invalid JSON response.\nError: {e}")
        if 'response' in locals():
            print(f"Status Code: {response.status_code}")
        return

    if isinstance(results,dict) and "error" in results:
        print(f"[Error]{results['error']}")
        return
    
    if isinstance(results, list) and len(results) > 0:
        caption=results[0].get("generated_text","No caption Found.")
        print("image",image_source)
        print("caption",caption)
    else:
        print(f"Unexpected result format: {results}")

if __name__=="__main__":
    caption_single_image()