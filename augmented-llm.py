# The Augmented LLM
    # It serves the purpose of a normal LLM and also has the ability to call tools and read/write files. Which can serve as memory.

# Importing the necessary libraries
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from mock_tools import calculator_tool
import json
import re


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
        # print(response.text)
        # print(type(response.text))
        if '<tool_call>' and '</tool_call>' in response.text:
            tool_results = self.response_parser(response.text)
            return tool_results
        else:
            return response.text

    def response_parser(self, text: str):
        matches = re.findall(r"<tool_call>\s*({.*?})\s*</tool_call>", text, re.DOTALL)
        tool_results = []
        for match in matches:
            json_obj = json.loads(match)
            temp = self.call_tool(json_obj)
            tool_results.append(temp)
        
        return tool_results
    
    def read_file(self, file_path: str) -> str:
        with open(file_path, "r") as file:
            return file.read()
        
    def write_file(self, file_path: str, content: str):
        with open(file_path, "w") as file:
            file.write(content)

    def call_tool(self, api_call: dict):
        # if tool_name == "read_file":
        #     return self.read_file(kwargs["file_path"])
        # elif tool_name == "write_file":
        #     return self.write_file(kwargs["file_path"], kwargs["content"])
        result = None
        if api_call["tool_name"] == "calculator_tool":
            try:
                tool = calculator_tool.CalculatorTool()

                if api_call["operation"] == "add":
                    result = tool.add(*api_call["parameters"])
                elif api_call["operation"] == "multiply":
                    result = tool.multiply(*api_call["parameters"])
            except Exception as e:
                print("There was an arror dawg.")
        return result
    
    def get_chat_history(self) -> list:
        return self.chat_history
    
    def get_model_name(self) -> str:
        return self.model_name
            

if __name__ == "__main__":
    llm = AugmentedLLM()
    init_prompt = """
    You are an assistant which talks as little as possible. Whenever I ask you to calculate a sum or a product, you should call a tool.
    DO NOT CALCULATE THE SUM OR PRODUCT BY YOURSELF !

    Here are some examples of how you can call a tool to calculate a sum or a product.
     - For calculating the sum of the following numbers: 1, 3, 5, 7, 9

     <tool_call>
     {
     "tool_name": "calculator_tool",
     "operation": "add",
     "parameters": [1, 3, 5, 7, 9]
     }
     </tool_call>

     - For calculating the product of the following numbers: 2, 4, 6, 8, 10
     <tool_call>
     {
     "tool_name": "calculator_tool",
     "operation": "multiply",
     "parameters": [2, 4, 6, 8, 10]
     }
     </tool_call>

     If you understand the instructions only reply with a "YEAH".
    """
    print(llm.generate_response(init_prompt))
    # llm.add_message('user', init_prompt)
    # llm.add_message('model', "YEAH")

    prompt = "Now, I want you to calculate the sum of the following numbers : 1, 2, 3, 4, 5."
    llm.add_message('user', prompt)

    print(llm.generate_response(llm.chat_history))
    
