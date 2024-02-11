import pprint
import time
import json
import requests
import streamlit as st
from uuid import uuid4
from PIL import Image
from io import BytesIO
import os

api_key = st.secrets["LEONARDO_API_KEY"]
authorization = "Bearer %s" % api_key
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

def generate_images(image_bytes: bytes):
    # print("image_file_path:", image_file_path)
    # Get a presigned URL for uploading an image
    print("-" * 100)
    url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
    payload = {"extension": "png"}
    response = requests.post(url, json=payload, headers=headers)
    print(f"Get a presigned URL for uploading an image: {response.status_code}")
    pprint.pprint(response.json())

    # Upload image via presigned URL
    print("-" * 100)
    fields = json.loads(response.json()['uploadInitImage']['fields'])
    url = response.json()['uploadInitImage']['url']
    image_id = response.json()['uploadInitImage']['id']  # For getting the image later
    # files = {'file': open(image_file_path, 'rb')}
    response = requests.post(url, data=fields, files={'file': image_bytes}) # Header is not needed
    print(F"Upload image via presigned URL: {response.status_code}")
    print(image_id)

    # Generate with an image prompt
    print("-" * 100)
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    payload = {
        "height": 888,
        "modelId": "1e60896f-3c26-4296-8ecc-53e2afecc132", # Setting model ID to Leonardo Creative
        "prompt": "As per image, tattoo, no person, white background",
        "width": 888,
        "init_image_id": image_id, # Accepts an array of image IDs
        "num_images": 2,
        "init_strength": 0.4,
        "presetStyle": "LEONARDO"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Generated with an image prompt: {response.status_code}")
    print(response.content)

    # Get the generation of images
    print("-" * 100)
    generation_id = response.json()['sdGenerationJob']['generationId']

    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            time.sleep(1.5)
            continue
        else:
            if not response.json()['generations_by_pk']['generated_images']:
                continue

        print(f"Get the generation of images: {response.status_code}")
        print(response.text)
        print(url)
        pprint.pprint(response.json())
        body = response.json()
        generated_images = body['generations_by_pk']['generated_images']
        for generated_image in generated_images:
            generated_image_url = generated_image['url']

            response = requests.get(generated_image_url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                st.image(image, width=400)
            else:
                st.error("Failed to fetch the image from URL")

        break


def main():
    st.title("Tattoo")

    image = st.file_uploader("Upload a tattoo image", type=['png', 'jpg', 'jpeg'])
    if image:
        st.image(image, caption="Original Tattoo image", width=400)
    prompt = st.text_input("Prompt text")

    upload_button = st.button("Generate Tattoos")

    if upload_button:
        if image and prompt:
            # Upload image
            image_id = uuid4().hex
            image_bytes = image.read()
            # image_path = f"saved/{image_id}.png"
            # with open(image_path, "wb") as f:
            #     f.write(image.read())
            
            generate_images(image_bytes)
            
        else:
            pass

if __name__ == '__main__':
    main()