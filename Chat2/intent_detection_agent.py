import requests

API_KEY = "9a13c0cd-af75-4f0e-8d70-f8ad6c1ee169"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

class IntentDetectionAgent:
    def __init__(self):
        self.role = "Intent Detector"
        self.description = "An AI-powered agent that detects user intent based on optimized input."
        self.goal = "Detect the intent behind user input after it has been optimized."
        self.backstory = "You are an advanced AI designed to detect user intent. Your input is the optimized output from the Optimizer Agent, ensuring clarity and completeness."

    def respond(self, optimized_input):
        # Headers for the API request
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        # Data for the API request
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "You are an AI intent detector. Your input has already been optimized by another AI agent. Detect the intent behind the following optimized input:"},
                {"role": "user", "content": optimized_input}
            ],
            "max_tokens": 150
        }

        # Make the API request
        response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            if "choices" in response_json and response_json["choices"]:
                detected_intent = response_json["choices"][0]["message"]["content"].strip()
                return detected_intent
            else:
                return "I'm not sure how to detect the intent."
        else:
            return f"Sorry, I encountered an issue while processing your request. Error {response.status_code}: {response.text}"