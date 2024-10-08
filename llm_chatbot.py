from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv()


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)
