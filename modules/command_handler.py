import webbrowser
import datetime
import subprocess
import json
import os
import re
from modules.web_scraping import handle_web_query

MEMORY_FILE = "memory.json"
memory_store = {}

# Load memory at startup with safe fallback
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory_store = json.load(f)
    except (json.JSONDecodeError, IOError):
        memory_store = {}
else:
    memory_store = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f, indent=4)

def execute_shell_command(command):
    try:
        if command.strip():
            result = subprocess.run(["sh", "-c", command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.stdout.decode("utf-8").strip()
        else:
            return "No command was provided."
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.decode('utf-8').strip()}"

def handle_command(command):
    # Check for news or weather explicitly
    if "news" in command:
        return handle_web_query("latest news")
    elif "weather" in command:
        return handle_web_query("weather")
    elif "color" in command:
        # Handle memory-based color queries
        for key in memory_store:
            if "color" in key and key in command:
                return f"Your favorite color is {memory_store[key]}"
        return "I'm not sure about your favorite color, but I can learn more about your preferences!"
    elif "time" in command:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    elif "date" in command:
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."
    elif "open browser" in command or "open google" in command:
        try:
            webbrowser.open("https://www.google.com")
            return "Opening your browser."
        except Exception as e:
            return f"Error opening browser: {str(e)}"
    elif command.startswith("remember"):
        content = command.replace("remember", "").strip()
        if content:
            # Try extracting key-value pairs like "my favorite color is blue"
            match = re.search(r"my (.+?) is (.+)", content)
            if match:
                key = match.group(1).strip().lower()
                value = match.group(2).strip()
                memory_store[key] = value
                save_memory()
                return f"Got it! I'll remember your {key} is {value}."
            else:
                memory_store["memory"] = content
                save_memory()
                return f"I'll remember that: {content}"
        else:
            return "What should I remember?"
    elif "what did i ask you to remember" in command:
        return memory_store.get("memory", "You haven't asked me to remember anything yet.")
    elif "exit" in command or "quit" in command or "sleep" in command or "thank you" in command:
        return "exit"
    else:
        # Check for memory keys dynamically
        for key in memory_store:
            if key in command:
                return f"Your {key} is {memory_store[key]}"

        return "Sorry, I did not understand that."
