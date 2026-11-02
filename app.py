"""TUKTUKI AI - Gemini-powered friendly companion. Developer credit: Noyon Sir."""
import os
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from google import genai

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="TUKTUKI AI", version="1.0.0")

SYSTEM_INSTRUCTION = (
    "You are TUKTUKI, a friendly, upbeat, respectful AI companion. Be warm and supportive, "
    "but do not claim to be human, a romantic partner, or to have real emotions. "
    "Keep responses concise and conversational. Respond in the user's language, including Bangla "
    "or Banglish when appropriate. Never request private information such as passwords, "
    "precise location, or personal account details."
)

class ChatMessage(BaseModel):
    role: Literal["user", "model"]
    content: str = Field(min_length=1, max_length=4000)

class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=24)

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "TUKTUKI AI", "developer": "Noyon Sir"}

@app.post("/api/chat")
async def chat(payload: ChatRequest):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY is not configured in Vercel Environment Variables.")
    try:
        client = genai.Client(api_key=api_key)
        history = []
        for item in payload.messages[-16:]:
            history.append({"role": item.role, "parts": [{"text": item.content}]})
        response = await client.aio.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=history,
            config={"system_instruction": SYSTEM_INSTRUCTION, "temperature": 0.8},
        )
        answer = (response.text or "I'm here. Could you try saying that another way?").strip()
        return {"reply": answer, "app": "TUKTUKI AI"}
    except HTTPException:
        raise
    except Exception as exc:
        # Avoid exposing upstream details or secrets to the browser.
        raise HTTPException(status_code=502, detail="Gemini could not respond right now. Please try again.") from exc

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(ROOT / "public" / "index.html")

@app.get("/{asset_path:path}", include_in_schema=False)
def static_assets(asset_path: str):
    candidate = (ROOT / "public" / asset_path).resolve()
    public_root = (ROOT / "public").resolve()
    if not candidate.is_relative_to(public_root) or not candidate.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(candidate)
