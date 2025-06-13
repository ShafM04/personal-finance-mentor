# Import the Google Generative AI library
import google.generativeai as genai

# === PASTE YOUR GOOGLE API KEY ON THE NEXT LINE ===
api_key = "AIzaSyD5-JmziwVUivEpCFFEzwCMP7W2kke_mGw"
# ===============================================

# Configure the client with your key
genai.configure(api_key=api_key)

print("Sending a request to the Financial Oracle (via Google)...")

try:
    # This is where you make the actual call to the AI
    # We're using 'gemini-1.5-flash-latest', a fast and capable free model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # The Gemini API has a simpler way to send a prompt
    response = model.generate_content("Explain what a 401(k) is in one simple paragraph.")

    # The response text is stored in 'response.text'
    print("\nOracle's Wisdom:")
    print(response.text)

except Exception as e:
    # If anything goes wrong, this code will run and print the error
    print(f"\nAn error occurred: {e}")