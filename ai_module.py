import re
from executor import open_app, type_text, search_file
from file_manager import save_log
from config import IS_TERMUX, SYSTEM

USE_ML = False

# Enable ML only on desktops (Windows/Linux) with enough resources
if not IS_TERMUX:
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        MODEL_NAME = "EleutherAI/gpt-neo-125M"
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        model.to(DEVICE)
        USE_ML = True
    except Exception as e:
        print(f"[ML fallback] Could not load model: {e}")

def offline_ml_response(prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    outputs = model.generate(**inputs, max_length=max_length)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return text

def interpret_command(command):
    command = command.lower()

    # ML response first
    if USE_ML:
        try:
            response = offline_ml_response(command)
            save_log(f"ML interpreted: {response}")
            return response
        except Exception as e:
            print(f"[ML error] {e}")

    # Rule-based fallback
    open_match = re.search(r"open (\w+)", command)
    if open_match:
        app_name = open_match.group(1)
        open_app(app_name)
        save_log(f"Opened {app_name}")
        return f"Opening {app_name}"

    type_match = re.search(r"type (.+)", command)
    if type_match:
        text = type_match.group(1)
        type_text(text)
        save_log(f"Typed: {text}")
        return f"Typed: {text}"

    search_match = re.search(r"search file (.+)", command)
    if search_match:
        filename = search_match.group(1)
        path = search_file(filename)
        save_log(f"Searched for {filename}: {path}")
        return f"Found at: {path}" if path else "File not found"

    return "Command not recognized"
