"""
EON Lite - a simple voice assistant for Windows.
Features: speech input, offline text-to-speech, predefined commands,
web shortcuts, Hindi jokes, and Rock-Paper-Scissors.
Note: SpeechRecognition's Google recognizer needs internet for speech-to-text.
No OpenAI, Hugging Face, or paid AI API is used.
"""

import random
import subprocess
import os
import sys
import webbrowser
from pathlib import Path
from urllib.parse import quote

import pyttsx3
import speech_recognition as sr


ASSISTANT_NAME = "EON"

JOKES_HI = [
    "टीचर: बताओ, बिजली कहाँ से आती है? छात्र: मामा के घर से! टीचर: कैसे? छात्र: जब भी बिजली जाती है, पापा कहते हैं—सालों ने फिर काट दी!",
    "दोस्त: पढ़ाई कैसी चल रही है? दूसरा: बस चल रही है। दोस्त: कहाँ तक? दूसरा: मोबाइल तक!",
    "टीचर: सबसे ज़्यादा नशा किस चीज़ में होता है? छात्र: किताबों में। टीचर: वो कैसे? छात्र: खोलते ही नींद आ जाती है!",
]

ROCK_PAPER_SCISSORS = {
    "rock": ["rock", "पत्थर", "stone"],
    "paper": ["paper", "कागज़", "कagaz", "कागज"],
    "scissors": ["scissors", "scissor", "कैंची"],
}

recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.7
speaker = pyttsx3.init()
speaker.setProperty("rate", 175)


def speak(message: str) -> None:
    """Print and speak a response."""
    print(f"\n{ASSISTANT_NAME}: {message}")
    try:
        speaker.say(message)
        speaker.runAndWait()
    except Exception as exc:
        print(f"[TTS warning] Could not speak this response: {exc}")


def listen(timeout: int = 5, phrase_time_limit: int = 7) -> str:
    """Listen for one command. Google speech recognition requires internet."""
    try:
        with sr.Microphone() as source:
            print("\nListening... बोलिए!")
            recognizer.adjust_for_ambient_noise(source, duration=0.35)
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_time_limit
            )
        try:
            command = recognizer.recognize_google(audio, language="en-IN")
        except sr.UnknownValueError:
            try:
                command = recognizer.recognize_google(audio, language="hi-IN")
            except sr.UnknownValueError:
                speak("माफ़ कीजिए, मैं समझ नहीं पाया। फिर से बोलिए।")
                return ""
        print(f"You: {command}")
        return command.lower().strip()
    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""
    except (OSError, AttributeError) as exc:
        speak("माइक्रोफ़ोन नहीं मिल रहा। कृपया माइक्रोफ़ोन कनेक्शन और permissions जाँचें।")
        print(f"[Microphone error] {exc}")
        return ""
    except sr.RequestError:
        speak("Speech recognition service तक पहुँचा नहीं जा सका। इंटरनेट जाँचिए।")
        return ""


def open_camera() -> None:
    if sys.platform == "win32":
        os.startfile("microsoft.windows.camera:")
    else:
        speak("Camera shortcut is configured for Windows. Please open your camera app manually.")


def open_settings() -> None:
    if sys.platform == "win32":
        os.system("start ms-settings:")
    else:
        speak("Settings shortcut is configured for Windows.")


def play_music() -> None:
    """Open the user's Music folder; Windows can play a selected file from there."""
    music_dir = Path.home() / "Music"
    if sys.platform == "win32":
        os.startfile(str(music_dir if music_dir.exists() else Path.home()))
    else:
        webbrowser.open("https://music.youtube.com")
    speak("आपका Music folder खोल रहा हूँ। वहाँ से कोई गाना चलाइए।")


