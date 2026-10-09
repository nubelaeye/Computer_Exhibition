import os
import webbrowser
import speech_recognition as sr
from openai import OpenAI

# ✅ Set your OpenAI API Key here (replace with your real key)
os.environ["OPENAI_API_KEY"] = "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"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize text-to-speech engine
import pyttsx3

# Initialize TTS engine
speaker = pyttsx3.init()

# Get all available voices
voices = speaker.getProperty('voices')

# Try to select a female voice first, fallback to first voice
  # fallback

# Optional: set speech rate
speaker.setProperty('rate', 200)

# Speak text
speaker.runAndWait()

speaker .setProperty('voice', voices[0].id)

def speak(text):
    """Speak and print text."""
    print("AI:Speak and print text ", text)
    speaker.say(text)

def takeCommand():
    """Listen to the user's voice and convert it to text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎧 Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        print("⏳ Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"🧠 You said: {query}\n")
        return query
    except Exception:
        ("Sorry, I didn't catch that.")
        return ""

while True:
    query = takeCommand().lower()

    # ---------- Fixed Commands ----------
    if "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open facebook" in query:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")

    elif "open news" in query:
        speak("Opening News")
        webbrowser.open("https://www.aajtak.in/livetv")

    elif "open calculator" in query:
        speak("Opening Calculator")
        os.system("start calc")

    elif "open camera" in query:
        speak("Opening Camera")
        os.system("start microsoft.windows.camera:")

    elif "open settings" in query:
        speak("Opening Settings")
        os.system("start ms-settings:")

    elif "stop" in query or "exit" in query or "goodbye" in query:
        speak("Goodbye, sudhanshu!")
        break

    # ---------- Smart AI Conversation ----------
    elif query.strip() != "":
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # or "gpt-3.5-turbo" if you prefer
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are Nova, an advanced AI voice assistant created by Pranjal. "
                            "You are friendly, smart, and sound natural in your responses."
                        )
                    },
                    {"role": "user", "content": query}
                ]
            )

            ai_reply = response.choices[0].message.content
            speak(ai_reply)

        except Exception as e:
            print("❌ Error:", e)
            speak("Something went wrong while connecting to OpenAI.")
