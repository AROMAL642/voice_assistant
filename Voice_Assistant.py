
# importing speech recognition package from google api
import speech_recognition as sr
import playsound # to play saved mp3 file
from gtts import gTTS # google text to speech
import os # to save/open files
import wolframalpha # to calculate strings into formula
from selenium import webdriver # to control browser operations
import pyttsx3
import vosk
import pyaudio
import requests
import pickle
import cv2
import subprocess
import re





#def load_and_cache_directory(directory_path, cache_file):
 #   if os.path.exists(cache_file):
       
  #      with open(cache_file, 'rb') as f:
   #         cached_data = pickle.load(f)
    #    print(f"Loaded directory from cache: {directory_path}")
      #  return cached_data

    #if os.path.exists(directory_path) and os.path.isdir(directory_path):
      
     #   loaded_directory = os.listdir(directory_path)

        
    #    with open(cache_file, 'wb') as f:
     #       pickle.dump(loaded_directory, f)
      #  print(f"Cached directory: {directory_path}")
       # return loaded_directory

   # else:
    #    print("The specified path does not exist or is not a directory.")
     #   return []

#if __name__ == "__main__":
 #   directory_path = "/home/aromal/Desktop/voice_assistant_project/vosk-model-en-in-0.5"
  #  cache_file = "directory_cache.pkl"

   
#directory=load_and_cache_directory(directory_path,cache_file)








num = 1
name="Aliya"
def assistant_name():
	name="I am liya"
	speak_online_or_offline(name)

#"/home/aromal/Desktop/voice_assistant_project/vosk-model-en-in-0.5"

def is_internet_available():
    try:
        
        response = requests.get("https://www.google.com", timeout=2)
       
        return response.status_code == 200
    except requests.ConnectionError:
        
        return False

def assistant_speaks(output):                      #speak on online
	global num

	num += 1
	print(name,":",output)

	toSpeak = gTTS(text = output, lang ='en', slow = False)

	file = str(num)+".mp3"
	toSpeak.save(file)
	playsound.playsound(file, True)
	os.remove(file)
 
def speak(output):# offline speaking
   
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  
    engine.setProperty("volume", 1.0)
    voice =engine.getProperty('voices')
    engine.setProperty('voice', 'english+f4') #mb-us1,us-mbrola-1,english+f4
    engine.say(output)
    engine.runAndWait()
    
