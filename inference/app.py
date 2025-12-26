from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from inference import generate

app = FastAPI(title="Sarcastic LLM API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(req: Prompt):
    if not req.prompt.strip():
        return {"response": "Try asking something first."}

    full_prompt = (
        "### Instruction:\n"
        f"{req.prompt}\n\n"
        "### Response:\n"
    )

    return {"response": generate(full_prompt)}
