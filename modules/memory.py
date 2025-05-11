import json
import os

MEMORY_FILE = "memory_store.json"

# Load memory from disk
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

# Save memory to disk
def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

# Remember something new
def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

# Recall a memory
def recall(key):
    memory = load_memory()
    return memory.get(key, "I don't remember that.")
