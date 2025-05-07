import os
import subprocess
import platform
import requests
from bs4 import BeautifulSoup
import urllib.parse
import ollama
from langchain_community.llms import Ollama

class ShellCommandTool:
    def __init__(self):
        self.name = "shell_command"
        self.description = "Execute a shell command and return the output."
    
    def run(self, command):
        try:
            command = command.strip()
            if command.startswith('`') and command.endswith('`'):
                command = command[1:-1]
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Failed to execute command: {str(e)}"

class OpenWebsite:
    def __init__(self):
        self.name = "open_website"
        self.description = "Opens the relevant website based on the query"
    
    def run(self, website):
        try:
            command = f'''open -a "Brave Browser 2.app" "{website}"'''
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Failed to execute command: {str(e)}"

class LLMTool:
    def __init__(self):
        self.name = "open_website"
        self.description = "Use this tool to get any details pass the query and get the result if you can't use any other tool"
    
    def run(self,query):
        try:
            response = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            return response['message']['content']
        except Exception as ex:
            print(ex)

class ExceptTool:
    def __init__(self):
        self.name = "anything"
        self.description = "Use this tool to get any details pass the query and get the result if you can't use any other tool"
    
    def run(self):
        try:
            return "Terminate this query"
        except Exception as ex:
            print(ex)