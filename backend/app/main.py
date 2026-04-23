from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.ai import router as ai_router
from backend.app.routes.orchestrator import router as orch_router

app = FastAPI(title="Agentic Nano AI Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)
app.include_router(orch_router)

@app.get("/")
def home():
    return {
        "message": "Agentic Nano AI Running",
        "endpoints": {
            "simple_task": "GET /api/payment-requirement → POST /api/execute-task",
            "complex_task": "GET /api/complex-task-requirement → POST /api/complex-task",
            "health": "GET /api/health"
        }
    }