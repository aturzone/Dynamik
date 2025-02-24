import requests
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import re

# Define API_KEY directly in the code
API_KEY = "9a13c0cd-af75-4f0e-8d70-f8ad6c1ee169"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

#----------AGENTS----------#

class Agent:
    def __init__(self, role, description, goal, backstory):
        self.role = role
        self.description = description
        self.goal = goal
        self.backstory = backstory

class Task:
    def __init__(self, name, description, agent, expected_output):
        self.name = name
        self.description = description
        self.agent = agent
        self.expected_output = expected_output

    def execute(self, *args, **kwargs):
        raise NotImplementedError

class OptimizerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Optimizer",
            description="An AI-powered agent that optimizes user input.",
            goal="Optimize user input for clarity and completeness.",
            backstory="You are an advanced AI optimizer designed to enhance user input for better understanding."
        )

    def respond(self, user_input):
        # Headers for the API request
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        
        # Data for the API request
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "You are an AI optimizer. Please optimize the following input:"},
                {"role": "user", "content": user_input}
            ],
            "max_tokens": 150
        }

        # Make the API request
        response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            print("API Response:", response_json)

            if "choices" in response_json and response_json["choices"]:
                optimized_answer = response_json["choices"][0]["message"]["content"].strip()
                return optimized_answer
            else:
                return "I'm not sure how to optimize that."
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return "Sorry, I encountered an issue while processing your request."

class IntentDetectionAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Intent Detector",
            description="An AI-powered agent that detects user intent.",
            goal="Detect the intent behind user input.",
            backstory="You are an advanced AI designed to detect the intent behind user input for better understanding."
        )

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
            print("API Response:", response_json)

            if "choices" in response_json and response_json["choices"]:
                detected_intent = response_json["choices"][0]["message"]["content"].strip()
                return detected_intent
            else:
                return "I'm not sure how to detect the intent."
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return "Sorry, I encountered an issue while processing your request."

class ManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Manager",
            description="An AI-powered agent that manages tasks, risks, and costs.",
            goal="Generate a comprehensive response based on user input, detected intent, and project data.",
            backstory="You are an advanced AI manager designed to handle various aspects of project management."
        )
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def respond(self, optimized_input, detected_intent, project_text):
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
            print("API Response:", response_json)

            if "choices" in response_json and response_json["choices"]:
                manager_response = response_json["choices"][0]["message"]["content"].strip()
                return manager_response
            else:
                return "I'm not sure how to generate a response."
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return "Sorry, I encountered an issue while processing your request."

class EditorAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Editor",
            description="An AI-powered agent that edits and improves responses.",
            goal="Edit and improve responses based on feedback.",
            backstory="You are an advanced AI editor designed to enhance responses for better accuracy and clarity."
        )

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
            print("API Response:", response_json)

            if "choices" in response_json and response_json["choices"]:
                edited_response = response_json["choices"][0]["message"]["content"].strip()
                return edited_response
            else:
                return "I'm not sure how to edit the response."
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return "Sorry, I encountered an issue while processing your request."

#----------TASKS----------#

class OptimizerTask(Task):
    def __init__(self, optimizer_agent):
        super().__init__(
            name="Optimize Input",
            description="Optimize user input for clarity and completeness.",
            agent=optimizer_agent,
            expected_output="An optimized version of the user input."
        )

    def execute(self, user_input):
        return self.agent.respond(user_input)

class IntentDetectionTask(Task):
    def __init__(self, intent_detection_agent):
        super().__init__(
            name="Detect Intent",
            description="Detect the intent behind the optimized user input.",
            agent=intent_detection_agent,
            expected_output="The detected intent behind the user input."
        )

    def execute(self, optimized_input):
        return self.agent.respond(optimized_input)

class ManagerTask(Task):
    def __init__(self, manager_agent):
        super().__init__(
            name="Manage Project",
            description="Generate a comprehensive response based on user input, detected intent, and project data.",
            agent=manager_agent,
            expected_output="A comprehensive response generated based on the inputs."
        )

    def execute(self, optimized_input, detected_intent, project_text):
        return self.agent.respond(optimized_input, detected_intent, project_text)

class EditorTask(Task):
    def __init__(self, editor_agent):
        super().__init__(
            name="Edit Response",
            description="Edit and improve responses based on feedback.",
            agent=editor_agent,
            expected_output="An edited and improved version of the response."
        )

    def execute(self, manager_response, feedback):
        return self.agent.respond(manager_response, feedback)

#----------CREW----------#

class CrewAI:
    def __init__(self, project_text):
        self.optimizer_agent = OptimizerAgent()
        self.optimizer_task = OptimizerTask(self.optimizer_agent)
        self.intent_detection_agent = IntentDetectionAgent()
        self.intent_detection_task = IntentDetectionTask(self.intent_detection_agent)
        self.manager_agent = ManagerAgent()
        self.manager_task = ManagerTask(self.manager_agent)
        self.editor_agent = EditorAgent()
        self.editor_task = EditorTask(self.editor_agent)
        self.project_text = project_text

    def run(self):
        print("## Welcome to CrewAI\n____________________________")
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            optimized_input = self.optimizer_task.execute(user_input)
            detected_intent = self.intent_detection_task.execute(optimized_input)
            manager_response = self.manager_task.execute(optimized_input, detected_intent, self.project_text)
            final_response = self.editor_task.execute(manager_response, "Please edit the response for clarity and completeness.")
            print(f"Optimized Input: {optimized_input}")
            print(f"Detected Intent: {detected_intent}")
            print(f"Manager Response: {manager_response}")
            print(f"Final Response: {final_response}")

#----------MAIN----------#

class UserInput(BaseModel):
    text: str
    project_text: Optional[str] = None
    project_name: Optional[str] = None
    
app = FastAPI()

# Read project text from a file
def read_project_text(file_path):
    with open(file_path, "r") as file:
        return file.read()

project_text = read_project_text("project_data.txt")

crew = CrewAI(project_text)

@app.post("/chat")
async def chat(user_input: UserInput, request: Request):
    # Log the incoming request for debugging
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Request headers: {request.headers}")
    print(f"Request body: {await request.body()}")

    optimized_input = crew.optimizer_task.execute(user_input.text)
    detected_intent = crew.intent_detection_task.execute(optimized_input)
    manager_response = crew.manager_task.execute(optimized_input, detected_intent, crew.project_text)
    final_response = crew.editor_task.execute(manager_response, "Please edit the response for clarity and completeness.")
    
    return {
        "optimized_input": optimized_input,
        "detected_intent": detected_intent,
        "manager_response": manager_response,
        "final_response": final_response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Chat:app", host="0.0.0.0", port=8000, reload=True)