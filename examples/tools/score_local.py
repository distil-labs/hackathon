"""Score a locally served model on a Dataset's test set (exact match), and time it.

Usage: .venv/bin/python score_local.py <dataset-dir> [--port 8080] [--limit N] [--max-tokens 512]
Sends each test row with the trained system prompt (task_description from job_description.json),
temperature 0. Exact match suits labels and short fixed answers; for free text or JSON, read the
outputs it prints with --show, or compare with the platform's predictions.
"""
import argparse
import json
import time
from pathlib import Path

from openai import OpenAI

ap = argparse.ArgumentParser()
ap.add_argument("dataset_dir")
ap.add_argument("--port", default="8080")
ap.add_argument("--limit", type=int)
ap.add_argument("--max-tokens", type=int, default=512)
ap.add_argument("--show", action="store_true", help="print every output next to its reference")
a = ap.parse_args()

root = Path(a.dataset_dir)
system = json.load(open(root / "job_description.json"))["task_description"]
rows = [json.loads(l) for l in open(root / "test.jsonl")][:a.limit]
client = OpenAI(base_url=f"http://127.0.0.1:{a.port}/v1", api_key="EMPTY")

hits, times = 0, []
for r in rows:
    user, ref = r["messages"][0]["content"], r["messages"][1]["content"]
    t = time.time()
    out = client.chat.completions.create(model="local", temperature=0, max_tokens=a.max_tokens, messages=[
        {"role": "system", "content": system}, {"role": "user", "content": user}]).choices[0].message.content.strip()
    times.append(time.time() - t)
    hits += out == ref.strip()
    if a.show:
        print(f"--- reference: {ref.strip()[:200]}\n    output:    {out[:200]}")
print(f"{root.name}: exact match {hits}/{len(rows)} = {hits / len(rows):.3f}; "
      f"median latency {sorted(times)[len(times) // 2] * 1000:.0f} ms")
