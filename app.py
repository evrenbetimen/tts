import streamlit as st
from TTS.api import TTS

# Load the Turkish TTS model
@st.cache_resource
def load_model():
    return TTS(model_name="tts_models/tr/common-voice/glow-tts", progress_bar=False, gpu=False)

tts = load_model()

# Streamlit app
st.title("Turkish Text-to-Speech with Coqui TTS")
text = st.text_area("Enter Turkish text:", "Merhaba, bu bir deneme metnidir.")

if st.button("Generate Speech"):
    output_file = "output.wav"
    tts.tts_to_file(text=text, file_path=output_file)
    st.audio(output_file, format="audio/wav")