import sys
from crew import LiveChat
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from setting import HOST, PORT, DEBUG, API_KEY, EXA_ENDPOINT
import logging
import json
import requests

#----------FAST API----------#

app = FastAPI(debug=DEBUG)

# Middleware to log request and response
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the request body
    body = await request.body()
    try:
        data = json.loads(body.decode('utf-8'))
        data_type = type(data)
    except json.JSONDecodeError:
        data_type = type(body.decode('utf-8'))
    logging.info(f"Request body: {body.decode('utf-8')}, Type: {data_type}")

    # Call the next middleware or endpoint
    response = await call_next(request)

    # Log the response body
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    try:
        data = json.loads(response_body.decode('utf-8'))
        data_type = type(data)
    except json.JSONDecodeError:
        data_type = type(response_body.decode('utf-8'))
    logging.info(f"Response body: {response_body.decode('utf-8')}, Type: {data_type}")

    async def new_body_iterator():
        yield response_body

    response.body_iterator = new_body_iterator()
    return response


class UserInput(BaseModel):
    message: str
    
@app.get("/")
async def root():
    return {"message": "Fast API is running"}

@app.post("/process_message/")
async def process_message(user_input: UserInput):
    try:
        # خواندن داده‌های پروژه
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
        # هنگام بروز خطا، درخواست به URL مشخص ارسال می‌شود
        try:
            # ارسال پیام خطا به EXA API با استفاده از فیلد `messages`
            messages = [
                {"role": "system", "content": "An error occurred in the system."},
                {"role": "user", "content": f"Error Message: {str(e)}"}
            ]
            headers = {
                "Content-Type": "application/json",
                "x-api-key": API_KEY  # اضافه کردن هدر x-api-key
            }
            data = {
                "model": "exa",
                "messages": messages,
                "max_tokens": 150
            }

            logging.info(f"Sending error to API: {EXA_ENDPOINT} with data: {json.dumps(data, indent=2)}")  # اضافه کردن لاگ ورودی
            response = requests.post(EXA_ENDPOINT, json=data, headers=headers)

            logging.info(f"API response status code: {response.status_code}")
            logging.info(f"API response text: {response.text}")  # لاگ پاسخ دریافتی

            # بررسی وضعیت پاسخ از API
            if response.status_code == 200:
                if response.text:
                    return response.json().get("results", [])
                else:
                    raise Exception("Empty response from the API.")
            else:
                raise Exception(f"API returned an error: {response.status_code} - {response.text}")

        except Exception as inner_e:
            # اگر درخواست API هم شکست خورد، پیغام خطای اصلی را باز می‌گردانیم
            raise HTTPException(status_code=500, detail=f"Error processing the message: {str(inner_e)}")


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
        
        # تعداد تکرارهایی که از خط فرمان دریافت می‌شود
        n_iterations = int(sys.argv[1])  # اگر نیاز به مقدار ورودی دارید
        LiveChat().crew().train(inputs=inputs, n_iterations=n_iterations)
        
    except Exception as e:
        raise Exception(f"Error in training: {e}")
