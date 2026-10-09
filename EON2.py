import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import openAI
from gtts import gTTS
import pygame
import os


import random 
ai_choice = random.choice(["rock", "paper", "scissors"])


# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your Key Here>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(50)
    
    pygame.mixer.music.unload()5
    os.remove("temp.mp3") 

def aiProcess(command):
    openAI.api_key = "your_api_key_here"

    response = openAI.Completion.create(
    model="text-davinci-003",
    prompt="Hello!",
    max_tokens=10
    )

    return response.choices[0].text

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open news" in c.lower():
        webbrowser.open("https://www.aajtak.in/livetv")
    elif c.lower().startswith("play music"):
        song = c.lower().split(" ")[3]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    
    
    elif "Say some Jokes" in c.lower():
        # Use random function for one joke
        speak('''Teacher: Agar tumhare paas 5 aam hain, aur main 2 aam le loon… to tumhare paas kitne aam bachenge?
            Student: 5
            Teacher: Bewakoof! Soch ke bata!
            Student: Sir, aap aam lenge hi nahi. Aap to hamesha lecture lete ho!''')
        
        speak('''Santa: Mere sapne mein ek bhoot aaya, aur mujhe dara ke chala gaya!
            Banta: Phir kya kiya?
            Santa: Main ne bhi uske sapne mein chala gaya… aur EMI bharne ko keh diya!''')
        speak('''Wife: Tum mujhe gift mein kya doge birthday pe?
                Husband: Tum kya chaho?
                Wife: Kuch aisa jo 0 se 100 tak sirf 3 second mein pahunch jaye!
                Husband: (next day) Weight Machine le aaya!''')
        speak('''Boss: Tum late kyun aaye ho office?
                Employee: Sir, alarm nahi baja!
                Boss: Alarm tumhara kaam kare ya tum?
                Employee: Sir, teamwork hona chahiye!''')
    elif "What is AI ?" in c.lower():
        speak('''AI means when computers or machines start doing things that normally need human intelligence — like thinking, learning, solving problems, or understanding language.
        Asaan bhaasha mein AI ek aisi technology hai jo machines ko thoda "smart" banati hai.
        Jaise tum apna dimaag use karte ho, waise hi AI machine ko thoda dimaag deta hai — ki wo khud se kaam kar sake..''')
    
    elif "Tell me the weather forecast" in c.lower():
        speak('''Dopahar mein zyada dhoop hogi, to hydrated rahna zaroori hai.
            Subah ya raat ko agar bahar nikal rahe ho to ek light jacket rakh lena.
            Shaam ko open area mein walk karna accha idea ho sakta hai!''') 
        
    elif "Hey Jarvis, let's play Rock, Paper, Scissors." in c.lower():

        if "rock"== ai_choice:
            result = "It's a draw!"
        if "paper" == ai_choice:
            result = "It's a draw!"
        if "scissors" == ai_choice:
            result = "It's a draw!"
        
        elif "rock" and ai_choice == "scissors" or \
            "paper" and ai_choice == "rock" or \
            "scissors" and ai_choice == "paper":
                result = "You win!"
        else:
            result = "I win!"

        speak(result)

    elif "Tell me a story" in c.lower():
        speak('''
            "Ek baar ki baat hai... ek gehre jungle mein, jahan har taraf ped-paudhe, pakshiyon ki awaaz aur ajeeb sounds the... ek chhota sa robot tha, jiska naam tha Zeno."
            "Zeno jungle mein kho gaya tha. Uska jetpack jungle ke upar se jaate waqt crash ho gaya. Battery low thi, aur use ghar ka rasta bhi nahi pata tha."

            "Tabhi usne ek ajeeb si awaaz suni... ‘whoooosh… click-click…’
            Yeh awaaz kisi janwar ki nahi thi... yeh toh ek doosre robot ki thi!"

            "Can you guess... woh doosra robot kis color ka tha?
            Koi bhi ek color bolo!"

            (Model waits for user input, then playfully responds)
            "Aha! Tumne kaha red? Accha choice hai!
            Lekin asal mein, woh robot tha silver — chamakdaar, chaand jaisa!"

            (Tone: Friendly)
            "Us silver robot ka naam tha Vee.
            Vee bola, ‘Chinta mat karo Zeno, mujhe rasta pata hai. Mere saath chalo!’"

            (SFX idea: Jungle footsteps, river sounds)
            "Phir dono saath-saath chale — nadiya paar ki, pahadiyan chadhi, aur ek baar to kuch jungli bandar bhi unka peecha karne lage... sirf unko gudgudi karne ke liye!" 😄

            (Tone: Happy)
            "Aakhirkaar, Zeno ne dekha ek chamakdaar platform — uska home base!
            Usne pichhe mudkar kaha, ‘Thank you Vee, tum na hote to main hamesha ke liye kho jaata!’"

            "Vee muskuraya aur bola, ‘Doston ka kaam hi hota hai madad karna.’"

            "Aur us din ke baad, Zeno kabhi jungle se nahi darra...
            kyunki use pata tha — koi na koi zaroor madad karega.
            Kahani khatam.

            ''')
        
    # Add for automated thank you....
    
        

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya..")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))


