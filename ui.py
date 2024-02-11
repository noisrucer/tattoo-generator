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
    i = 0
    progress_text = "Image is being generated..."
    progress_bar = st.progress(0, text=progress_text)
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            time.sleep(1.5)
            progress_bar.progress(i + 1, text=progress_text)
            i += 1
            continue
        else:
            if not response.json()['generations_by_pk']['generated_images']:
                progress_bar.progress(i + 1, text=progress_text)
                i += 1
                continue
        progress_bar.progress(100, text = "Complete!")

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
    prompt = st.text_input("(선택) Prompt", placeholder="어떤 느낌의 타투를 원하는지 간략히 입력해주세요.")

    upload_button = st.button("Generate Tattoos")

    if upload_button:
        if image:
            if not prompt:
                prompt = "As per image, tattoo style, white background"
            # Upload image
            image_bytes = image.read()
            generate_images(image_bytes)
        else:
            pass

if __name__ == '__main__':
    main()