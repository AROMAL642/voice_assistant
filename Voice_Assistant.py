
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

num = 1




def speak_on_or_off(output):
    try:
      
        response = requests.get('http://www.google.com', timeout=5)
        if response.status_code==200:
            
            assistant_speaks(output)
        else:
           
           speak(output)  
        
    except requests.ConnectionError:
        return False
        

                    
        
def recognize_on_or_off():
    try:
        # Send a request to a reliable online service (e.g., Google DNS)
        response = requests.get('http://www.google.com', timeout=5)
    
        r="true"
        if r=="true":
         get_audio()
        else:
        
         offline_sr()
    except requests.ConnectionError:
        print("error")
            



def speak(output):# offline speaking
   
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  
    engine.setProperty("volume", 1.0)
    voice =engine.getProperty('voices')
    engine.setProperty('voice', 'english+f4') #mb-us1,us-mbrola-1,english+f4
    engine.say(output)
    engine.runAndWait()
    
    
def assistant_speaks(output):                      #speak on online
	global num

	num += 1
	print("PerSon : ", output)

	toSpeak = gTTS(text = output, lang ='en', slow = False)

	file = str(num)+".mp3"
	toSpeak.save(file)
	playsound.playsound(file, True)
	os.remove(file)
    



def offline_sr(model_path="/home/aromal/vosk-model-small-en-us-0.15",sample_rate=16000):    #offline voice Recognizer

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
		
		# recording the audio using speech recognition
		audio = rObject.listen(source, phrase_time_limit = 5)
	print("Stop.") # limit 5 secs

	try:

		text = rObject.recognize_google(audio, language ='en-US')
		print("You : ", text)
		return text

	except:

		speak_on_or_off("Could not understand your audio, PLease try again !")
		return 0


# Driver Code
name="Aliya"
def assistant_name():
	name="I am liya"
	speak_on_or_off(name)



def search():
	
	driver = webdriver.Firefox()
	driver.implicitly_wait(1)
	driver.maximize_window()

	if 'youtube' in str(text):

		speak_on_or_off("Opening in youtube")
	    
		query = text.replace("search", "").strip()
		speak_on_or_off(query)
		driver.get(f"https://www.youtube.com/results?search_query={query}")
		return

	elif 'google' in str(text):
		speak_on_or_off("Searching on google...pleace wait")
        
		word_list={"search","search in","in google","find in","find","on google"}
		query = text.replace(word_list, "").strip()
		speak_on_or_off(query)
		driver.get("https://www.google.com/search?client=firefox-b-e&q={query}")
		return	
	
	elif 'firefox' in str(text) or 'search on web' in str(text) or 'search' in str(text):
		speak_on_or_off("Searching on Web...pleace wait")
        

		word_list={"search","search in","in firefox","find in","find","on firefox"}
		query = text.replace(str(word_list), "").strip()
		speak_on_or_off(query)
		driver.get(f"https://www.google.com/search?client=firefox-b-e&q={query}")
		return
   

if __name__ == "__main__":

	speak_on_or_off("Can I Help You Sir?")
	answer=recognize_on_or_off()
	if "yes" in str(answer) or "of course" in str(answer) or "sure" in str(answer) or "yeah" in str(answer) or "ok" in str(answer):
		access="grant"
	
	
	while(access=="grant"):

		speak_on_or_off("What can i do for you?")
		text = recognize_on_or_off().lower()

		if text == 0:
			continue
		
		elif "who are you" in str(text) or "deffine yourself" in str(text):
			speak_on_or_off('''Hello, I am a virtual Person. Your personal Assistant.
		    Developed by Aromal''')
			continue
		
		
		elif "who made you" in str(text) or "who developed you" in str(text) or "who invent" in str(text):
			speak_on_or_off('''The one and only Genious Aromal''')
			continue
			
		elif "what is your name" in str(text) or "your name" in str(text) or "name of you" in str(text):
		
			assistant_name()
			continue
		elif (name) in str(text) or ("who is" +name) in str(text) or "who are you" in str(text):
			assistant_name()
			continue

		elif "search" in str(text) or "find" in str(text)or "play" in str(text):
			speak_on_or_off("Iam Trying to find your Result...Pleace wait..")
			search()
			continue	

		elif "exit" in str(text) or "bye" in str(text) or "sleep" in str(text)or "shut up" in str(text)or "get lost" in str(text)or "leave me" in str(text) or "nothing" in str(text):
			speak("Ok bye, ")
			break














            
		# calling proceses text to process the query
		
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
