import speech_recognition as sr
import getpass
import re

def get_user_input():
    mode = input("Choose input mode - (t)ext or (a)udio [t/a]: ").strip().lower()
    if mode == 'a':
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please speak now...")
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You (audio): {text}")
            return preprocess_input(text)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return get_user_input()
        except sr.RequestError:
            print("Speech recognition service unavailable.")
            return get_user_input()
    else:
        return preprocess_input(input("You: "))

def validate_input(prompt, is_password=False):
    while True:
        if is_password:
            value = getpass.getpass(prompt)
        else:
            value = input(prompt)
        if value.strip():
            return value.strip()
        print("Input cannot be empty.")

def preprocess_input(text):
    # Lowercase, strip, remove extra spaces, basic sanitization
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text
