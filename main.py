from flask import Flask, render_template, request, flash
from braille_image_to_text import driver as braille_image_to_text
import os
from pydub import AudioSegment
from braille_to_text import braille_to_text
from text_to_speech import text_to_speech
from speech_to_text import get_large_audio_transcription_fixed_interval
from braille_to_text import text_to_braille, braille_to_text
from time import time

app = Flask(__name__)
app.secret_key = "Something Ominous"

# For windows ffmpeg
# AudioSegment.ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"

# For linux ffmpeg
AudioSegment.ffmpeg = "/usr/bin/ffmpeg"


@app.route("/", methods=["GET"])
def home_page():
    return render_template("index.html")

@app.route("/text_to_braille", methods=["GET", "POST"])
def text_to_braille_page():
    # Post request to get the image
    if request.method == "POST":
        conversion = request.form.to_dict()
        
        if conversion["text"].strip() == "":
            flash("Failed to translate text, no text given", "danger")
        else:
            if conversion["type"] == '0':
                text = text_to_braille(conversion["text"])
            else:
                text = braille_to_text(conversion["text"])
            
            return render_template("text_to_braille.html", text=text)
    return render_template("text_to_braille.html")

@app.route("/braille_image_to_text", methods=["GET", "POST"])
def braille_image_to_text_page():
    # Post request to get the image
    if request.method == "POST":
        image_file = request.files["brailleImage"]
        
        # Get image file or set a default filename
        file_name = image_file.filename if image_file.filename else f"{time() * 10000}.jpeg"
        
        try:
            file_path = f"static/images/{file_name}"
            
            # Save image file
            image_file.save(file_path)
            
            flash("Image file processed successfully!", "success")
            
            # Convert image to braille text
            braille_text = braille_image_to_text(file_path)
            
            # Convert braille text to english
            english_text = braille_to_text(braille_text)
            
            # Create and save an mp3 file of the text
            text_to_speech(english_text, file_name)
            
            # Send all info to the web application
            return render_template("braille_image_to_text.html", image=file_name, braille_text=braille_text, english_text=english_text)
        except Exception as e:
            print(e)
            flash("Problem processing image file", "danger")

    return render_template("braille_image_to_text.html")

@app.route("/speech_to_braille", methods=["GET", "POST"])
def speech_to_braille_page():
    if request.method == "POST":
        audio_file = request.files['audioFile']
        file_name = audio_file.filename
        webm_file_path = f"static/audio/{file_name}"
        audio_file.save(webm_file_path)
        
        # Convert .webm to .wav using pydub
        wav_file_path = os.path.splitext(webm_file_path)[0] + ".wav"
        try:
            # Load the .webm file
            audio = AudioSegment.from_file(webm_file_path, format="webm")
            # Export the audio as .wav
            audio.export(wav_file_path, format="wav")
            flash("File uploaded successfully", "success")
            # Delete the .webm file after conversion
            os.remove(webm_file_path)
            # Convert speech to text
            text_from_wav_file = get_large_audio_transcription_fixed_interval(wav_file_path)
            
            # Convert text to braille
            braille_from_text = text_to_braille(text_from_wav_file)
        except Exception as e:
            flash(f"Error converting to wav file: {e}", "danger")
        return render_template("speech_to_braille.html", wav_file_path=wav_file_path, text_from_wav_file=text_from_wav_file, braille_from_text=braille_from_text)
        
    return render_template("speech_to_braille.html")

if __name__ == "__main__":
    app.run(debug=True)
