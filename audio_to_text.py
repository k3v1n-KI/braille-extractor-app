import speech_recognition as sr
import sys

filename = sys.argv[1]

# initialize the recognizer
r = sr.Recognizer()

# open the file
with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    # IMPORTANT: Change the path!!
    f = open("C:/Projetos/Assignment2-Part2-Braille/Audio-to-text.txt", "w")   # 'r' for reading and 'w' for writing
    f.write(text)    # Write inside file 
    f.close()
    print(text)