def offline_sr(model_path="/home/aromal/Desktop/voice_assistant_project/vosk-model-en-in-0.5",sample_rate=16000,):    #offline voice Recognizer

    if not os.path.exists(model_path):
        print(f"Vosk model not found at {model_path}")
        return

    vosk_model = vosk.Model(model_path)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=1024)
    recognizer = vosk.KaldiRecognizer(vosk_model, sample_rate)
    print("Listening...")

    try:
        while True:
            data = stream.read(1024)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                recognized_text = str(result)
                print(f"Recognized: {recognized_text}")
                return(recognized_text)
                
    except KeyboardInterrupt:
        pass

    print("Recognition finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()




def get_audio():                          #online voice Recognizer

	rObject = sr.Recognizer()
	audio = ''

	with sr.Microphone() as source:
		print("Speak...")
		
		audio = rObject.listen(source, phrase_time_limit = 4)
	print("Stop.") # 

	try:

		text = rObject.recognize_google(audio, language ='en-US')
		print("You : ", text)
		return text

	except:

		speak_online_or_offline("Could not understand your audio, PLease try again !")
		return 0
    
 

def speak_online_or_offline(output):
    if is_internet_available():
        assistant_speaks(output)
    else:
        speak(output)
        
def recognize_online_or_offline():
    if is_internet_available():
        
        return get_audio()
    else:
        return offline_sr()        


		
def calculate_numbers(text):
	word_list_calculation={"1","2","3","4","5","6","6","7","8","9","0"}
	words_in_sentence = text.split()
	print(words_in_sentence)
	numbers = []
	
	for word in words_in_sentence:
		if word in word_list_calculation:
			numbers.append(word)
			print(numbers)
		#query = text.replace(str(word_list_addition), "").strip()
		break





def opensettings(text):
	if "settings" in text.lower():

		assistant_speaks("settings app oppened")
		subprocess.run(['gnome-control-center'])
	
	return recognize_online_or_offline()











def search():
	
	driver = webdriver.Firefox()
	driver.implicitly_wait(1)
	driver.maximize_window()

	if 'youtube' in str(text):

		speak_online_or_offline("Opening in youtube")
	    
		query = text.replace("search", "").strip()
		speak_online_or_offline(query)
		driver.get(f"https://www.youtube.com/results?search_query={query}")
		return

	elif 'google' in str(text):
		speak_online_or_offline("Searching on google...pleace wait")
        
		word_list={"search","search in","in google","find in","find","on google"}
		query = text.replace(word_list, "").strip()
		speak_online_or_offline(query)
		driver.get("https://www.google.com/search?client=firefox-b-e&q={query}")
		return	
	
	elif 'firefox' in str(text) or 'search on web' in str(text) or 'search' in str(text):
		speak_online_or_offline("Searching on Web...pleace wait")
        

		word_list={"search","search in","in firefox","find in","find","on firefox"}
		query = text.replace(str(word_list), "").strip()
		speak_online_or_offline(query)
		driver.get(f"https://www.google.com/search?client=firefox-b-e&q={query}")
		return
   

if __name__ == "__main__":

	speak_online_or_offline("Can I Help You Sir?")
	answer=recognize_online_or_offline()
           
    
	if "yes" in str(answer) or "of course" in str(answer) or "sure" in str(answer) or "yeah" in str(answer) or "ok" in str(answer):
		access="grant"
	
	
 
while(access=="grant"):

		speak_online_or_offline("What can i do for you?")
		text = recognize_online_or_offline().lower()

		if text == 0:
			continue
		
		elif "who are you" in str(text) or "deffine yourself" in str(text):
			speak_online_or_offline('''Hello, I am a virtual Person. Your personal Assistant.
		    Developed by Aromal''')
			continue
		
		
		elif "who made you" in str(text) or "who developed you" in str(text) or "who invent" in str(text):
			speak_online_or_offline('''The one and only Genious Aromal''')
			continue
			
		elif "what is your name" in str(text) or "your name" in str(text) or "name of you" in str(text):
		
			assistant_name()
			continue
		elif (name) in str(text) or ("who is" +name) in str(text) or "who are you" in str(text):
			assistant_name()
			continue

		elif "search" in str(text) or "find" in str(text)or "play" in str(text):
			speak_online_or_offline("Iam Trying to find your Result...Pleace wait..")
			search()
			continue
    

		elif "exit" in str(text) or "bye" in str(text) or "sleep" in str(text)or "shut up" in str(text)or "get lost" in str(text)or "leave me" in str(text) or "nothing" in str(text):
			speak_online_or_offline("Ok bye, ")
			break
      
		elif "calculate" in str(text) or "multiply" in str(text) or "devide" in str(text)or "add" in str(text)or "substract" in str(text):
			calculate_numbers(text)
			break
		elif "open" in str(text) or "run" in str(text) or "goto" in str(text):
			opensettings(text)
			break

		elif "set" in str(text) or "make" in str(text) or "adjust" in str(text):
			extract_numbers(text)
			break









            
	
		
def process_text(text):
	try:
	
		if "calculate" in text.lower():
			
			# write your wolframalpha app_id here
			app_id = "WOLFRAMALPHA_APP_ID"
			client = wolframalpha.Client(app_id)

			indx = input.lower().split().index('calculate')
			query = input.split()[indx + 1:]
			res = client.query(' '.join(query))
			answer = next(res.results).text
			assistant_speaks("The answer is " + answer)
			return

		elif 'open' in input:
			
			# another function to open
			# different application available
			open_application(input.lower())
			return

		else:

			assistant_speaks("I can search the web for you, Do you want to continue?")
			ans = offline_sr()
			if 'yes' in str(ans) or 'yeah' in str(ans):
				search_web(input)
			else:
				return
	except :

		assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
		ans = offline_sr()
		if 'yes' in str(ans) or 'yeah' in str(ans):
			search_web(input)
def search_web(text):

	driver = webdriver.Firefox()
	driver.implicitly_wait(1)
	driver.maximize_window()

	if 'youtube' in str(text):

		assistant_speaks("Opening in youtube")
		indx = input.lower().split().index('youtube')
		query = input.split()[indx + 1:]
		driver.get("http://www.youtube.com/results?search_query =" + '+'.join(query))
		return

	elif 'wikipedia' in input.lower():

		assistant_speaks("Opening Wikipedia")
		indx = input.lower().split().index('wikipedia')
		query = input.split()[indx + 1:]
		driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
		return

	else:

		if 'google' in input:

			indx = input.lower().split().index('google')
			query = input.split()[indx + 1:]
			driver.get("https://www.google.com/search?q =" + '+'.join(query))

		elif 'search' in input:

			indx = input.lower().split().index('google')
			query = input.split()[indx + 1:]
			driver.get("https://www.google.com/search?q =" + '+'.join(query))

		else:

			driver.get("https://www.google.com/search?q =" + '+'.join(input.split()))

		return


# function used to open application
# present inside the system.
def open_application(input):

	if "chrome" in input:
		assistant_speaks("Google Chrome")
		os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
		return

	elif "firefox" in input or "mozilla" in input:
		assistant_speaks("Opening Mozilla Firefox")
		os.startfile('C:\Program Files\Mozilla Firefox\\firefox.exe')
		return

	elif "word" in input:
		assistant_speaks("Opening Microsoft Word")
		os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Word 2013.lnk')
		return

	elif "excel" in input:
		assistant_speaks("Opening Microsoft Excel")
		os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\\Excel 2013.lnk')
		return

	else:

		assistant_speaks("Application not available")
		return
