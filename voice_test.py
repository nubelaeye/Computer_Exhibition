import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        
        # Helps the recognizer adapt to the room's background noise.
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=6
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return None

    try:
        print("🧠 Processing speech...")

        # Online speech recognition
        text = recognizer.recognize_google(audio)
        print(f"👤 You said: {text}")
        return text

    except sr.UnknownValueError:
        print("I couldn't understand that.")
        return None
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return None

if __name__ == "__main__":
    listen()
