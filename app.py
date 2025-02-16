import streamlit as st
from TTS.api import TTS
import os
import uuid

# Load the Turkish TTS model
@st.cache_resource
def load_model():
    return TTS(model_name="tts_models/tr/common-voice/glow-tts", progress_bar=False, gpu=False)

tts = load_model()

# Streamlit app
st.title("Turkish Text-to-Speech with Coqui TTS")
st.write("Enter Turkish text below and click 'Generate Speech' to hear the audio.")

# Text input from the user
text = st.text_area("Enter Turkish text:", "Merhaba, bu bir deneme metnidir.")

# Generate speech when the user clicks the button
if st.button("Generate Speech"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Generate a unique filename to avoid conflicts
        output_file = f"output_{uuid.uuid4().hex}.wav"
        
        # Generate speech
        try:
            tts.tts_to_file(text=text, file_path=output_file)
            st.success("Speech generated successfully!")
            
            # Play the generated audio
            st.audio(output_file, format="audio/wav")
            
            # Provide a download link
            with open(output_file, "rb") as file:
                st.download_button(
                    label="Download Audio",
                    data=file,
                    file_name=output_file,
                    mime="audio/wav"
                )
            
            # Clean up the file after use
            os.remove(output_file)
        except Exception as e:
            st.error(f"An error occurred: {e}")