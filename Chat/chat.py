import requests
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from crewai import Agent, Task

# Define API_KEY directly in the code
API_KEY = "6e58c733-2848-4401-90e7-645e46e26699"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

#----------AGENTS----------#

class IntentDetectionAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Intent Detection Agent",
            description="An AI agent that detects the user's intent based on their input.",
            goal="Detect user's intent and decide the next actions.",
            backstory="You are an advanced AI designed to detect user intent from their input."
        )

    def detect_intent(self, user_input, project_text):
        try:
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "exa",
                "messages": [
                    {"role": "system", "content": "You are an AI intent detection agent. Detect the user's intent based on their input."},
                    {"role": "user", "content": f"Detect the intent of the following user input: {user_input}. Use the following project details for context: {project_text}"}
                ],
                "max_tokens": 50
            }

            response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
            
            if response.status_code == 200:
                response_json = response.json()
                print("API Response:", response_json)

                if "choices" in response_json and response_json["choices"]:
                    intent = response_json["choices"][0]["message"]["content"].strip()
                    return intent

                else:
                    return "unknown"
            
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return "unknown"
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return "unknown"

class AnalyzerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Analyzer Agent",
            description="An AI agent that analyzes user input and extracts relevant information from the project text.",
            goal="Analyze user input and extract accurate information from the project text. Format the response as a professional Markdown document.",
            backstory="You are an advanced AI designed to analyze user queries and provide relevant information based on the project text."
        )

    def respond(self, user_input, project_text):
        try:
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "exa",
                "messages": [
                    {"role": "system", "content": "You are an AI analyzer agent. Analyze the user input and extract relevant information from the project text. Format the response as a professional Markdown document with appropriate headings, bold text, and links."},
                    {"role": "user", "content": f"Analyze the following user input: {user_input}. Use the following project details to extract relevant information and format the response as a Markdown document: {project_text}"}
                ],
                "max_tokens": 150
            }

            response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
            
            if response.status_code == 200:
                response_json = response.json()
                print("API Response:", response_json)

                if "choices" in response_json and response_json["choices"]:
                    raw_answer = response_json["choices"][0]["message"]["content"].strip()
                    return raw_answer

                else:
                    return "I'm not sure how to respond to that."
            
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return "Sorry, I encountered an issue while processing your request."
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return "Sorry, I encountered a network issue while processing your request."

class ManagerAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Manager Agent",
            description="An AI agent that verifies and refines responses provided by the analyzer agent.",
            goal="Verify and refine responses to ensure accuracy and clarity.",
            backstory="You are an advanced AI designed to verify and refine responses for accuracy and clarity."
        )

    def verify_and_refine(self, user_input, analyzer_response, project_text):
        return analyzer_response  # In a real-world scenario, additional verification logic would be implemented here.

#----------TASKS----------#

class IntentDetectionTask(Task):
    def __init__(self, intent_detection_agent):
        super().__init__(
            name="Intent Detection Task",
            description="Detect the intent of the user input.",
            agent=intent_detection_agent,
            expected_output="Detected intent of the user input."
        )

    def execute(self, user_input, project_text):
        return self.agent.detect_intent(user_input, project_text)

class AnalyzerTask(Task):
    def __init__(self, analyzer_agent):
        super().__init__(
            name="Analyzer Task",
            description="Analyze user input and extract relevant information from the project text.",
            agent=analyzer_agent,
            expected_output="Extracted information from the project text."
        )

    def execute(self, user_input, project_text):
        return self.agent.respond(user_input, project_text)

class ManagerTask(Task):
    def __init__(self, manager_agent):
        super().__init__(
            name="Manager Task",
            description="Verify and refine the response provided by the analyzer agent.",
            agent=manager_agent,
            expected_output="Verified and refined response."
        )

    def execute(self, user_input, analyzer_response, project_text):
        return self.agent.verify_and_refine(user_input, analyzer_response, project_text)

#----------CREW----------#

class CrewAI:
    def __init__(self, project_text):
        self.intent_detection_agent = IntentDetectionAgent()
        self.analyzer_agent = AnalyzerAgent()
        self.manager_agent = ManagerAgent()
        self.intent_detection_task = IntentDetectionTask(self.intent_detection_agent)
        self.analyzer_task = AnalyzerTask(self.analyzer_agent)
        self.manager_task = ManagerTask(self.manager_agent)
        self.project_text = project_text
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def run(self):
        print("## Welcome to CrewAI\n____________________________")
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            intent = self.intent_detection_task.execute(user_input, self.project_text)
            if "project" in intent:
                analyzer_response = self.analyzer_task.execute(user_input, self.project_text)
                final_response = self.manager_task.execute(user_input, analyzer_response, self.project_text)
                print(f"CrewAI: {final_response}")
            else:
                print("CrewAI: not in my data.")

#----------FASTAPI----------#
class UserInput(BaseModel):
    text: str
    project_text: Optional[str] = None
    
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

    intent = crew.intent_detection_task.execute(user_input.text, crew.project_text)
    if "project" in intent:
        analyzer_response = crew.analyzer_task.execute(user_input.text, crew.project_text)
        final_response = crew.manager_task.execute(user_input.text, analyzer_response, crew.project_text)
        return {"response": final_response}
    else:
        return {"response": "not in my data."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("chat:app", host="0.0.0.0", port=8000, reload=True)