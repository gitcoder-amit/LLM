from groq import Groq
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read the variable
api_key = os.getenv("API_KEY")



system_prompt = """
        You're evaluating writing style in text,
        Your evaluation must always be in json format, here is the format you must follow:

        ```
            "issues": [
                {
                    "type": "style",
                    "line": 14,
                    "description": "Line too long",
                    "suggestion": "Break into multiple lines"
                },
                {
                    "type": "bug",
                    "line": 21,
                    "description": "Potential null pointer dereference",
                    "suggestion": "Add a null check"
                },
            ]
        ```
"""


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
        - Code style and formating issues
        - Potential bugs or logical errors
        - Performance improvement
        - Best Practices

        Content: {file_content}

        {{
            "issues": [
                {{
                    "type": "<style|bug|performance|best_practice>",
                    "line": <line_number>,
                    "description": "<description>",
                    "suggestion": "<suggestion>"
                }}
            ],

        }}
        ``json
    """

    client = Groq(
        api_key = os.getenv("GROQ_API_KEY"),
    )

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages = [
            {'role': 'system', 'content':system_prompt},
            {'role': 'user',
            'content':prompt}
        ],
        temperature=1,
        stream=True # enable streaming means we will get results related to response as soon as they are generated
    )    


    print(completion.choices[0].message.content)


import requests
import base64

class GithubCodeAccess:
    def __init__(self, repo_name, username, pr_number, token=None):
        self.repo_name = repo_name
        self.username = username
        self.pr_number = pr_number
        self.token = token

    def analyse_pr(self):
        pr_files = self.fetch_pr_files()
        for file in pr_files:
            file_path = file['filename']
            file_content_response = self.fetch_file_content(file_path)
            base64_content = file_content_response['content']
            decoded_content = self.convert_base64_to_string(base64_content)
            analyze_code_with_llm(decoded_content)

    def fetch_pr_files(self):
        url = f"https://api.github.com/repos/{self.username}/{self.repo_name}/pulls/{self.pr_number}/files"
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    

    def fetch_file_content(self, file_path):
        url = f"https://api.github.com/repos/{self.username}/{self.repo_name}/contents/{file_path}"
        headers = {"Authorization": f"token {self.token}"} if self.token else {}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def convert_base64_to_string(self, base64_content):
        return base64.b64decode(base64_content).decode('utf-8')



import base64
code_str = """IyEvdXNyL2Jpbi9lbnYgcHl0aG9uCiIiIkRqYW5nbydzIGNvbW1hbmQtbGlu\nZSB1dGlsaXR5IGZvciBhZG1pbmlzdHJhdGl2ZSB0YXNrcy4iIiIKaW1wb3J0\nIG9zCmltcG9ydCBzeXMKCgpkZWYgbWFpbigpOgogICAgIiIiUnVuIGFkbWlu\naXN0cmF0aXZlIHRhc2tzLiIiIgogICAgb3MuZW52aXJvbi5zZXRkZWZhdWx0\nKCdESkFOR09fU0VUVElOR1NfTU9EVUxFJywgJ2RqbWlkZGxld2FyZS5zZXR0\naW5ncycpCiAgICB0cnk6CiAgICAgICAgZnJvbSBkamFuZ28uY29yZS5tYW5h\nZ2VtZW50IGltcG9ydCBleGVjdXRlX2Zyb21fY29tbWFuZF9saW5lCiAgICBl\neGNlcHQgSW1wb3J0RXJyb3IgYXMgZXhjOgogICAgICAgIHJhaXNlIEltcG9y\ndEVycm9yKAogICAgICAgICAgICAiQ291bGRuJ3QgaW1wb3J0IERqYW5nby4g\nQXJlIHlvdSBzdXJlIGl0J3MgaW5zdGFsbGVkIGFuZCAiCiAgICAgICAgICAg\nICJhdmFpbGFibGUgb24geW91ciBQWVRIT05QQVRIIGVudmlyb25tZW50IHZh\ncmlhYmxlPyBEaWQgeW91ICIKICAgICAgICAgICAgImZvcmdldCB0byBhY3Rp\ndmF0ZSBhIHZpcnR1YWwgZW52aXJvbm1lbnQ/IgogICAgICAgICkgZnJvbSBl\neGMKICAgIGV4ZWN1dGVfZnJvbV9jb21tYW5kX2xpbmUoc3lzLmFyZ3YpCgoK\naWYgX19uYW1lX18gPT0gJ19fbWFpbl9fJzoKICAgIG1haW4oKQo=\n"""
# print(base64.b64decode(code_str).decode()) 
analyze_code_with_llm(base64.b64decode(code_str).decode())


# items = "Chicken, Rice, Broccoli, Garlic, Soy Sauce"
# generateRecipe(items)



github = GithubCodeAccess(
    repo_name="LLM",
    username="gitcoder-amit",
    pr_number=1,
    token=None
)

github.analyse_pr()