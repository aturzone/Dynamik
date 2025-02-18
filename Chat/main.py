import sys
from crew import LiveChat
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from setting import HOST, PORT, DEBUG

#----------FAST API----------#

app = FastAPI(debug=DEBUG)

class UserInput(BaseModel):
    message: str
    
@app.get("/")
async def root():
    return {"message": "Fast API is running"}

@app.post("/process_message/")
async def process_message(user_input: UserInput):
    try:
        # خواندن داده‌های پروژهuser_input
        with open("/home/aturzone/Dynamik/Chat/Data/ProjectData.txt", "r") as file:
            file_content = file.read()

        # تنظیمات ورودی برای شروع فرآیند
        inputs = {
            'customer_domain': 'crewai.com',
            'project_data': file_content,
            'user_message': user_input.message  # ارسال پیام کاربر
        }
        
        # راه اندازی LiveChat
        live_chat = LiveChat().crew()
        
        # شروع فرآیند با ارسال ورودی به IntentDetectionAgent
        result = live_chat.kickoff(inputs=inputs)
        
        # نتایج را به کاربر بازگشت می‌دهیم
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
#----------MAIN----------#

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)


def run():
    with open("/home/aturzone/Dynamik/Chat/Data/ProjectData.txt", "r") as file:
        file_content = file.read()
        
    inputs = {
        'customer_domain': 'crewai.com',
        'project_data': file_content  
        
    }
    LiveChat().crew().kickoff(inputs=inputs)
    
    
def train():
    """
    Train the crew for a given number of iterations
    """
    
    try:
        
        with open("/home/aturzone/Dynamik/Chat/Data/ProjectData.txt", "r") as file:
            file_content = file.read()
            
        inputs = {
            'customer_domain': 'crewai.com',
            'project_data': file_content  
        }
        
        n_iterations = int(sys.argv)
        LiveChat().crew().train(inputs=inputs, n_iterations=n_iterations)
        
    except Exception as e:
        raise Exception(f"Error in training: {e}")
    
