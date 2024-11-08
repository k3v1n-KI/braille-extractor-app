import os
from flask import Flask, render_template, request, flash, redirect, url_for
from pydub import AudioSegment
from braille_to_text import braille_to_text
from text_to_speech import text_to_speech

app = Flask(__name__)
app.secret_key = "Something Ominous"

AudioSegment.ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"  

@app.route("/", methods=["GET", "POST"])
def home():
    # Post request to get the image
    if request.method == "POST":
        image_file = request.files["brailleImage"]
        # get image file
        file_name = image_file.filename
        if file_name != '':
            # Save image file
            image_file.save(f"static/images/{file_name}")
            flash("Image file processed successfully!", "success")
            # Extract braille text from image file
            braille_text = "⠠⠇⠑⠁⠧⠑⠎ ⠞⠥⠗⠝ ⠃⠗⠕⠺⠝ ⠁⠝⠙ ⠽⠑⠇⠇⠕⠺ ⠊⠝ ⠞⠓⠑ ⠋⠁⠇⠇. ⠠⠁⠙⠙ ⠞⠓⠑ ⠎⠥⠍ ⠞⠕ ⠞⠓⠑ ⠏⠗⠕⠙⠥⠉⠞ ⠕⠋ ⠞⠓⠑⠎⠑ ⠞⠓⠗⠑⠑." 
            # Convert braille text to english
            english_text = braille_to_text(braille_text)
            # Create and save an mp3 file of the text
            text_to_speech(english_text, file_name)
            # Send all info to the web application
            return render_template("index.html", image=file_name, braille_text=braille_text, english_text=english_text)
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
  