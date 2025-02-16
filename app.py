from flask import Flask, request, send_file, render_template
from TTS.api import TTS
import os
import uuid

app = Flask(__name__)

# Load the Turkish TTS model
def load_model():
    return TTS(model_name="tts_models/tr/common-voice/glow-tts", progress_bar=False, gpu=False)

tts = load_model()

# Home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if not text:
            return render_template("index.html", error="Please enter some text.")
        
        # Generate a unique filename
        output_file = f"output_{uuid.uuid4().hex}.wav"
        
        try:
            # Generate speech
            tts.tts_to_file(text=text, file_path=output_file)
            
            # Provide the audio file for download
            return send_file(
                output_file,
                as_attachment=True,
                download_name=output_file,
                mimetype="audio/wav"
            )
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {e}")
        finally:
            # Clean up the file
            if os.path.exists(output_file):
                os.remove(output_file)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)