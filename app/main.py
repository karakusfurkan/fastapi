from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Ortam değişkeninden OpenAI API anahtarını al
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="ChatGPT Mini API",
    description="FastAPI ile Dockerize edilmiş ChatGPT entegrasyonlu demo",
    version="1.0.0"
)

# Gelen veriyi tanımlayan model
class ChatRequest(BaseModel):
    message: str

# Giden cevabı tanımlayan model
class ChatResponse(BaseModel):
    reply: str

# Basit test endpoint'i
@app.post("/chat", response_model=ChatResponse)
def basic_chat(chat: ChatRequest):
    return {
        "reply": f"Sen: {chat.message} | Ben: Bu çok ilginç bir şey!"
    }

# OpenAI GPT-4 entegrasyonlu endpoint
@app.post("/chatgpt", response_model=ChatResponse)
def gpt_chat(chat: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "Sen yardımcı ve nazik bir yapay zekasın."},
                {"role": "user", "content": chat.message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message["content"].strip()
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API hatası: {str(e)}")
