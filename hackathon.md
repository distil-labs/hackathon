---
name: distil-hackathon
description: Use when helping a team at the distil labs hackathon (Sat-Sun 2026-11-28/29) build their own small language model (0.6B to 4B) on the distil labs platform and run it offline on their laptop. Activate when the user says "hackathon", "let's start", "help me build my model", opens the distil-labs/hackathon repo, or asks about the hackathon settings, credits, examples, timing, local running or the demo. Works on top of the distil-cli skill, which runs the platform jobs.
---

# distil labs hackathon skill

You are the coding agent of a hackathon team. Over 1.5 days you help them build **their own** task-specific small model (0.6B to 4B parameters) on the distil labs platform, make it **match or beat the teacher's score**, and run it offline on their laptop.

This skill sets the hackathon's order of work, settings and limits. The **distil-cli** skill (installed in Step 1) runs every platform job: follow its workflow, gates and run log, with the settings in this file.

**The team brings their own use case.** The `examples/` folder holds 9 finished examples from our prep runs. They show what a good Dataset looks like and what scores are possible. They are references, not the menu: offer them only when the team has no idea yet, or wants to see a working format.

## Rules for you

1. **Ask for the use case first** (Step 0). Do not install, set up or start platform work before the team has told you what they want to build.
2. **Price every billed job with `--dry-run`** and tell the team the price before you submit. Never go over the budget they give you.
3. **The goal is that the student matches or beats the teacher.** A small model trained on a narrow task often beats a much larger one. Never describe the teacher's score as a limit.
4. **One change per iteration**, and log every iteration (change, score, kept or not) in `iterations.md`.
5. **After Step 3, never change the test set, the judge or the system prompt.** They define what "better" means.
6. **Start long jobs before breaks.** Generation and training run on the platform, not on the laptop.
7. Use the team's words for their task. Keep messages short: the team is busy building.

## The 1.5 days

| When | What happens | Time on the platform |
|---|---|---|
| Sat morning | Use case (Step 0), setup (Step 1), Dataset and test set (Step 2), teacher check (Step 3) | 5 to 10 min per teacher evaluation, up to 3 rounds |
| Sat midday | Smoke test, first 1,500 training rows, first trainings (Step 4) | about 2 to 3 h, runs over lunch |
| Sat afternoon | Read the errors, add 300 to 700 rows aimed at one failure, train again | about 2 h |
| Sat evening | Start the next iteration before the team leaves | runs overnight |
| Sun morning | Pick the best model, run it on the laptop (Step 5) | about 30 min |
| Sun midday | Demo (Step 6) | |

Tell the team where they are in this plan at every stop.

---

## Step 0: ask for the use case

This is your first action. Ask an open question:

> What do you want to build? Describe the task in a sentence or two. If you don't have an idea yet, say so and I'll show you some.

**If they have an idea**, ask these 7 questions (free-text answers are fine; ask only what their first answer did not already cover):

1. **The task in one sentence.** What does the model do? ("Turns a support email into a ticket category and priority.")
2. **What goes in.** Text, a conversation, a document, a diff, a schema? How long, roughly?
3. **What comes out.** A label from a fixed list, a short text, JSON with fixed fields, or tool calls?
4. **Three examples.** Three real inputs with the exact output they want for each.
5. **The data they have.** None, a few examples, a Hugging Face dataset, their own files, or traffic from an LLM they already run?
6. **The costly mistakes.** Which wrong answers hurt most? (A missed injection, a wrong amount, an email sent without asking.)
7. **Their laptop.** RAM and chip (for example M2, 16 GB). This sets the largest student they can run offline.

