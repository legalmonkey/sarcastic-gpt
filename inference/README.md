# Sarcastic LLM – Inference Server

This directory contains the production inference server for the
Sarcastic LLM.

## Run locally
pip install -r requirements.txt
uvicorn app:app --reload

## API
POST /generate
{
  "prompt": "Is college worth it?"
}
