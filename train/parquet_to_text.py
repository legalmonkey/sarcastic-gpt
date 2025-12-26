import pandas as pd
import glob

OUTPUT = "wiki_clean.txt"

written_bytes = 0
MAX_MB = 200
LIMIT = MAX_MB * 1024 * 1024

with open(OUTPUT, "w", encoding="utf-8") as out:
    for fname in glob.glob("data/*.parquet"):
        print("Reading", fname)
        df = pd.read_parquet(fname)

        for text in df["text"]:
            if not isinstance(text, str):
                continue
            text = text.strip()
            if len(text) < 40:
                continue

            out.write(text + "\n")
            written_bytes += len(text.encode("utf-8"))

            if written_bytes >= LIMIT:
                break

        if written_bytes >= LIMIT:
            break

print(f"Saved {OUTPUT} (~{written_bytes / (1024*1024):.1f} MB)")
