# The Augmented LLM
    # It serves the purpose of a normal LLM and also has the ability to call tools and read/write files. Which can serve as memory.

# Importing the necessary libraries
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time


class AugmentedLLM:
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set")
    genai.configure(api_key=GEMINI_API_KEY)

    def __init__(self, model_name: str = "gemini-1.5-flash"):
        self.chat_history = []
        self.model_name = model_name
        self.model = genai.GenerativeModel(self.model_name)

    def clear_chat_history(self):
        self.chat_history = []

    def add_message(self, role: str, content: str):
        self.chat_history.append({"role": role, "parts": [content]})

    def generate_response(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        self.add_message("user", prompt)
        self.add_message("assistant", response.text)
        return response.text
    
    def read_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()
        
    def write_file(self, file_path: str, content: str):
        with open(file_path, "w") as file:
            file.write(content)

    def call_tool(self, tool_name: str, **kwargs):
        if tool_name == "read_file":
            return self.read_file(kwargs["file_path"])
        elif tool_name == "write_file":
            return self.write_file(kwargs["file_path"], kwargs["content"])
    
    def get_chat_history(self) -> list:
        return self.chat_history
    
    def get_model_name(self) -> str:
        return self.model_name
            

if __name__ == "__main__":
    llm = AugmentedLLM()
    print(llm.generate_response("Hello, how are you?"))
    print(llm.read_file("test.txt"))
    llm.write_file("test.txt", "Hello, world!")
    print(llm.get_chat_history())
    print(llm.get_model_name())
