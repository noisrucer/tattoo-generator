import json
import requests
import time

api_key = "35657856-b1ae-4894-a80d-2523fedd0d9a"
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# # Get a presigned URL for uploading an image
# url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

# payload = {"extension": "png"}

# response = requests.post(url, json=payload, headers=headers)

# print(response.status_code)

# # Upload image via presigned URL
# fields = json.loads(response.json()['uploadInitImage']['fields'])

# url = response.json()['uploadInitImage']['url']

# image_id = response.json()['uploadInitImage']['id']  # For getting the image later

# image_file_path = "./image2.png"
# files = {'file': open(image_file_path, 'rb')}

# response = requests.post(url, data=fields, files=files) # Header is not needed

# print(response.status_code)

# # Generate with an image prompt
# url = "https://cloud.leonardo.ai/api/rest/v1/generations"

# payload = {
#     "height": 512,
#     "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", # Setting model ID to Leonardo Creative
#     "prompt": "As per image, tattoo, no person, white background",
#     "width": 512,
#     "imagePrompts": [image_id], # Accepts an array of image IDs,
#     "initStrength": 0.5
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.status_code)

# # Get the generation of images
# generation_id = response.json()['sdGenerationJob']['generationId']

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % "caf349c0-e1b4-454b-88d7-9f5960debf9b"

# time.sleep(20)

response = requests.get(url, headers=headers)

print(response.text)
