"""Score a locally served model on a starter's test set (exact match), and time it.

Usage: .venv/bin/python score_local.py <use-case> <port> [limit]
Sends each test row with the trained system prompt (task_description), temperature 0.
"""
import json
import sys
import time
from pathlib import Path

from openai import OpenAI

uc, port = sys.argv[1], sys.argv[2]
limit = int(sys.argv[3]) if len(sys.argv) > 3 else None
root = Path(__file__).resolve().parent.parent
system = json.load(open(root / "v2" / uc / "job_description.json"))["task_description"]
rows = [json.loads(l) for l in open(root / "v2" / uc / "test.jsonl")][:limit]
client = OpenAI(base_url=f"http://127.0.0.1:{port}/v1", api_key="EMPTY")

hits, times = 0, []
for r in rows:
    user, ref = r["messages"][0]["content"], r["messages"][1]["content"]
    t = time.time()
    out = client.chat.completions.create(model="local", temperature=0, max_tokens=64, messages=[
        {"role": "system", "content": system}, {"role": "user", "content": user}]).choices[0].message.content.strip()
    times.append(time.time() - t)
    hits += out == ref
print(f"{uc}: exact match {hits}/{len(rows)} = {hits / len(rows):.3f}; "
      f"median latency {sorted(times)[len(times) // 2] * 1000:.0f} ms")
