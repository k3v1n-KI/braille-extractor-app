import speech_recognition as sr
import sys

duration = int(sys.argv[1])

# initialize the recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    # read the audio data from the default microphone
    audio_data = r.record(source, duration=duration)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data)
    # IMPORTANT: Change the path!!
    f = open("C:/Projetos/Assignment2-Part2-Braille/Speech-to-text.txt", "w")   # 'r' for reading and 'w' for writing
    f.write(text)    # Write inside file 
    f.close()
    print(text)
