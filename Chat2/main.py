from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
from crew_ai import CrewAI

with open("project_data.txt", "r") as file:
    project_data = file.read().strip()

crew = CrewAI(project_data)

class UserInput(BaseModel):
    text: str
    project_name: Optional[str] = None
    
app = FastAPI()

@app.post("/chat")
async def chat(user_input: UserInput, request: Request):
    # Log the incoming request for debugging
    print(f"Incoming request: {request.method} {request.url}")
    print(f"Request headers: {request.headers}")
    print(f"Request body: {await request.body()}")

    optimized_input = crew.optimizer_task.execute(user_input.text)
    detected_intent = crew.intent_detection_task.execute(optimized_input)
    manager_response = crew.manager_task.execute(user_input.text, optimized_input, detected_intent)
    final_response = crew.editor_task.execute(manager_response, "Please edit the response for clarity and completeness.")
    
    return {
        "optimized_input": optimized_input,
        "detected_intent": detected_intent,
        "manager_response": manager_response,
        "final_response": final_response
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)