def play_rps() -> None:
    speak("Rock, paper, या scissors बोलिए।")
    user = listen(timeout=6, phrase_time_limit=4)
    choices = {
        "rock": ("rock", "पत्थर", "stone"),
        "paper": ("paper", "कागज", "कागज़"),
        "scissors": ("scissors", "scissor", "कैंची"),
    }
    selected = None
    for choice, aliases in choices.items():
        if any(alias in user for alias in aliases):
            selected = choice
            break

    if selected is None:
        speak("मैं आपकी चाल नहीं समझ पाया। जब चाहें फिर से game शुरू कर सकते हैं।")
        return

    computer = random.choice(list(choices.keys()))
    hindi = {"rock": "रॉक", "paper": "पेपर", "scissors": "कैंची"}
    if selected == computer:
        result = "Tie! इस बार बराबरी हुई।"
    elif (selected, computer) in {
        ("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")
    }:
        result = "आप जीत गए! बढ़िया!"
    else:
        result = "मैं जीत गया! अगली बार फिर कोशिश कीजिए।"

    speak(f"आपने {hindi[selected]} चुना और मैंने {hindi[computer]}। {result}")


def handle_command(command: str) -> bool:
    """Run a predefined command. Returns False when the user wants to quit."""
    if not command:
        return True

    if any(x in command for x in ("exit", "quit", "stop assistant", "बंद हो जाओ", "बाय")):
        speak("अलविदा! आपका दिन अच्छा रहे।")
        return False

    if any(x in command for x in ("hello", "hi eon", "hey eon", "नमस्ते", "हेलो")):
        speak("नमस्ते! मैं EON हूँ। बताइए, मैं आपकी क्या मदद कर सकता हूँ?")
    elif any(x in command for x in ("introduce", "who are you", "your name", "अपने बारे", "परिचय")):
        speak("नमस्ते! मेरा नाम EON है। मैं Python से बना एक छोटा voice assistant हूँ। मैं आपके commands सुन सकता हूँ, जवाब बोल सकता हूँ, websites और कुछ Windows apps खोल सकता हूँ, jokes सुना सकता हूँ और आपके साथ Rock Paper Scissors खेल सकता हूँ।")
    elif any(x in command for x in ("joke", "funny", "जोक", "चुटकुला")):
        speak(random.choice(JOKES_HI))
    elif any(x in command for x in ("camera", "कैमरा")):
        speak("कैमरा खोल रहा हूँ।")
        try:
            open_camera()
        except Exception as exc:
            speak("Camera app नहीं खुल पाया।")
            print(f"[Camera error] {exc}")
    elif "youtube" in command or "यूट्यूब" in command:
        speak("YouTube खोल रहा हूँ।")
        webbrowser.open("https://www.youtube.com")
    elif "google" in command or "गूगल" in command or "search" in command:
        query = command.replace("search", "").replace("google", "").replace("गूगल", "").strip()
        if not query or query in ("open", "खोलो"):
            query = ""
        speak("Google खोल रहा हूँ।")
        webbrowser.open("https://www.google.com" + ("/search?q=" + quote(query) if query else ""))
    elif any(x in command for x in ("setting", "सेटिंग")):
        speak("Windows Settings खोल रहा हूँ।")
        try:
            open_settings()
        except Exception as exc:
            speak("Settings नहीं खुल पाई।")
            print(f"[Settings error] {exc}")
    elif any(x in command for x in ("music", "song", "गाना", "म्यूजिक")):
        play_music()
    elif any(x in command for x in ("weather", "forecast", "मौसम", "मौसम का हाल")):
        speak("ताज़ा मौसम देखने के लिए browser में forecast खोल रहा हूँ।")
        webbrowser.open("https://www.google.com/search?q=weather+forecast+near+me")
    elif any(x in command for x in ("rock paper scissors", "play game", "game", "गेम", "रॉक पेपर")):
        play_rps()
    elif any(x in command for x in ("help", "commands", "क्या कर सकते", "मदद")):
        speak("आप कह सकते हैं: tell me a joke, open camera, open YouTube, open Google, open settings, play music, weather forecast, introduce yourself, play rock paper scissors, या exit.")
    else:
        speak("यह command अभी मेरी list में नहीं है। Help बोलिए और मैं commands बता दूँगा।")

    return True


def main() -> None:
    print("=" * 48)
    print(" EON LITE | Simple Python Voice Assistant ")
    print("=" * 48)
    print("Say 'help' for commands, or 'exit' to quit.")
    speak("नमस्ते! मैं EON हूँ। शुरू करने के लिए कोई command बोलिए।")
    while True:
        command = listen()
        if not handle_command(command):
            break


if __name__ == "__main__":
    main()
