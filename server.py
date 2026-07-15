from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from agent import Agent
from memory import save_memory
from tools.registry import list_tools
from fastapi.responses import Response

app = FastAPI(title="AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = Agent()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    tool_used: Optional[str] = None


@app.get("/favicon.ico")
async def favicon():
    return Response(status_code=204)


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        reply = agent.run(req.message)
        return ChatResponse(response=reply, tool_used=agent.last_tool_used)
    except Exception as e:
        return ChatResponse(response=f"Error: {e}", tool_used=None)


@app.get("/api/tools")
def get_tools():
    return {"tools": list_tools()}


@app.post("/api/clear")
def clear_conversation():
    save_memory([])
    return {"status": "cleared"}


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")