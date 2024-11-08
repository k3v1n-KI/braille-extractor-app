from flask import Flask, render_template, request, flash
from braille_image_to_text import driver as braille_image_to_text
from text_to_speech import text_to_speech
from time import time

app = Flask(__name__)
app.secret_key = "Something Ominous"

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
            
            # Convert braille text to english
            english_text = braille_image_to_text(file_path)
            
            # Create and save an mp3 file of the text
            text_to_speech(english_text, file_name)
            
            # Send all info to the web application
            return render_template("index.html", image=file_name, english_text=english_text)
        except:
            flash("Problem processing image file", "error")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
