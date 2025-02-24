import requests

API_KEY = "9a13c0cd-af75-4f0e-8d70-f8ad6c1ee169"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

class EditorAgent:
    def __init__(self):
        self.role = "Editor"
        self.description = "An AI-powered agent that edits and improves responses."
        self.goal = "Edit and improve responses based on feedback."
        self.backstory = "You are an advanced AI editor designed to enhance responses for better accuracy and clarity."

    def respond(self, manager_response, feedback):
        # Combine response and feedback for editing
        combined_input = f"Response: {manager_response}\nFeedback: {feedback}"

        # Headers for the API request
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        # Data for the API request
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "You are an AI editor. Please edit the following response based on the feedback:"},
                {"role": "user", "content": combined_input}
            ],
            "max_tokens": 150
        }

        # Make the API request
        response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            if "choices" in response_json and response_json["choices"]:
                edited_response = response_json["choices"][0]["message"]["content"].strip()
                return edited_response
            else:
                return "I'm not sure how to edit the response."
        else:
            return f"Sorry, I encountered an issue while processing your request. Error {response.status_code}: {response.text}"