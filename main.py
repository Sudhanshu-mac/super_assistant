import time
from modules.voice_input import record_audio
from modules.speech_to_text import transcribe_audio
from modules.tts_output import speak
from modules.command_handler import handle_command

# Initial greeting when the assistant starts
speak("Hello, sir! I am your assistant. How can I help you?")

while True:
    # Use a more subtle print statement for starting the process, avoiding excessive logs
    audio = record_audio()
    text = transcribe_audio(audio)
    print(f"You said: {text}")

    response = handle_command(text)
    if response == "exit":
        speak("Goodbye! Sir, have a great day!")
        break

    speak(response)
