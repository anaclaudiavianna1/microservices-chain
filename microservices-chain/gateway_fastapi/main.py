from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime
import httpx  

app = FastAPI(title="gateway", version="1.0")

class TraceEntry(BaseModel):
    service: str
    language: str
    info: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str

class Payload(BaseModel):
    message: str
    trace: List[TraceEntry] = Field(default_factory=list)

@app.get("/ping")
def ping():
    return {"ok": True, "service": "gateway"}

@app.get("/hello")
def hello(name: str = "Inconnu"):
    return {"message": f"Bonjour {name}!", "timestamp": datetime.utcnow()}

@app.post("/api/chain")
async def chain(payload: Payload):
    try:
        payload.trace.append(TraceEntry(
            service="gateway",
            language="Python (FastAPI)",
            info={"note": "iniciado no gateway"},
            timestamp=datetime.utcnow().isoformat()
        ))
        return payload
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
