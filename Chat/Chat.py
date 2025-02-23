import requests
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import re
from crewai import Agent, Task

# Define API_KEY directly in the code
API_KEY = "6515bee9-6910-415c-aedc-108c8cde542e"
EXA_ENDPOINT = "https://api.exa.ai/chat/completions"

#----------AGENTS----------#

class ChatAgent(Agent):
    def __init__(self):
        super().__init__(
            role="Chat Assistant",
            description="An AI-powered chat assistant that provides informative and friendly responses.",
            goal="Engage users in helpful and meaningful conversations.",
            backstory="You are an advanced AI chatbot designed to assist users with their inquiries in a friendly and informative manner."
        )

    def respond(self, user_input, project_text):
        # پاسخگویی به احوال‌پرسی‌ها
        if "hi" in user_input.lower() or "hello" in user_input.lower() or "hey" in user_input.lower():
            return "Hello! How can I assist you today?"

        if "how are you" in user_input.lower():
            return "I'm an AI assistant, so I don't have feelings, but I'm here to help you! How can I assist you today?"

        if "i am sad" in user_input.lower():
            return "I'm sorry to hear that you're feeling sad. If you'd like to talk about it, I'm here to listen."

        if "bye" in user_input.lower() or "goodbye" in user_input.lower():
            return "Goodbye! Have a great day!"

        if "thank you" in user_input.lower():
            return "You're welcome! If you have any other questions, feel free to ask."

        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "exa",
            "messages": [
                {"role": "system", "content": "you are a helpful AI assistant. Please provide the answer to the following question:"},
                {"role": "user", "content": f"You are a friendly and informative AI assistant for answer {user_input}. Use the following project details to answer questions related to the project: {project_text}"}
            ],
            "max_tokens": 150
        }

        response = requests.post(EXA_ENDPOINT, json=data, headers=headers)
        
        if response.status_code == 200:
            response_json = response.json()
            print("API Response:", response_json)

            if "choices" in response_json and response_json["choices"]:
                raw_answer = response_json["choices"][0]["message"]["content"].strip()
                clean_answer = re.sub(r'http[s]?://\S+', '', raw_answer)
                clean_answer = re.sub(r'\s+', ' ', clean_answer).strip()
                return clean_answer

            else:
                return "I'm not sure how to respond to that."
        
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return "Sorry, I encountered an issue while processing your request."

#----------TASKS----------#

class ChatTask(Task):
    def __init__(self, chat_agent):
        super().__init__(
            name="Chat Interaction",
            description="Process and respond to user queries in a conversational manner.",
            agent=chat_agent,
            expected_output="A helpful and informative response to the user query."
        )

    def execute(self, user_input, project_text):
        return self.agent.respond(user_input, project_text)

#----------CREW----------#

class CrewAI:
    def __init__(self, project_text):
        self.chat_agent = ChatAgent()
        self.chat_task = ChatTask(self.chat_agent)
        self.project_text = project_text
        self.current_date = datetime.now().strftime("%Y-%m-%d")

    def run(self):
        print("## Welcome to CrewAI\n____________________________")
        while True:
            user_input = input("You: ").strip()


            if user_input.lower() == "exit":
                print("Goodbye!")
                break

            result = self.chat_task.execute(user_input, self.project_text)
            print(f"CrewAI: {result}")

#----------MAIN----------#

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

    response = crew.chat_task.execute(user_input.text, crew.project_text)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Chat:app", host="0.0.0.0", port=8000, reload=True)
