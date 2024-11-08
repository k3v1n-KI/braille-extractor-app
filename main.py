from flask import Flask, render_template, request, flash
from braille_image_to_text import driver as braille_image_to_text
import os
from pydub import AudioSegment
from braille_to_text import braille_to_text
from text_to_speech import text_to_speech
from time import time

app = Flask(__name__)
app.secret_key = "Something Ominous"

AudioSegment.ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"  

@app.route("/", methods=["GET", "POST"])
def home():
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
            return render_template("index.html", image=file_name, braille_text=braille_text, english_text=english_text)
        except Exception as e:
            print(e)
            flash("Problem processing image file", "error")

    return render_template("index.html")

@app.route("/speech_to_braille", methods=["GET", "POST"])
def speech_to_braille():
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
            
        except Exception as e:
            flash(f"Error converting to wav file: {e}", "error")
        return render_template("speech_to_braille.html", wav_file_path=wav_file_path)
        
    return render_template("speech_to_braille.html")

if __name__ == "__main__":
    app.run(debug=True)
