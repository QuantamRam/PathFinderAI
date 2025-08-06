"""
PathFinder-AI / backend/main.py
Minimal FastAPI server for chatbot inference
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from bot_final_code import chatbot_response

app = FastAPI()

# Allow local frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat(req: ChatRequest):
    reply = chatbot_response(req.text)
    return {"reply": reply}
