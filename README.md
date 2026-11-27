# distil labs hackathon, Nov 28-29 2026

Build a small language model (0.6B to 4B) on the distil labs platform, make it match or beat its teacher, and run it offline on your laptop.

**The full guide is [hackathon.md](hackathon.md).** Read it, or give it to your coding agent.

## Quick start

1. Clone this repo:

   ```bash
   git clone https://github.com/distil-labs/hackathon-nov-2026 distil-hackathon
   cd distil-hackathon
   ```

2. Open your coding agent (Claude Code, Codex, Cursor or similar) in this folder and tell it:

   > Read hackathon.md and follow it. Start with Step 0.

3. Your agent asks you which use case you want to build. Pick a starter or bring your own, then follow the guide.

## What is in this repo

| Path | What it is |
|---|---|
| [`hackathon.md`](hackathon.md) | The guide: setup, settings, the training loop, running the model locally, pitfalls |
| [`starters/`](starters) | 9 ready Datasets (config, system prompt, seed rows, test set), one folder per use case |
| [`starters/tools/`](starters/tools) | `merge.py` (adapter to a local model), `agent_loop.py` (personal agent loop), `score_local.py` (score a local model) |

## Starters

| Starter | Our student vs the teacher |
|---|---|
| Personal agent | matches (0.93 vs 0.93) |
| Gen Z translator | beats (0.993 vs 0.977) |
| Tool calling | beats (0.953 vs 0.94) |
| PII extraction | beats (0.801 vs 0.768) |
| Invoice extraction | matches (0.996 vs 0.998) |
| Prompt-injection guard | close (0.974 vs 0.987) |
| Commit message writer | gap for you to close (0.889 vs 0.967) |
| Terminal copilot | gap for you to close (0.80 vs 0.93) |
| Text-to-SQL | gap for you to close (0.70 vs 0.77) |

## Help

The distil labs team on site: Vineeth, Maciej and Lev. Ask in **#general** on the [distil labs Slack community](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g).
