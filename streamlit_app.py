import streamlit as st
import os
from dotenv import load_dotenv
import requests
from PIL import Image
from io import BytesIO
import base64

load_dotenv()
st.set_page_config(page_title="AI Image Generator", layout="wide")

st.markdown("""
<style>
    body {
        color: #FFFFFF;
        background-color: #000000;
    }
    .stButton>button {
        color: #FFFFFF;
        background-color: #0066CC;
        border-color: #0066CC;
    }
    .stSlider>div>div>div>div {
        background-color: #0066CC;
    }
    .stProgress>div>div>div>div {
        background-color: #0066CC;
    }
    .model-button {
        position: relative;
        width: 100%;
        height: 100px;
        margin-bottom: 10px;
        overflow: hidden;
        cursor: pointer;
        border-radius: 10px;
    }
    .model-button img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }
    .model-button .button-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        background-color: rgba(0,0,0,0.5);
        padding: 5px 10px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("About")
    st.write("Created by BoiCodes")
    st.write("This project has been an incredibly rewarding experience that has taught me a great deal. Throughout the development process, I leveraged various AI tools to assist with coding, which not only enhanced the efficiency of the project but also provided valuable insights into AI-assisted development practices. This approach allowed me to create a more robust and feature-rich application while simultaneously expanding my knowledge and skills in both AI and software development.")
    st.write("[Visit my GitHub](https://github.com/Boilovestech)")

# Main content
st.title("LostWonders AI 🖼️🤖 (version 1.0.0)")

model_name = st.session_state.get('model_name', None)

def set_model(name):
    st.session_state['model_name'] = name

# Function to create a model button
def model_button(title, image_path, model):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    
    button_html = f"""
    <div class="model-button" onclick="document.getElementById('{model}').click()">
        <img src="data:image/png;base64,{encoded_image}" alt="{title}">
        <div class="button-text">{title}</div>
    </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)
    if st.button("Select", key=model, help=f"Select {title} model"):
        set_model(model)

# Input for prompt
prompt = st.text_area("Enter your prompt", height=100)

# Model selection buttons
st.subheader("Model Selection")

# Create model buttons
model_button("SDXL Flash", "image1.png", "sd-community/sdxl-flash")
model_button("Stable Diffusion v1.5", "image2.jpg", "runwayml/stable-diffusion-v1-5")
model_button("Kolors", "image3.webp", "Kwai-Kolors/Kolors")

# Display selected model
if model_name:
    st.write(f"Selected model: {model_name}")

# Advanced options
st.subheader("Advanced Options")
num_inference_steps = st.slider("Number of inference steps", 1, 100, 50)
guidance_scale = st.slider("Guidance scale", 1.0, 20.0, 7.5, 0.1)
negative_prompt = st.text_area("Negative prompt")
width = st.slider("Image width", 256, 1024, 512, 64)
height = st.slider("Image height", 256, 1024, 512, 64)

# Function to generate image using Hugging Face Inference API
def generate_image(prompt, model_name, num_inference_steps, guidance_scale, negative_prompt, width, height):
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"authorization": f"Bearer {st.secrets['HUGGINGFACE_API_KEY']}"}

    payload = {
        "inputs": prompt,
        "negative_prompt": negative_prompt,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale,
        "width": width,
        "height": height
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    try:
        image = Image.open(BytesIO(response.content))
        return image
    except Exception as e:
        raise Exception(f"Failed to process the image: {str(e)}")

# Generate button
# Number of images selection
st.subheader("Number of Images")
num_images = st.radio("Select number of images to generate:", (1, 2, 3), horizontal=True)

# Set background image
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom right, #000000, #01386E);
        background-attachment: fixed;
    }
</style>
""", unsafe_allow_html=True)

if st.button("Generate Image"):
    if prompt and model_name:
        with st.spinner("Generating image(s)..."):
            progress_bar = st.progress(0)
            for i in range(100):
                progress_bar.progress(i + 1)
            try:
                for _ in range(num_images):
                    image = generate_image(prompt, model_name, num_inference_steps, guidance_scale, negative_prompt, width, height)
                    st.image(image, caption="Generated Image", use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a prompt and select a model.")
