import requests

API_KEY = "9a13c0cd-af75-4f0e-8d70-f8ad6c1ee169"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

class IntentDetectionAgent:
    def __init__(self):
        self.role = "Intent Detector"
        self.description = "An AI-powered agent that detects user intent."
        self.goal = "Detect the intent behind user input."
        self.backstory = "You are an advanced AI designed to detect the intent behind user input for better understanding."

    def respond(self, optimized_input):
        # Headers for the API request
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        # Data for the API request
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "You are an AI intent detector. Please detect the intent behind the following input:"},
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