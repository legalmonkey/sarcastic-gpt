import torch
import sentencepiece as spm
from model_def import GPTLanguageModel, block_size

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load tokenizer
sp = spm.SentencePieceProcessor()
sp.load("bpe.model")

def encode(text: str):
    return sp.encode(text, out_type=int)

def decode(tokens):
    return sp.decode(tokens)

# Load model
model = GPTLanguageModel(vocab_size=sp.get_piece_size())
model.load_state_dict(
    torch.load("stage2_best.pt", map_location=DEVICE)
)
model.to(DEVICE)
model.eval()