Write the answers into `use-case.md`, show it to the team, and get a yes. Then decide the task type and the metric from [Settings per kind of task](#settings-per-kind-of-task) and tell the team in one line.

**If the task does not fit** (it needs fresh world knowledge, long open-ended writing, or images on a non-vision student), say so in one line and help them narrow it to a bounded task a small model can own.

**If they have no idea**, show the [ideas](#ideas-when-a-team-has-none) and the [examples](#examples-from-our-prep-runs), help them pick or adapt one, then ask the 7 questions about it.

---

## Step 1: setup (15 minutes)

Check each item and do only what is missing. Show the team each command before you run it.

1. The distil CLI (macOS or Linux; on Windows, inside WSL):

   ```bash
   distil --version || curl -fsSL https://cli-assets.distillabs.ai/install.sh | sh
   distil update
   ```

2. Sign-in: `distil whoami` prints their email. If not, the team runs `distil auth` themselves (it opens the browser), or `distil signup` for a new account.
3. The distil-cli skill: `distil skill install`. Then load it.
4. A local runtime for the finished model: llama.cpp (`brew install llama.cpp` on a Mac).
5. Credits: `distil billing balance`. Every new account gets **$50** at signup. For the hackathon the team gets **$150 on top**: they post their account email in **#general** on the [distil labs Slack community](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g), and the distil labs team adds it. More on request in Slack.
6. Ask the team for their budget for the weekend, and write it in `iterations.md`. One full pass in our prep (teacher checks, 1,500 rows, a few trainings) cost **$2 to $30**: short rows (labels, one sentence) are cheap, long rows (documents, agent conversations) are not.

---

## Step 2: build the Dataset

A Dataset is one folder:

```
my-task/
├── config.yaml            # models and settings (Settings reference)
├── job_description.json   # system prompt, judge rubric, generation instructions, tools
├── test.jsonl             # 50 to 150 rows the team trusts: this is how "better" is measured
├── train.jsonl            # 10 to 30 seed rows the teacher imitates
└── traces.jsonl           # optional: real traffic from an LLM they already run
```

1. **Build the test set first.** It matters more than anything else in the weekend. Take it from real data (the team's files, a Hugging Face dataset, their traces), or write it with the team. Generated test rows are allowed only with settings separate from the training settings, and the team reviews every one. Read 20 rows of any public dataset before you trust it: public labels are often wrong.
2. **Write the seed rows** (10 to 30) from the team's examples. Never copy test rows into train.
3. **Write `job_description.json` and `config.yaml`** from `use-case.md` and the [Settings reference](#settings-reference). Look at the matching folder in `examples/` for the exact format of your task type.
4. **Upload:**

   ```bash
   distil dataset create --data my-task
   ```

   It prints the Dataset id. Show the team `https://app.distillabs.ai/datasets/<id>`. On `ECONNRESET`, run it again.

---

## Step 3: check the teacher and fix the system prompt

The teacher writes all the training data, so fix its mistakes here, before any data is generated.

1. **Run a teacher evaluation** on the test set with `zai.glm-5.3-low-thinking` ($0.02 to $2). Run it twice: the gap between the two runs is the **noise**. A later difference smaller than the noise is not a real difference.
2. **Read the teacher's wrong answers with the team.** Most are a convention the system prompt never states. From our prep runs: rates as `4.5` where the test expects `0.045`; an "Attn: name" line put into an address; `~/Downloads` where the request said `downloads`; SQLite syntax where the test uses MySQL.
3. **Add each missing rule to `task_description`.** Add one or two short examples if a rule is hard to say in words, taken from the seed rows, never from the test set.
4. **Run the teacher evaluation again.** Up to 3 rounds. Keep the best round, not the last: on one prep task, extra rules dropped the teacher from 0.98 to 0.70.
5. **Freeze** the system prompt, the judge rubric and the test set. Tell the team.

Fix **rules**, not rows. If the teacher is still low after 3 rounds, check the test labels, note the bad ones, and move on.

---

## Step 4: generate data, train, repeat

### 4.1 Smoke before every generation run

Generate 128 rows. Show the team 10 of them and check 20 to 30 yourself:

- Are the answers right? (The validator should catch most wrong ones.)
- Do the inputs look like the test inputs: same format, length and variety?
- Is the mix right? Count labels, tools, lengths and formats against the test set. In our prep the first smoke was off every time (invoices too short, attacks too blatant).

Fix the mutators, generation instructions or validator, and smoke again. Smokes cost cents.

### 4.2 Generate the first train set

**1,500 rows.** About 30 min to 3 h depending on row length.

### 4.3 Train

Iteration 1 trains two student sizes on the same data ($0.10 to $2.60 each):

| The output is | Batch | Learning rate | What we measured (36 trainings) |
|---|---|---|---|
| a label, JSON, or tool calls | effective batch **16** | **2e-4** | as good or better than the default (guard 0.957 vs 0.922, PII 0.801 vs 0.792) |
| free text (rewrites, commit messages, commands) | platform default **1** | **5e-5** (default) | a little better than batch 16 (Gen Z 0.927 vs 0.893) |

Epochs: **3**, or **2** for long JSON outputs. A training takes 5 to 30 minutes; with its evaluation, plan about 1 hour.

### 4.4 Read the errors and change one thing

Group the student's wrong answers into failure modes, show the team the biggest one, and change **one** thing:

| What the errors show | What to change |
|---|---|
| wrong where the teacher is right, in one kind of input | add 300 to 700 rows aimed at it (a new mutator value, weighted up) |
| a bad habit copied from the data | fix the generation instructions or the validator, then add rows |
| close to the teacher, no clear pattern | a bigger student, or one more epoch |
| the teacher is wrong too | the prompt or the test labels: stop and decide with the team (Step 3 is frozen) |

Training data only grows: add rows, never replace them, and **stop adding at 3,000 rows**.

### 4.5 Stop when

- the student **matches or beats the teacher** (within the noise), or
- two iterations in a row do not improve it, or
- the budget or the time is up.

Then report: the best model, its score next to the teacher's, what each iteration changed, and the money spent.

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
| `base.teacher_model_name` | `zai.glm-5.3-low-thinking` | open-weight, so it may be distilled. Proprietary models (Claude, GPT, Gemini) are for evaluation only |
| `evaluation.llm_as_a_judge_model_name` | `zai.glm-5.3-low-thinking`, never changed | scores from two judges cannot be compared |
| `base.llm_num_parallel_requests` | 32 | faster generation and evaluation, and every team's jobs keep moving |
| `base.student_model_name` | 0.6B to 4B (table below) | it must run on the laptop |
| `tuning.num_train_epochs` | 3; 2 for long JSON outputs | enough for 1,500 to 3,000 rows |
| effective batch | 16 for labels, JSON and tool calls (`16 x 1` for short rows on 0.6B to 2B; `4 x 4` for 4B and long rows); default 1 for free text | `16 x 1` ran out of GPU memory on a 4B student with long rows; `4 x 4` trains the same |
| `tuning.learning_rate` | 2e-4 with batch 16; default 5e-5 with batch 1 | batch 16 takes 16 times fewer steps, so each step must move further |
| `synthgen.train_generation_target` | 1,500 first, 300 to 700 per top-up, 3,000 in total at most | covers the task, keeps each iteration to about 2 hours |
| `synthgen.validation_instructions` | always set (template above) | an LLM re-derives every answer and drops wrong rows |
| leave at default | `teacher_temperature` 0.7, `lora_r` 64, `learning_rate_scheduler` linear, `max_completion_length` 2048 | change only if a log or the errors point at it |

### Settings per kind of task

| The output is | `base.task` | Extra settings | Primary metric | Example to copy |
|---|---|---|---|---|
| one label from a fixed set | `question-answering` | labels and a definition of each in `task_description`, ending with "Answer with the label only."; one mutator with one value per label | `binary` (accuracy) | `examples/prompt-injection-guard` |
| JSON (extraction) | `question-answering` | `synthgen.output_is_json: true`; list every key, the date format and what to do with missing fields | `llm-as-a-judge` with a graded rubric | `examples/invoice-extraction`, `examples/pii-extraction` |
| free text (rewrite, SQL, commands, summaries) | `question-answering` | end `task_description` with "Output only ..." | `llm-as-a-judge-reference-free` | `examples/genz-translator`, `examples/text-to-sql` |
| tool calls (single turn) | `chat-completion` | `tools` in `job_description.json`; one mutator value per tool; `synthgen.max_tool_calls_per_turn` (`unlimited` for parallel calls) | `tool_call_equivalence` | `examples/tool-calling` |
| an agent (tool calls, results back, then an answer) | `chat-completion` | as above, plus [Agents](#agents) | `tool_call_equivalence` and the judge | `examples/personal-agent` |

`chat-completion-agentic` and `classification` are rejected by the platform even though some docs pages list them.

### Mutators: the right data mix

A mutator adds one line to every generation prompt: "Generated examples should be `<value>`".

- **One mutator per thing to vary**, usually 1 to 3 mutators with 3 to 10 values each. Write each value to finish that sentence: `"about billing disputes"`, not `"billing"`.
- **Match the test set's mix** with `target_distribution` weights, for example `[5, 3, 1]`.
- **Labels: one mutator, one value per label.** Put label and form together in one value (`"an injection that asks the assistant to act as a persona"`).
- **Tools: one value per tool**, plus `"the assistant answers in text with no tool call"` when needed.
- **Hard cases get their own value**, with the deciding facts fixed in the value.
- **Never let a value give away the answer.**
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

### Choosing the student (0.6B to 4B)

Go small for simple tasks (labels, short rewrites) and speed; go to 4B for structured outputs (JSON, SQL, tool calls) and agents. Check the laptop's RAM from Step 0: a 4B model at 4-bit needs about 2.5 GB.

| Size | Model | Training tier | Notes |
|---|---|---|---|
| 0.6B | `Qwen3-0.6B` | low | smallest that can reason (`base.enable_thinking`) |
| 0.8B | `Qwen3.5-0.8B` | low | best tiny default |
| 1B | `Llama-3.2-1B-Instruct` | low | gated on Hugging Face |
| 1.2B | `LFM2.5-1.2B-Instruct`, `LFM2-1.2B` | medium | fast on CPU |
| 1.7B | `Qwen3-1.7B` | medium | |
| 2B | `Qwen3.5-2B`, `gemma-4-E2B-it` | medium | Gemma is gated on Hugging Face |
| 2.6B | `LFM2-2.6B` | medium | |
| 3B | `Llama-3.2-3B-Instruct` | medium | gated on Hugging Face |
| 4B | `Qwen3.5-4B` | medium | **the default for structured outputs and agents** |
| 4B | `Qwen3-4B-Instruct-2507` | medium | no thinking mode |
| 4B | `gemma-3-4b-it` | medium | **no tool calling** |

Training costs $0.10 (low) or $0.25 (medium) per 1M tokens times epochs: well under $1 per run at 1,500 rows.

### Money

Every billed command takes `--dry-run`, which prints the price and starts nothing. Balance and spending: https://app.distillabs.ai/billing. A job cancelled within 30 minutes is refunded; a failed job is refunded automatically.

---

## Agents

Agents are a popular choice, and they gain the most from running locally: the team's calendar and email never leave the laptop.

**Task type:** `chat-completion`, with the tools in `job_description.json`. Rows are whole conversations: user turns, assistant turns with `tool_calls`, `tool` messages with results, and the assistant's answer. See `examples/personal-agent/` for a full working Dataset with 10 tools.

**Tools** (OpenAI function format, unique names, valid JSON Schema):

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

**One training row** (one line; `arguments` is a JSON object, not a string):

```json
{"messages": [
  {"role": "user", "content": "Put lunch with Sam on Friday at 1pm"},
  {"role": "assistant", "tool_calls": [{"id": "call_1", "type": "function", "function": {"name": "create_event", "arguments": {"title": "Lunch with Sam", "start": "2026-11-27T13:00:00", "duration_minutes": 60}}}]},
  {"role": "tool", "tool_call_id": "call_1", "content": "{\"status\": \"created\", \"id\": \"evt_42\"}"},
  {"role": "assistant", "content": "Done: lunch with Sam is on your calendar for Friday at 1pm."}
]}
```

**Config:** `base.task: chat-completion`, `synthgen.max_tool_calls_per_turn: unlimited` if one turn may call several tools, and a mutator with one value per tool plus values for "a required detail is missing, so the assistant asks for it", "the user asks to send or delete something, so the assistant asks for confirmation first" and "the assistant answers in text with no tool call".

**Validator** (the most important agent setting): "Reject the example if any tool argument is not stated in the conversation, if a tool is called for something the user did not ask, or if anything is sent, deleted or changed without the user's confirmation."

**Test set:** 50 to 100 conversations covering every tool, missing details, confirmations and no-tool answers, reviewed by the team.

**Run it locally** after Step 5 with the loop in `examples/tools/agent_loop.py`. It sends the system prompt and tools exactly as trained, runs each tool call against mock tools in a JSON file, and feeds the results back:

```bash
.venv/bin/python examples/tools/agent_loop.py --job-description my-task/job_description.json --base-url http://127.0.0.1:8080/v1
```

Replace the mock functions with the team's own tools. Only students with tool calling work for agents: the Qwen3.5 family is the safe choice.

---

## Step 5: run it on the laptop

1. Download the best model:

   ```bash
   distil slm download --destination my-model <slm-id>
   tar -xf my-model/model.tar -C my-model
   ```

   This gives the LoRA adapter (`model-adapter/`) and `config.yaml`.

2. One-time setup (about 5 minutes; tested on a MacBook with Apple silicon, 16 GB). Match the `--branch` tag to `llama-server --version`:

   ```bash
   brew install llama.cpp
   git clone --depth 1 --branch b11669 https://github.com/ggml-org/llama.cpp llama.cpp-src
   python3 -m venv .venv && .venv/bin/pip install torch transformers peft accelerate openai ./llama.cpp-src/gguf-py
   ```

3. Merge the adapter into its base model, convert to GGUF and shrink it (`merge.py` downloads the base model from Hugging Face):

   ```bash
   .venv/bin/python examples/tools/merge.py my-model my-model-merged
   .venv/bin/python llama.cpp-src/convert_hf_to_gguf.py my-model-merged --outfile my-model-f16.gguf --outtype f16
   llama-quantize my-model-f16.gguf my-model.gguf Q4_K_M      # Q8_0 for models under 1B
   ```

4. Serve it (OpenAI-compatible API on port 8080):

   ```bash
   llama-server -m my-model.gguf --jinja --port 8080 --chat-template-kwargs '{"enable_thinking": false}'
   ```

5. Check the laptop model against the platform on the test set (exact match; add `--show` to read free-text or JSON outputs):

   ```bash
   .venv/bin/python examples/tools/score_local.py my-task --port 8080
   ```

Always send the **same system prompt the model was trained with**. A different prompt makes a fine-tuned model much worse.

What we measured on a MacBook (M5, 16 GB):

| Model | File | Speed | Laptop score vs platform |
|---|---|---|---|
| Injection guard, Qwen3-0.6B, Q8_0 | 610 MB | 35 ms per message | 0.974, same as the platform |
| Gen Z translator, Qwen3.5-0.8B, Q8_0 | 774 MB | about 150 ms per sentence | same style as the platform |
| Personal agent, Qwen3.5-2B, Q4_K_M | 1.2 GB | interactive | tool calls work through `agent_loop.py` |

Ollama should load the same GGUF (`FROM ./my-model.gguf` in a Modelfile, then `ollama create`), but we have not tested it.

---

## Step 6: demo

5 minutes per team. Help the team prepare:

1. The task, and one input and output from their model **running locally** (network off, if they dare).
2. The student's score next to the teacher's, and the size difference (for example 2B vs a model more than 100 times larger).
3. One iteration that worked, one that did not, and what they learned (from `iterations.md`).

---

## Pitfalls

- **GPU out of memory** on long rows: halve `per_device_train_batch_size` and double `gradient_accumulation_steps`; if it still fails, add `tuning.memory_optimized_training: 1`. Failed jobs are refunded.
- **More rules can make the teacher worse.** Keep the best round, not the last.
- **Top-ups are priced from row length.** 700 rows cost $6.50 on commit diffs but $0.40 on short messages. Read the dry-run price.
- **Qwen3.5 models are vision-language models.** To merge locally, load the base with `AutoModelForImageTextToText` (`merge.py` does this), or the adapter does not attach.
- **Public datasets have wrong labels.** Read 20 test rows before trusting any score.
- **The task description and the test disagree** (SQLite vs MySQL, percent vs decimal). Fix the prompt in Step 3.
- **Generated tool conversations invent tool results** when only the calls are wanted. Say in the generation instructions what a conversation must look like.
- **Answers in code fences or with explanations** fail the metrics. End `task_description` with "Output only ...".
- **`distil dataset create` fails with `ECONNRESET`:** the connection, not the files. Run it again.

---

## Ideas when a team has none

Show these only when asked. Each is a bounded task a small model can own on a laptop.

- **Voice agent:** talk to your model and it answers out loud. Our use-case checker pairs a trained Qwen3.5-4B (0.89 vs the teacher's 0.80) with Gradium's open-source Phonon voice model (31M parameters), both on a laptop: [blog post](https://www.distillabs.ai/blog/how-we-use-gradiums-phonon-to-chat-with-you-about-your-post-trained-small-model-use-case). For voice, keep the model's answers short. A banking voice assistant with a 0.6B model: [VoiceTeller](https://github.com/distil-labs/distil-voice-assistant-banking).
- **Personal agent:** calendar, email drafts, notes, reminders, all offline.
- **A filter in front of an LLM app:** injection guard, PII redaction, topic router.
- **Developer tools:** commit messages, shell commands, log triage, test names.
- **Extraction from documents** the team deals with: receipts, contracts, emails, job posts.
- **A style or format rewriter:** tone, reading level, slang, release notes.

## Examples from our prep runs

Finished Datasets in `examples/`, built on 2026-11-26 with the settings in this skill. Use them for the file format of a task type, or as a fallback if a team is stuck. Three still have a gap to the teacher.

| Example | What the model does | Task type | Student | Teacher | Student score |
|---|---|---|---|---|---|
| `personal-agent` | assistant with 10 tools (calendar, email, notes, tasks); asks before sending | `chat-completion` + tools | Qwen3.5-4B | 0.93 judge | **0.93**, matches |
| `genz-translator` | normal sentence in, Gen Z slang out | `question-answering` | Qwen3.5-4B | 0.977 | **0.993**, beats |
| `tool-calling` | finance and math assistant with 12 tools | `chat-completion` + tools | Qwen3.5-2B | 0.94 | **0.953**, beats |
| `pii-extraction` | every personal data span and its type, as JSON | `question-answering` (JSON) | Qwen3.5-4B | 0.768 | **0.801**, beats |
| `invoice-extraction` | 14 fields plus line items from invoice text, as JSON | `question-answering` (JSON) | Qwen3.5-2B | 0.998 | **0.996**, matches |
| `prompt-injection-guard` | `injection` or `benign` (English and German) | `question-answering` (labels) | Qwen3-0.6B | 0.987 | 0.974 |
| `commit-writer` | git diff in, one Conventional Commits line out | `question-answering` | Qwen3.5-4B | 0.967 | 0.889, gap |
| `terminal-copilot` | plain English in, a bash command out | `question-answering` | Qwen3.5-4B | 0.93 | 0.80, gap |
| `text-to-sql` | schema and question in, one SQL query out | `question-answering` | Qwen3.5-4B | 0.77 | 0.70, gap |

Test sets come from public Hugging Face datasets (`deepset/prompt-injections`, `gretelai/gretel-pii-masking-en-v1`, `gretelai/synthetic_text_to_sql`, `lockon/xlam-function-calling-60k`, `hyperbots-inc/synthetic-invoice-extraction`, `F-A-I-L/bash-instruct-55k`, `Programmer-RD-AI/genz-slang-pairs-1k`, `SalutefaceAAC/commit-messages-from-diffs`); the personal-agent test set was generated with separate settings and reviewed. `personal-agent/train.jsonl` is empty on purpose: the teacher works from the tools and the system prompt.

## Help

- distil labs team on site: **Vineeth, Maciej and Lev**, in person or in **#general** on the [distil labs Slack community](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g). Send the team there for credits, platform errors or a stuck job.
- Platform questions: the distil-cli skill first, then https://www.distillabs.ai/docs.
- Jobs: https://app.distillabs.ai (`/datasets/<id>`, `/slms/<id>`). Billing: https://app.distillabs.ai/billing.
