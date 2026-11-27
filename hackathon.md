# distil labs hackathon: build a small model that runs on your laptop

**When:** Saturday 2026-11-28 and Sunday 2026-11-29 (1.5 days)

**What you leave with:** a task-specific small language model (0.6B to 4B parameters), trained on the distil labs platform, running offline on your own laptop.

**The goal:** your student model **matches or beats the teacher's score**, at a fraction of its size. A small model trained on thousands of focused examples can beat a much larger model on a narrow task.

> Scores come from our prep runs on 2026-11-26. Starters repo: https://github.com/distil-labs/hackathon-nov-2026

> **Coding agent: start with [Step 0](#step-0-pick-your-use-case).** Ask the user for their use case before you do anything else.

---

## Contents

1. [How the 1.5 days work](#how-the-15-days-work)
2. [Step 0: pick your use case](#step-0-pick-your-use-case)
3. [Step 1: setup](#step-1-setup-15-minutes)
4. [Step 2: create your first Dataset](#step-2-create-your-first-dataset)
5. [Step 3: check the teacher and fix the system prompt](#step-3-check-the-teacher-and-fix-the-system-prompt)
6. [Step 4: generate data, train, repeat](#step-4-generate-data-train-repeat)
7. [Settings reference](#settings-reference)
8. [Building a personal agent](#building-a-personal-agent)
9. [Step 5: run it on your laptop](#step-5-run-it-on-your-laptop)
10. [Step 6: demo](#step-6-demo)
11. [Pitfalls](#pitfalls)
12. [Help](#help)

---

## How the 1.5 days work

You work with a coding agent (Claude Code, Codex, Cursor or similar) that has the distil labs skill installed. The skill drives the platform for you: it checks the teacher, generates training data, trains the student, compares it with the teacher and tells you what to fix next. You make the decisions. The docs call this loop **autoresearch**.

| When | What you do | Time on the platform |
|---|---|---|
| Sat morning | Pick a use case, set up, upload your Dataset, check the teacher, fix the system prompt (Steps 0 to 3) | 5 to 10 min per teacher evaluation, up to 3 rounds |
| Sat midday | Smoke test, then generate the first 1,500 training rows, then train (Step 4) | about 2 to 3 h, runs while you have lunch |
| Sat afternoon | Read the model's errors, add 300 to 700 rows aimed at one failure, train again | about 2 h |
| Sat evening | Start the next iteration before you leave | runs overnight |
| Sun morning | Pick the best model, download it, run it on your laptop (Step 5) | about 30 min |
| Sun midday | Demo (Step 6) | |

**Rule that keeps you on time: start long jobs before breaks.** Data generation and training run on the platform, not on your laptop.

---

## Step 0: pick your use case

> **For the coding agent reading this file:** this is your first action. Ask the user which use case they want to build, with your question tool (multiple choice, one question). Offer the 9 starters below plus "Bring your own", each with its one-line description. Do not run setup, install anything or start any platform work until the user has answered.
>
> - **They pick a starter:** confirm it in one line, then go to Step 1.
> - **They pick "Bring your own":** ask the 7 questions below before anything else (free-text answers are fine). Write the answers into `use-case.md` and show it to the user to confirm.
>
> After that, use the settings in this file for every job, and price every billed job with `--dry-run` before you submit it.

**For you:** pick one. A starter saves about 3 hours: its test set, system prompt, mutators and config are ready and were checked in our prep runs. "Bring your own" is the most fun if you have a real problem.

| # | Starter | What the model does | Task type | Student | Teacher score | Our student score |
|---|---|---|---|---|---|---|
| 1 | **Personal agent** | Your own assistant: calendar, email drafts, notes, to-dos, reminders. Calls tools, reads results, asks before it sends anything | `chat-completion` + tools | Qwen3.5-4B (2B works too) | 0.93 judge · 0.72 tool calls | **0.93 · 0.76** ✅ |
| 2 | **Terminal copilot** | Plain English in, a bash command or script out. Works offline in your shell | `question-answering` | Qwen3.5-4B | 0.93 | 0.80 (gap left for you to close) |
| 3 | **Prompt-injection guard** | Labels a message `injection` or `benign` before it reaches your LLM app (English and German) | `question-answering` (labels) | Qwen3-0.6B | 0.987 | **0.974** (1.5 rows from the teacher) |
| 4 | **Gen Z translator** | Rewrites a normal sentence in Gen Z slang, same meaning, no cap | `question-answering` | Qwen3.5-4B (0.8B scores 0.91) | 0.977 | **0.993** ✅ beats |
| 5 | **Commit message writer** | Git diff in, one Conventional Commits line out. Use it as a git hook | `question-answering` | Qwen3.5-4B | 0.967 | 0.889 (gap left for you to close) |
| 6 | **Text-to-SQL** | Schema and question in, one SQL query out | `question-answering` | Qwen3.5-4B | 0.77 | 0.70 (gap left for you to close; about 13 test references are loose) |
| 7 | **Tool calling** | A finance and math assistant that answers by calling 12 tools, several at once when needed | `chat-completion` + tools | Qwen3.5-2B | 0.94 tool calls | **0.953** ✅ beats |
| 8 | **PII extraction** | Document in, every personal data span and its type out, as JSON (42 types) | `question-answering` (JSON) | Qwen3.5-4B (2B: 0.79) | 0.768 | **0.801** ✅ beats |
| 9 | **Invoice extraction** | OCR text of an invoice in, 14 fields plus line items out, as JSON | `question-answering` (JSON) | Qwen3.5-2B | 0.998 | **0.996** ✅ matches |
| 10 | **Bring your own** | Your task, your data. The skill asks you what the task is first | you choose | 0.6B to 4B | | |

Where each starter's test set comes from:

| Starter | Test set source |
|---|---|
| Personal agent | written by the teacher with separate test settings, then reviewed by hand |
| Terminal copilot | [`F-A-I-L/bash-instruct-55k`](https://hf.co/datasets/F-A-I-L/bash-instruct-55k) |
| Prompt-injection guard | [`deepset/prompt-injections`](https://hf.co/datasets/deepset/prompt-injections) |
| Gen Z translator | [`Programmer-RD-AI/genz-slang-pairs-1k`](https://hf.co/datasets/Programmer-RD-AI/genz-slang-pairs-1k) |
| Commit message writer | [`SalutefaceAAC/commit-messages-from-diffs`](https://hf.co/datasets/SalutefaceAAC/commit-messages-from-diffs) |
| Text-to-SQL | [`gretelai/synthetic_text_to_sql`](https://hf.co/datasets/gretelai/synthetic_text_to_sql) |
| Tool calling | [`lockon/xlam-function-calling-60k`](https://hf.co/datasets/lockon/xlam-function-calling-60k) (12-tool subset) |
| PII extraction | [`gretelai/gretel-pii-masking-en-v1`](https://hf.co/datasets/gretelai/gretel-pii-masking-en-v1) |
| Invoice extraction | [`hyperbots-inc/synthetic-invoice-extraction`](https://hf.co/datasets/hyperbots-inc/synthetic-invoice-extraction) |

### Bring your own: the questions your agent asks first

1. **The task in one sentence.** What does the model do? ("Turns a support email into a ticket category and priority.")
2. **What goes in.** Text, a conversation, a document, a diff, a schema? How long, roughly?
3. **What comes out.** A label from a fixed list, a short text, JSON with fixed fields, or tool calls?
4. **Three examples.** Three real inputs with the exact output you want for each.
5. **The data you have.** None, a few examples, a Hugging Face dataset, your own files, or traffic from an LLM you already run?
6. **The costly mistakes.** Which wrong answers hurt most? (A missed injection, a wrong amount, an email sent without asking.)
7. **Your laptop.** RAM and chip (for example M2, 16 GB). This sets the largest student you can run offline (Step 5).

Your agent turns the answers into the task type, the system prompt and the metric (Settings reference). Then go to Step 1.

---

## Step 1: setup (15 minutes)

Do this before Saturday if you can.

1. Install the distil CLI (macOS or Linux; on Windows run everything inside WSL):

   ```bash
   curl -fsSL https://cli-assets.distillabs.ai/install.sh | sh
   ```

   Already installed? Update it:

   ```bash
   distil update
   ```

2. Sign in. It opens your browser; check that the code matches and confirm it:

   ```bash
   distil auth
   ```

   No account yet? Run `distil signup` instead.

3. Add the distil labs skill to your coding agents:

   ```bash
   distil skill install
   ```

4. Install a local runtime for the finished model: [Ollama](https://ollama.com), or llama.cpp (`brew install llama.cpp` on a Mac).

5. Check your credits:

   ```bash
   distil billing balance
   ```

   **Credits:** every new account gets **$50** at signup. For the hackathon we add **$150 on top**: post your account email in **#general** on Slack and the team adds it. Need more later? Ask in Slack and we top you up. One full pass on a starter (teacher checks, 1,500 rows, a few trainings) cost us **$2 to $30**: short rows (labels, one sentence) are cheap, long rows (invoices, agent conversations) are not. $200 covers several iterations.

6. Join the distil labs Slack community: [join here](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g). The team is there all weekend to help.

**Check:** `distil --version` prints a version, and `distil whoami` prints your email.

---

## Step 2: create your first Dataset

A Dataset is one folder with up to five files:

```
my-task/
├── config.yaml            # models and settings (Settings reference below)
├── job_description.json   # the system prompt, the judge's rubric, generation instructions, tools
├── test.jsonl             # 50 to 150 rows you trust: this is how "better" is measured
├── train.jsonl            # 10 to 30 seed rows the teacher imitates (the personal-agent starter has none: the teacher works from the tools and the system prompt)
└── traces.jsonl           # optional: real traffic from an LLM you already run
```

### With a starter

1. Clone the starters repo from GitHub (it also holds the agent loop for Step 5):

   ```bash
   git clone https://github.com/distil-labs/hackathon-nov-2026 distil-hackathon
   cd distil-hackathon
   ```

2. Upload your starter:

   ```bash
   distil dataset create --data starters/<your-starter>
   ```

   It prints your Dataset id, and the Dataset shows at `https://app.distillabs.ai/datasets/<id>`.

3. Tell your agent:

   > Use the distil labs skill and the settings in hackathon.md. This is my root Dataset: `<id>`. The test set is agreed. Check the teacher, fix the system prompt if the teacher scores low, then keep iterating until the student matches or beats the teacher, for under $`<your budget>`.

### Bring your own

Tell your agent:

> Use the distil labs skill, the settings in hackathon.md and my answers in use-case.md to build a model that `<your task>`. Budget: $`<your budget>`.

The skill starts from your answers in `use-case.md`, asks for anything still missing, and writes the files with you. Plan 1 to 2 hours for this. **A good test set of 50 to 150 real examples matters more than anything else you do.** Write them yourself or take them from real data; never let the teacher grade its own homework.

---

## Step 3: check the teacher and fix the system prompt

The teacher writes all your training data, so fix its mistakes here, before you generate any data.

1. **Run a teacher evaluation** on your test set with `zai.glm-5.3-low-thinking`. It costs $0.02 to $2. Run it twice: the gap between the two runs is your **noise**, and any later difference smaller than that is not a real difference.
2. **Read the teacher's wrong answers.** Most are not the teacher being wrong; they are a convention your system prompt never states. Examples from our prep runs:
   - the teacher wrote rates as `4.5` where the test expects `0.045`;
   - it put the "Attn: name" line into an invoice address;
   - it wrote `~/Downloads` where the request said `downloads`;
   - it used SQLite syntax where the test answers use MySQL.
3. **Add each missing rule to `task_description`** (the system prompt) in `job_description.json`. Add one or two short examples if a rule is hard to say in words. Take examples from your seed rows, **never from the test set**.
4. **Run the teacher evaluation again.** Up to 3 rounds.
5. **Freeze it.** After the last round, the system prompt, the judge rubric and the test set do not change again. They define what "better" means; changing them makes every earlier score meaningless.

Fix **rules**, not rows: if you tune the prompt until the teacher gets these exact test rows right, it fits those rows, not the task.

If the teacher still scores low after 3 rounds, look at the test labels: public datasets often have wrong ones. Note them and move on; do not edit the test set.

---

## Step 4: generate data, train, repeat

### 4.1 Smoke before every generation run

Generate 128 rows first. Read 20 to 30 of them yourself and check:

- Are the answers right? (The validator, below, should catch most wrong ones.)
- Do the inputs look like your test inputs: same format, same length, same variety?
- Is the mix right? Count labels, tools, lengths, formats against your test set. In our prep runs the first smoke was off every time: invoices had 3 to 4 line items where the test has up to 12; injection attacks were all blatant where the test has subtle ones.

Fix the generation settings (mutators, generation instructions, validator) and smoke again. Smokes cost cents.

### 4.2 Generate the first train set

Run the full generation: **1,500 rows**. About 30 min to 3 h depending on row length.

### 4.3 Train

Iteration 1 trains a few models at once on the same data. Each training costs $0.10 to $2.60, so try two sizes:

| Your output is | Batch | Learning rate | What we measured (36 trainings) |
|---|---|---|---|
| a label, JSON, or tool calls | effective batch **16** | **2e-4** | as good or better than the default: guard 0.957 vs 0.922, PII 0.801 vs 0.792, tools and invoice equal |
| free text (rewrites, commit messages, commands) | platform default **1** | **5e-5** (default) | a little better than batch 16: Gen Z 0.927 vs 0.893, commit 0.856 vs 0.822 |

Train your starter's student **and one size up or down** in iteration 1. 4B beat 2B clearly on the terminal copilot (0.74 vs 0.55); 2B was already enough for invoices and tool calls.

Epochs: **3**, or **2** for long JSON outputs. A training itself takes about 5 to 30 minutes; with the evaluation afterwards, plan about 1 hour.

### 4.4 Read the errors and change one thing

Your agent groups the student's wrong answers into failure modes. Pick the biggest one and change **one** thing:

| What the errors show | What to change |
|---|---|
| the student is wrong where the teacher is right, in one kind of input | add 300 to 700 rows aimed at that kind (a new mutator value, weighted up) |
| the student copies a bad habit from the data | fix the generation instructions or the validator, then add rows |
| the student is close to the teacher with no clear pattern | try a bigger student, or one more epoch |
| the teacher is wrong too | the system prompt or the test labels; stop and decide (Step 3 is frozen) |

One change per iteration, or you cannot tell what helped. Training data only grows: add rows, never replace them, and **stop adding at 3,000 rows**.

### 4.5 Stop when

- the student **matches or beats the teacher** (within noise), or
- two iterations in a row do not improve it, or
- your budget or time is up.

Your agent logs every iteration (change, score, kept or not) in `iterations.md`.

---

## Settings reference

### config.yaml template

```yaml
base:
  task: question-answering                 # or chat-completion for tools and agents
  student_model_name: Qwen3.5-4B           # 0.6B to 4B, table below
  teacher_model_name: zai.glm-5.3-low-thinking
  llm_num_parallel_requests: 32
tuning:
  num_train_epochs: 3                      # 2 for long JSON outputs
  per_device_train_batch_size: 16          # 4B student or long rows: 4
  gradient_accumulation_steps: 1           # 4B student or long rows: 4  (4 x 4 = 16)
  learning_rate: 2e-4                      # with batch 16. Free-text tasks: leave all three out (batch 1, 5e-5)
evaluation:
  llm_as_a_judge_model_name: zai.glm-5.3-low-thinking   # set once, never change
synthgen:
  train_generation_target: 1500            # top-ups: 300 to 700
  validation_instructions: >-
    Work out the correct answer from the input yourself before reading the answer.
    Reject the example if the answer differs, invents a value the input does not give,
    or contains anything besides the answer.
  mutators:
    - name: kind                           # one mutator per thing to vary
      values:
        - "about ..."
        - "about ..."
```

### Settings that hold all hackathon

| Setting | Value | Why |
|---|---|---|
| `base.teacher_model_name` | `zai.glm-5.3-low-thinking` | the recommended large teacher; open-weight, so it may be distilled. Proprietary models (Claude, GPT, Gemini) are for evaluation only |
| `evaluation.llm_as_a_judge_model_name` | `zai.glm-5.3-low-thinking`, never changed | scores from two judges cannot be compared |
| `base.llm_num_parallel_requests` | 32 | faster generation and evaluation, same results, and every team's jobs keep moving |
| `base.student_model_name` | 0.6B to 4B (table below) | it must run on your laptop |
| `tuning.num_train_epochs` | 3; 2 for long JSON outputs | the docs say more epochs when the batch is bigger; 3 is enough for 1,500 to 3,000 rows |
| effective batch | 16 for labels, JSON and tool calls (`16 x 1` for short rows on 0.6B to 2B; `4 x 4` for 4B students and long rows); default 1 for free text | `16 x 1` ran out of GPU memory on a 4B student with SQL-length rows; `4 x 4` trains the same and fits |
| `tuning.learning_rate` | 2e-4 with batch 16; default 5e-5 with batch 1 | batch 16 takes 16 times fewer steps than batch 1, so each step must move further; confirmed on 9 starters |
| `synthgen.train_generation_target` | 1,500 first, 300 to 700 per top-up, 3,000 in total at most | covers the task and keeps each iteration to about 2 hours |
| `synthgen.validation_instructions` | always set (template above) | an LLM re-derives every generated answer and drops the wrong rows; the strongest data-quality setting |
| leave at default | `teacher_temperature` 0.7, `lora_r` 64, `learning_rate_scheduler` linear, `max_completion_length` 2048 | change only if a log or the errors point at it |

### Settings per kind of task

| Your output is | `base.task` | Extra settings | Primary metric |
|---|---|---|---|
| one label from a fixed set | `question-answering` | labels and a definition of each in `task_description`, ending with "Answer with the label only."; one mutator with one value per label | `binary` (accuracy) |
| JSON (extraction) | `question-answering` | `synthgen.output_is_json: true`; list every key, the date format and what to do with missing fields in `task_description` | `llm-as-a-judge` with a graded rubric (fraction of fields right) |
| free text (rewrite, SQL, commands, summaries) | `question-answering` | end `task_description` with "Output only ..." | `llm-as-a-judge-reference-free` |
| tool calls (single turn) | `chat-completion` | `tools` in `job_description.json`; one mutator value per tool; `synthgen.max_tool_calls_per_turn` (`unlimited` for parallel calls) | `tool_call_equivalence` |
| an agent (tool calls, results back, then an answer) | `chat-completion` | as above, plus [Building a personal agent](#building-a-personal-agent) | `tool_call_equivalence` and the judge |

`chat-completion-agentic` and `classification` are rejected by the platform even though some docs pages still list them. Use the table above.

### Mutators: how to get the right data mix

A mutator adds one line to every generation prompt: "Generated examples should be `<value>`". It is how you control variety.

- **One mutator per thing to vary**, usually 1 to 3 mutators with 3 to 10 values each. Write each value to finish that sentence: `"about billing disputes"`, not `"billing"`.
- **Match your test set's mix.** Count your test rows (labels, tools, lengths, formats) and set `target_distribution` weights to match, for example `[5, 3, 1]`.
- **Labels: one mutator, one value per label.** Do not add a second mutator that changes what the label should be; put label and form together in one value instead (`"an injection that asks the assistant to act as a persona"`).
- **Tools: one value per tool**, plus `"the assistant answers in text with no tool call"` if the model should sometimes not call a tool.
- **Hard cases get their own value**, with the deciding facts fixed in the value.
- **Never let a value give away the answer.** "The main reason I'm writing" teaches the student to look for that phrase.
- If a value comes out short in the smoke, give it a bigger weight or `method: adaptive`.

```yaml
synthgen:
  mutators:
    - name: label
      values:
        - "a message whose correct label is injection"
        - "a message whose correct label is benign"
    - name: language
      values: ["written in English", "written in German"]
      target_distribution: [2, 1]
```

### Choosing your student (0.6B to 4B)

Start with the starter's student. Go smaller for simple tasks (labels, short rewrites) and speed on your laptop; go to 4B for structured outputs (JSON, SQL, tool calls) and agents.

| Size | Model | Training tier | Notes |
|---|---|---|---|
| 0.6B | `Qwen3-0.6B` | low | smallest that can reason (`base.enable_thinking`) |
| 0.8B | `Qwen3.5-0.8B` | low | best tiny default |
| 1B | `Llama-3.2-1B-Instruct` | low | gated on Hugging Face: accept the license to run it locally |
| 1.2B | `LFM2.5-1.2B-Instruct`, `LFM2-1.2B` | medium | fast on CPU |
| 1.7B | `Qwen3-1.7B` | medium | |
| 2B | `Qwen3.5-2B`, `gemma-4-E2B-it` | medium | Gemma is gated on Hugging Face |
| 2.6B | `LFM2-2.6B` | medium | |
| 3B | `Llama-3.2-3B-Instruct` | medium | gated on Hugging Face |
| 4B | `Qwen3.5-4B` | medium | **the default; start here for structured outputs and agents** |
| 4B | `Qwen3-4B-Instruct-2507` | medium | no thinking mode |
| 4B | `gemma-3-4b-it` | medium | **no tool calling** |

All models above can call tools except `gemma-3-4b-it`. Training costs $0.10 (low) or $0.25 (medium) per 1M tokens times epochs: well under $1 per run at 1,500 rows.

### Money

Every billed command takes `--dry-run`, which prints the price and starts nothing. Your agent does this before every job; read the number it shows you. Balance and spending: https://app.distillabs.ai/billing. A job cancelled within 30 minutes of submitting is refunded; a failed job is refunded automatically.

---

## Building a personal agent

A personal agent is the most fun thing to build here, and the one that benefits most from running locally: your calendar and email never leave your laptop.

**Task type:** `chat-completion`, with your tools in `job_description.json`. Rows are whole conversations: user turns, assistant turns with `tool_calls`, `tool` messages with the results, and the assistant's answer.

**1. Declare your tools** in `job_description.json` (OpenAI function format, unique names):

```json
{
  "task_description": "You are a personal assistant with access to the user's calendar, notes and email drafts. Call a tool when it helps. Ask a short follow-up question when a required detail is missing. Never send, delete or change anything without the user's explicit confirmation in the conversation.",
  "tools": [
    {"type": "function", "function": {
      "name": "create_event",
      "description": "Create a calendar event.",
      "parameters": {"type": "object",
        "properties": {
          "title": {"type": "string"},
          "start": {"type": "string", "description": "ISO 8601 date-time"},
          "duration_minutes": {"type": "integer"}},
        "required": ["title", "start"]}}}
  ],
  "llm_as_a_judge_instructions": "Output 'good' if the assistant's turn calls the right tool with arguments taken from the conversation, or asks for a missing detail, or answers correctly from the tool results, and never acts without confirmation. Otherwise output 'bad'."
}
```

**2. One training row** (`train.jsonl`, one line; `arguments` is a JSON object, not a string):

```json
{"messages": [
  {"role": "user", "content": "Put lunch with Sam on Friday at 1pm"},
  {"role": "assistant", "tool_calls": [{"id": "call_1", "type": "function", "function": {"name": "create_event", "arguments": {"title": "Lunch with Sam", "start": "2026-11-27T13:00:00", "duration_minutes": 60}}}]},
  {"role": "tool", "tool_call_id": "call_1", "content": "{\"status\": \"created\", \"id\": \"evt_42\"}"},
  {"role": "assistant", "content": "Done: lunch with Sam is on your calendar for Friday at 1pm."}
]}
```

**3. Config differences:**

```yaml
base:
  task: chat-completion
  student_model_name: Qwen3.5-4B
synthgen:
  max_tool_calls_per_turn: unlimited      # if one turn may call several tools
  mutators:
    - name: tool
      values:
        - "a conversation that calls create_event"
        - "a conversation that calls search_notes"
        - "a conversation that calls draft_email"
        - "a conversation where a required detail is missing, so the assistant asks for it"
        - "a conversation where the user asks to send or delete something, so the assistant asks for confirmation first"
        - "a conversation the assistant answers in text with no tool call"
```

**4. The validator** is the most important setting for agents: "Reject the example if any tool argument is not stated in the conversation, if a tool is called for something the user did not ask, or if anything is sent, deleted or changed without the user's confirmation."

**5. Test set:** 50 to 100 conversations you write or check yourself, covering every tool, missing details, confirmations and no-tool answers. The skill can generate test rows with settings separate from your training settings; review every one.

**6. Run it:** serve the model on your laptop (Step 5), then run the loop from the starters repo. It sends your system prompt and tools exactly as trained, runs every tool call against local mock tools (a JSON file), feeds the results back, and prints the answer:

```bash
.venv/bin/python starters/tools/agent_loop.py --job-description starters/personal-agent/job_description.json --base-url http://127.0.0.1:8080/v1
```

Swap the mock functions in `starters/tools/agent_loop.py` for real ones (your calendar, mail client, notes) when you are ready. Tested on a MacBook with the 2B agent at 4-bit (1.2 GB): it booked an event, drafted an email, waited for "yes" before sending, and answered a weather question from the tool result.

Only students with tool calling work for agents: the Qwen3.5 family is the safe choice.

---

## Step 5: run it on your laptop

1. Download the best model:

   ```bash
   distil slm download --destination my-model <slm-id>
   tar -xf my-model/model.tar -C my-model
   ```

   You get the trained LoRA adapter (`model-adapter/`) and `config.yaml`, which names the base model and the LoRA rank. Keep both.

2. One-time setup (about 5 minutes; tested on a MacBook with Apple silicon, 16 GB):

   ```bash
   brew install llama.cpp
   git clone --depth 1 --branch b11669 https://github.com/ggml-org/llama.cpp llama.cpp-src
   python3 -m venv .venv && .venv/bin/pip install torch transformers peft accelerate openai ./llama.cpp-src/gguf-py
   ```

   Match the `--branch` tag to your installed llama.cpp (`llama-server --version`), so the converter and the server agree.

3. Merge the adapter into its base model, convert to GGUF and shrink it (`starters/tools/merge.py` is in the starters repo; it downloads the base model from Hugging Face). Run these from the cloned repo folder:

   ```bash
   .venv/bin/python starters/tools/merge.py my-model my-model-merged
   .venv/bin/python llama.cpp-src/convert_hf_to_gguf.py my-model-merged --outfile my-model-f16.gguf --outtype f16
   llama-quantize my-model-f16.gguf my-model.gguf Q4_K_M      # Q8_0 for models under 1B
   ```

4. Serve it (OpenAI-compatible API on port 8080):

   ```bash
   llama-server -m my-model.gguf --jinja --port 8080 --chat-template-kwargs '{"enable_thinking": false}'
   ```

   `--jinja` uses the model's own chat template, which tool calls need. `enable_thinking: false` matches how the starters were trained.

What we measured on a MacBook (M5, 16 GB):

| Model | File | Speed | Score on the laptop vs the platform |
|---|---|---|---|
| Injection guard, Qwen3-0.6B, Q8_0 | 610 MB | 35 ms per message | 113/116 = 0.974, same as the platform |
| Gen Z, Qwen3.5-0.8B, Q8_0 | 774 MB | about 150 ms per sentence | same style as the platform's predictions |
| Personal agent, Qwen3.5-2B, Q4_K_M | 1.2 GB | interactive | tool calls work through `agent_loop.py` |

We tested `llama-server`. Ollama should load the same GGUF (a Modelfile with `FROM ./my-model.gguf`, then `ollama create my-model -f Modelfile`), but we have not tested it with these models.

3. Always send the **same system prompt the model was trained with** (your `task_description`). A different prompt makes a fine-tuned model much worse.

---

## Step 6: demo

5 minutes per team. Show:

1. The task, and one input and output from your model **running locally** (network off, if you dare).
2. Your student's score next to the teacher's, and the size difference (for example 2B vs a model more than 100 times larger).
3. One iteration that worked, one that did not, and what you learned.

---

## Pitfalls

- **Training runs out of GPU memory** on long rows: halve `per_device_train_batch_size` and double `gradient_accumulation_steps`; if it still fails, add `tuning.memory_optimized_training: 1`. In our prep, `16 x 1` failed on a 4B student with SQL rows and `4 x 4` worked. Failed jobs are refunded.
- **More rules can make the teacher worse.** On Gen Z, two rounds of extra rules dropped the teacher from 0.98 to 0.93 and then 0.70: it got timid and wrote barely any slang. Keep the best round, not the last one.
- **Top-ups are priced from your rows' length.** A 700-row top-up cost $6.50 on commit diffs but $0.40 on short messages. Read the dry-run price before every submit.
- **Qwen3.5 models are vision-language models.** To merge the adapter locally, load the base with `AutoModelForImageTextToText`, not `AutoModelForCausalLM` (the starters' `merge.py` does this), or the adapter does not attach.
- **Public datasets have wrong labels.** Read 20 test rows before you trust any score. In our prep: the injection dataset labels harmless role-play as injection; about 13 of 150 SQL references answer a different reading of the question.
- **The task description and the test disagree** (SQLite vs MySQL, percent vs decimal). The teacher follows the prompt and loses points. Fix the prompt in Step 3.
- **The smoke's mix is off.** Count labels, tools and lengths in the 128 rows against your test set before the full run.
- **Generated tool conversations invent tool results** when you only want the calls. Say in the generation instructions what a conversation must look like.
- **Answers wrapped in code fences or followed by explanations** fail the metrics. End `task_description` with "Output only ...".
- **Tool schemas must be valid JSON Schema** and every call must match them; uploads reject rows that do not (for example `"0.5 * 15"` where a number is expected).
- **`distil dataset create` sometimes fails with `ECONNRESET`.** It is the connection, not your files: run it again.
- **`chat-completion-agentic` and `classification` are rejected.** Use `chat-completion` and `question-answering`.
- **Changing the judge, the test set or the system prompt after Step 3** makes all earlier scores meaningless.

---

## Help

- distil labs team on site: **Vineeth, Maciej and Lev**. Find us in person or in the [distil labs Slack community](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g) (channel: **#general**).
- Your agent: ask "what does the distil labs skill say about `<topic>`?"
- Docs: https://www.distillabs.ai/docs (the skill is more up to date where they differ)
- Jobs: https://app.distillabs.ai (`/datasets/<id>`, `/slms/<id>`), billing: https://app.distillabs.ai/billing
