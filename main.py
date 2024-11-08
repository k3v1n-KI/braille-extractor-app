from flask import Flask, render_template, request, flash
from braille_to_text import braille_to_text
from text_to_speech import text_to_speech

app = Flask(__name__)
app.secret_key = "Something Ominous"

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

if __name__ == "__main__":
    app.run(debug=True)
    