import sys
import threading
import tkinter as tk
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import speech_recognition
import pyttsx3 as tts

from neuralintents import GenericAssistant

class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate",150)

        self.assistant = GenericAssistant.load_model(model_name="jarvis-V0")

        self.root = tk.Tk()
        self.label = tk.Label(text="AI")
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()


    def create_file(self):
        with open("somefile.txt", "w") as f:
            f.write("Hello World")
    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    if "hey jarvis" in text:
                        self.label.config(fg="red")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                                self.label.config(fg="black")
            except:
                self.label.config(fg="black")
                continue

Assistant()