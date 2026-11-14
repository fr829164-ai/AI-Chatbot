import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

load_dotenv()

app = FastAPI(title="AI Smart Search Chatbot")

# Frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """
You are a helpful and friendly AI Assistant.
Answer users clearly using simple language.
Maintain context from previous conversation.
"""

class ChatRequest(BaseModel):
    messages: list[dict]

@app.get("/")
def home():
    return {"message": "AI Smart Search Chatbot API is running"}

@app.post("/api/chat")
def chat(request: ChatRequest):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API key is missing."
        )

    try:
        client = Groq(api_key=api_key)

        api_messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        for message in request.messages[-10:]:
            role = message.get("role")
            content = message.get("content", "")

            if role in ["user", "assistant"] and content.strip():
                api_messages.append({
                    "role": role,
                    "content": content
                })

        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=api_messages
        )

        response = completion.choices[0].message.content

        return {"reply": response}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="AI response error: " + str(e)
        )
