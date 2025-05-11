import os

def speak(text):
    print("Assistant:", text)
    os.system(f"say '{text}'")
