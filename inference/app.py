from fastapi import FastAPI
from pydantic import BaseModel
import sys
import time

from inference import generate

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # safe for demo
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------
# Request schema
# --------------------
class Prompt(BaseModel):
    prompt: str


# --------------------
# Cold-start readiness flag
# --------------------
MODEL_READY = False


# --------------------
# Startup warmup
# --------------------
@app.on_event("startup")
def warmup_model():
    global MODEL_READY
    try:
        print("WARMUP STARTED", flush=True)
        generate(
            "### Instruction:\nHello\n\n### Response:\n",
            max_new_tokens=5
        )
        MODEL_READY = True
        print("WARMUP COMPLETE", flush=True)
    except Exception as e:
        print("WARMUP FAILED:", e, flush=True)


# --------------------
# Health endpoint
# --------------------
@app.get("/health")
def health():
    return {
        "status": "ready" if MODEL_READY else "warming"
    }


# --------------------
# Generate endpoint
# --------------------
@app.post("/generate")
def generate_text(req: Prompt):
    print("REQUEST RECEIVED", flush=True)
    sys.stdout.flush()

    if not MODEL_READY:
        return {
            "response": "Model is waking up. Please retry in a few seconds."
        }

    if not req.prompt.strip():
        return {
            "response": "Please enter a prompt."
        }

    full_prompt = (
        "### Instruction:\n"
        f"{req.prompt}\n\n"
        "### Response:\n"
    )

    print("STARTING GENERATION", flush=True)
    sys.stdout.flush()

    start = time.time()
    response = generate(full_prompt)
    end = time.time()

    print(f"GENERATION FINISHED in {end - start:.2f}s", flush=True)
    sys.stdout.flush()

    return {"response": response}
