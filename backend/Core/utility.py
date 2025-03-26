
import os
import dotenv
import getpass

def getApiKey():
    dotenv.load_dotenv( './.env')
    if "GROQ_API_KEY" not in os.environ:
        os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")
    if "GOOGLE_API_KEY" not in os.environ:
        os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Gemini API key: ")
    if "MISTRAL_API_KEY" not in os.environ:
        os.environ["MISTRAL_API_KEY"] = getpass.getpass("Enter your Mistral API key: ")