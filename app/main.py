from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from app.database import db  # MongoDB bağlantısı

# .env dosyasını yükle
load_dotenv()

# OpenAI API key'i ortam değişkeninden al
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Furkan's ChatGPT API",
    description="FastAPI + OpenAI + MongoDB demo projesi",
    version="1.0.0"
)

# İstek/yanıt modelleri
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Basit sabit yanıt dönen endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(chat: ChatRequest):
    return {
        "reply": f"Sen: {chat.message} | Ben: Bu çok ilginç bir şey!"
    }

# OpenAI API ile GPT yanıtı dönen endpoint
@app.post("/chatgpt", response_model=ChatResponse)
def chatgpt(chat: ChatRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen yardımcı bir yapay zekasın."},
                {"role": "user", "content": chat.message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message["content"].strip()
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API hatası: {str(e)}")

# Mesajı MongoDB'ye kaydet
@app.post("/chat/save")
async def save_message(chat: ChatRequest):
    result = await db.messages.insert_one(chat.dict())
    return {"inserted_id": str(result.inserted_id)}

# Kayıtlı tüm mesajları listele
@app.get("/chat/list")
async def list_messages():
    messages = await db.messages.find().to_list(length=100)
    return messages
