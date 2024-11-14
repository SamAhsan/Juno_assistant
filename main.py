import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from openai import OpenAI
recognizer = sr.Recognizer
msg = pyttsx3.init()
newsapi = "NewsApi_Key"
def speak(text):
    msg.say(text)
    msg.runAndWait()
def aiProcess(command):
    client = OpenAI(api_key="Openai_Api_Key",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named juno skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content

def commandProcess(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])

            if articles:
                speak("Here are the top news headlines:")

                # Limit to the top 5 headlines
                for article in articles[:5]:
                    title = article.get('title', 'No title available')
                    description = article.get('description', 'No description available')
                    speak(f"Title: {title}")
                    speak(f"Description: {description}")
            else:
                speak("No news articles found at the moment.")
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)
if __name__ == "__main__":
    speak("Juno is getting ready.....")
    while True:
        r = sr.Recognizer()

        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening....")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            print(word)
            if "juno" in word.lower():
                speak("Yes, I'm ready")
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1.0)
                    r.energy_threshold = 300
                    r.dynamic_energy_threshold = True
                    r.pause_threshold = 0.8

                    print("Listening for command...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=7)
                    command = r.recognize_google(audio, language="en-IN")
                    speak(command)
                    print(command)
                    commandProcess(command)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")