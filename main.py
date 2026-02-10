from groq import Groq
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read the variable
api_key = os.getenv("API_KEY")


def generateRecipe(items):
    prompt = f"""
          You are a Recipe suggester assistant. The user will provide a list of ingredients they have on hand, and you will suggest one or more recipe that can be made using those ingredients.
          {items}
    """

    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages = [
            {'role': 'user',
            'content':prompt}
        ],
        temperature=1
    )    


    print(completion.choices[0].message.content)

def analyze_code_with_llm(file_content):
    prompt = f"""
        Analyze the following code for :
        Code style 
        {file_content}
    """



items = "Chicken, Rice, Broccoli, Garlic, Soy Sauce"
generateRecipe(items)