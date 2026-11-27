# distil labs hackathon, Nov 28-29 2026

Bring your own use case. In 1.5 days, build a small language model (0.6B to 4B) for it on the distil labs platform, make it match or beat its teacher, and run it offline on your laptop.

Your coding agent does the platform work with two skills: **distil-cli** (runs the jobs) and **[hackathon.md](hackathon.md)** (the hackathon's steps, settings and limits).

## Quick start

1. Clone this repo:

   ```bash
   git clone https://github.com/distil-labs/hackathon distil-hackathon
   cd distil-hackathon
   ```

2. Open your coding agent in this folder:
   - **Claude Code** loads the hackathon skill from `.claude/skills/distil-hackathon/` on its own.
   - **Other agents** (Codex, Cursor and others): tell it "Read hackathon.md and follow it."

3. Say: **"Let's start."** Your agent asks what you want to build, then sets up the CLI, credits and the distil-cli skill with you.

No idea yet? Ask your agent for ideas. It shows a few, including a voice agent.

## What is in this repo

| Path | What it is |
|---|---|
| [`hackathon.md`](hackathon.md) | The hackathon skill: steps, settings, running the model locally, pitfalls. Readable by people too |
| `.claude/skills/distil-hackathon/SKILL.md` | The same file, where Claude Code finds it |
| [`examples/`](examples) | 9 finished Datasets from our prep runs. References for the file format and the scores you can reach, not a menu |
| [`examples/tools/`](examples/tools) | `merge.py` (trained adapter to a local model), `agent_loop.py` (run an agent locally), `score_local.py` (score the local model) |

## Credits and help

- Every new account gets $50 at signup. For the hackathon you get **$150 on top**: post your account email in **#general** on the [distil labs Slack community](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g).
- The distil labs team on site: Vineeth, Maciej and Lev. Find us in person or in #general.
