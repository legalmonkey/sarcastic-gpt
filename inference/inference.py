import torch
from model_loader import model, encode, decode, DEVICE, block_size


@torch.no_grad()
def generate(
    prompt: str,
    max_new_tokens=120,
    temperature=0.7,
    top_k=40,
    frequency_penalty=0.8,
    presence_penalty=0.6,
):
    if not prompt.startswith(" "):
        prompt = " " + prompt

    idx = torch.tensor([encode(prompt)], dtype=torch.long).to(DEVICE)
    generated = []

    for _ in range(max_new_tokens):
        idx_cond = idx[:, -block_size:]
        logits, _ = model(idx_cond)
        logits = logits[:, -1, :] / temperature

        if generated:
            for tok in set(generated):
                logits[:, tok] -= presence_penalty
            for tok in generated:
                logits[:, tok] *= frequency_penalty

        if top_k is not None:
            v, _ = torch.topk(logits, top_k)
            logits[logits < v[:, [-1]]] = -float("inf")

        probs = torch.softmax(logits, dim=-1)
        next_id = torch.multinomial(probs, 1)

        generated.append(next_id.item())
        idx = torch.cat([idx, next_id], dim=1)

    

    text = decode(idx[0].tolist())

    # ---------- STOP AT NEXT INSTRUCTION ----------
    stop_token = "### Instruction:"
    prompt_len = len(prompt)

    if stop_token in text[prompt_len:]:
        text = text[: text.find(stop_token, prompt_len)]

    # ---------- EXTRACT FINAL RESPONSE ----------
    response_marker = "### Response:"

    if response_marker in text:
        # Take text AFTER the LAST response marker
        text = text.split(response_marker)[-1]

    return text.strip()
