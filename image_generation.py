# image_generation.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_image_with_nvidia_nim(prompt):
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/66941524-29ae-4045-8e66-0bc8f41889e1"
    headers = {
        "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",
        "Accept": "application/json",
    }
    payload = {
        "prompt": prompt,
        "cfg_scale": 5,
        "aspect_ratio": "16:9",
        "seed": 0,
        "steps": 50,
        "negative_prompt": ""
    }
    response = requests.post(invoke_url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()