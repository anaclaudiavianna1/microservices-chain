from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

# Inicializa FastAPI
app = FastAPI(title="service-c", version="1.0")

# Modelos de dados
class TraceEntry(BaseModel):
    service: str
    language: str
    info: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str

class Payload(BaseModel):
    message: str
    trace: List[TraceEntry] = Field(default_factory=list)

# Endpoint 
@app.get("/ping")
def ping():
    return {"ok": True, "service": "service-c"}

# Endpoint principal
@app.post("/stepC")
def step_c(payload: Payload):
    try:
        msg = payload.message
        length = len(msg)

        # nova entrada no trace
        entry = TraceEntry(
            service="service-c",
            language="Python",
            info={"appended_len": length},
            timestamp=datetime.utcnow().isoformat()
        )

        payload.trace.append(entry)

        return {
            "message": msg,
            "trace": payload.trace
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rodar o servidor 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("service_c:app", host="127.0.0.1", port=9003, reload=True)
