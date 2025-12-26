from fastapi import FastAPI
import sys
import time

from inference import generate
from schemas import Prompt  # assuming this is where Prompt lives

app = FastAPI()

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
# Optional health endpoint (recommended)
# --------------------
@app.get("/health")
def health():
    return {
        "status": "ready" if MODEL_READY else "warming"
    }


# --------------------
# Generate endpoint (modified)
# --------------------
@app.post("/generate")
def generate_text(req: Prompt):
    print("REQUEST RECEIVED", flush=True)
    sys.stdout.flush()

    # ---- Cold start guard ----
    if not MODEL_READY:
        return {
            "response": "Model is waking up. Please retry in a few seconds."
        }

    # ---- Empty prompt guard ----
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
