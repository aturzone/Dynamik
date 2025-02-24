import requests
from datetime import datetime

API_KEY = "9a13c0cd-af75-4f0e-8d70-f8ad6c1ee169"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

class ManagerAgent:
    def __init__(self):
        self.role = "Manager"
        self.description = "An AI-powered agent that manages tasks, risks, and costs."
        self.goal = "Generate a comprehensive response based on user input, detected intent, and project data."
        self.backstory = "You are an advanced AI manager designed to handle various aspects of project management."
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def respond(self, optimized_input, detected_intent):
        project_text = self.read_project_text("project_data.txt")
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "You are an AI manager. Please generate a comprehensive response based on the following inputs:"},
                {"role": "user", "content": f"Optimized Input: {optimized_input}\nDetected Intent: {detected_intent}\nProject Data: {project_text}"}
            ],
            "max_tokens": 300
        }

        response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            if "choices" in response_json and response_json["choices"]:
                manager_response = response_json["choices"][0]["message"]["content"].strip()
                return manager_response
            else:
                return "I'm not sure how to generate a response."
        else:
            return f"Sorry, I encountered an issue while processing your request. Error {response.status_code}: {response.text}"

    def read_project_text(self, file_path):
        with open(file_path, "r") as file:
            return file.read()