import requests
import re

API_KEY = "9a13c0cd-af75-4f0e-8d70-f8ad6c1ee169"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

with open("project_data.txt", "r") as file:
    project_data = file.read().strip()
class OptimizerAgent:
    def __init__(self, project_data):
        self.role = "Optimizer"
        self.description = "An AI-powered agent that optimizes user input based on project data."
        self.goal = "Optimize user input for clarity and completeness , considering project context."
        self.backstory = "You are an advanced AI optimizer designed to enhance user input for better understanding."
        self.project_data = project_data
        

    def respond(self, user_input):
        project_name = self.extract_project_name(user_input)
        if not project_name:
            project_name = input("Please provide the project name: ").strip()
            user_input += f" Project Name: {project_name}"

        return self.optimize_input(user_input)

    def extract_project_name(self, user_input):
        # Check if "Project Name" is present in the input
        match = re.search(r"Project Name:\s*(\w+)", user_input, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    def optimize_input(self, user_input):
        # Headers for the API request
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        contextual_input = f"Project Data: {self.project_data}\nUser Input: {user_input}"
        
        # Data for the API request
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "You are an AI optimizer. Please optimize the following input considering the project context:"},
                {"role": "user", "content": contextual_input}
            ],
            "max_tokens": 150
        }

        # Make the API request
        response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            if "choices" in response_json and response_json["choices"]:
                optimized_answer = response_json["choices"][0]["message"]["content"].strip()
                return optimized_answer
            else:
                return "I'm not sure how to optimize that."
        else:
            return f"Sorry, I encountered an issue while processing your request. Error {response.status_code}: {response.text}"