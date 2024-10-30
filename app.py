import os
import streamlit as st
import base64
from openai import OpenAI

# Function to encode the image to base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

# Page configuration
st.set_page_config(page_title="Análisis de Imagen", layout="centered", initial_sidebar_state="expanded")

# Title and header
st.title("🖼️ Análisis de Imagen: 🤖🏞️")
st.write("Sube una imagen y proporciona contexto adicional para recibir un análisis detallado.")

# Input for OpenAI API key
api_key = st.text_input('🔑 Ingresa tu Clave de API de OpenAI', type="password")

# Initialize OpenAI client
if api_key:
    client = OpenAI(api_key=api_key)

# Image uploader
uploaded_file = st.file_uploader("📤 Sube una imagen", type=["jpg", "png", "jpeg"], label_visibility="visible")

if uploaded_file:
    st.image(uploaded_file, caption="Imagen subida", use_column_width=True)

# Toggle for showing additional details input
show_details = st.checkbox("📝 Agregar detalles sobre la imagen", value=False)

if show_details:
    additional_details = st.text_area("🔍 Contexto adicional de la imagen:", "")

# Button to trigger the analysis
analyze_button = st.button("🔍 Analizar imagen")

if uploaded_file and api_key and analyze_button:
    with st.spinner("Analizando ..."):
        base64_image = encode_image(uploaded_file)
        prompt_text = "Describe lo que ves en la imagen en español."
        if show_details and additional_details:
            prompt_text += f"\n\nContexto adicional proporcionado: {additional_details}"

        # Create messages for the request
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ]

        # Make the request to the OpenAI API
        try:
            # Streaming response
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4-vision-preview", messages=messages, max_tokens=1200, stream=True
            ):
                if completion.choices[0].delta.content:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Ha ocurrido un error: {e}")

# Warnings for user action required
if not uploaded_file and analyze_button:
    st.warning("⚠️ Por favor, sube una imagen.")
if not api_key:
    st.warning("⚠️ Por favor, ingresa tu clave de API.")
