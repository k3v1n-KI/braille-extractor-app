from gtts import gTTS

import os

# # Sample text in english
# mytext = 'That time I got reincarnated as a slime is the best isekai anime'

def text_to_speech(mytext, file_name="speech_output"):
    language = 'en'

    # Passing the text and language into gTTs
    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Saving the converted audio in an mp3 file
    myobj.save(f"static/audio/{file_name}.mp3")

# text_to_speech(mytext)
# # Playing the converted file
# os.system("start speech_output.mp3")
