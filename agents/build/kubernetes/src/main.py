import os
import uuid

from fastapi import FastAPI
from pydantic import BaseModel

from agent import run_agent


app = FastAPI(
    title="Kubernetes Troubleshooting Agent",
    version="1.0.0",
)


AGENT_NAME = os.getenv(
    "AGENT_NAME",
    "Kubernetes Troubleshooting Agent",
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "name": AGENT_NAME,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):

    result = run_agent(request.message)

    return ChatResponse(
        response=result,
    )


# OpenAI-compatible endpoint.
@app.get("/v1/models")
def models():

    return {
        "object": "list",
        "data": [
            {
                "id": "kubernetes-agent",
                "object": "model",
                "owned_by": "local",
            }
        ],
    }


@app.post("/v1/chat/completions")
def chat_completions(request: dict):

    messages = request.get("messages", [])

    user_message = ""

    for message in reversed(messages):
        if message.get("role") == "user":
            user_message = message.get("content", "")
            break

    result = run_agent(user_message)

    return {
        "id": f"chatcmpl-{uuid.uuid4()}",
        "object": "chat.completion",
        "model": "kubernetes-agent",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result,
                },
                "finish_reason": "stop",
            }
        ],
    }
