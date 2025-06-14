# oracle.py

import google.generativeai as genai
import gradio as gr
import json
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv() # This line loads the variables from your .env file
API_KEY = os.getenv("GEMINI_API_KEY")
HISTORY_FILE = "chat_history.json"

# Check if the API key is loaded
if not API_KEY:
    raise ValueError("API key not found. Please create a .env file and add GEMINI_API_KEY=YourApiKey")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- AI Persona Definition ---
system_prompt = """
You are the Financial Oracle, a wise and encouraging personal finance mentor. 
Your goal is to provide clear, easy-to-understand financial education.
You must not provide personalized financial, investment, or legal advice. 
Instead, you should explain financial concepts, define terms, and offer general guidance and educational information.
Keep your tone supportive and accessible to a beginner.
"""

# --- Functions for Saving and Loading Chat History ---

def load_history():
    """Loads chat history from a JSON file if it exists."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or empty, start fresh
            pass 
    # Return the initial system prompt setup if no history exists
    return [
        {'role': 'user', 'parts': [system_prompt]},
        {'role': 'model', 'parts': ["Understood. I am the Financial Oracle, ready to assist with general financial education."]}
    ]

def save_history(history):
    """Saves the current chat history to a JSON file."""
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

# --- Main Chat Logic ---

# Load the history once when the script starts
chat = model.start_chat(history=load_history())

def financial_oracle_chat(message, history_for_gradio):
    """The core function that handles the chat logic."""
    try:
        response = chat.send_message(message)
        # Save the updated history after a successful response
        save_history(chat.history) 
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# --- Gradio User Interface ---

ui = gr.ChatInterface(
    fn=financial_oracle_chat,
    chatbot=gr.Chatbot(height=600),
    title="Financial Oracle 🪙",
    description="Ask me about general finance concepts! Your conversation will be saved and loaded automatically.",
    theme="soft",
    examples=["What is a 401(k)?", "Explain the difference between a stock and a bond.", "What does 'diversification' mean?"],
    cache_examples=False # Set to False to ensure fresh runs
)

# --- Run the application ---
if __name__ == "__main__":
    ui.launch()
