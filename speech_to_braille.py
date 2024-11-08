import speech_recognition as sr
import sys
braille = ['⠴','⠂','⠆','⠒','⠲','⠢','⠖','⠶','⠦','⠔',
			'⠁','⠃','⠉','⠙','⠑','⠋','⠛','⠓','⠊','⠚',
			'⠅','⠇','⠍','⠝','⠕','⠏','⠟','⠗','⠎','⠞',
			'⠥','⠧','⠺','⠭','⠽','⠵',
			'⠱','⠰','⠣','⠿','⠀','⠮','⠐','⠼','⠫','⠩',
			'⠯','⠄','⠷','⠾','⠡','⠬','⠠','⠤','⠨','⠌',
			'⠜','⠹','⠈','⠪','⠳','⠻','⠘','⠸']
English = ['0','1','2','3','4','5','6','7','8','9',
			'a','b','c','d','e','f','g','h','i','j',
			'k','l','m','n','o','p','q','r','s','t',
			'u','v','w','x','y','z',
			':',';','<','=',' ','!','"','#','$','%',
			'&','','(',')','*','+',',','-','.','/',
			'>','?','@','[','\\',']','^','_']
def Braille2English(BrailleText) :
	return ''.join([English[braille.index(fi)] for ch in BrailleText for fi in braille if ch == fi])
def English2Braiile(EnglishText) :
	return ''.join([braille[English.index(fi)] for ch in EnglishText for fi in English if ch == fi])

duration = int(sys.argv[1])

# initialize the recognizer
r = sr.Recognizer()
print("Please talk")
with sr.Microphone() as source:
    # read the audio data from the default microphone
    audio_data = r.record(source, duration=duration)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data)
	# convert text to braille
    text_to_braille = English2Braiile(text)
    # IMPORTANT: Change the path!!
    f = open("C:/Projetos/Assignment2-Part2-Braille/Speech-to-braille.txt", "w", encoding='UTF-8')   # 'r' for reading and 'w' for writing
    f.write(text_to_braille)    # Write inside file 
    f.close()
    print(text_to_braille)