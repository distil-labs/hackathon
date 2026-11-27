---
name: distil-hackathon
metadata:
  version: "1.0.0"
description: >
  Use at the distil labs hackathon (Sat-Sun 2026-11-28/29), when a team builds their own small
  model (0.6B to 4B) on the distil labs platform and runs it offline on their laptop. Activate
  for "let's start the hackathon", "help me build my model for the hackathon", "what should we
  build", "how do we go faster", "how do I get the hackathon credits", "run my model locally",
  "prepare our demo", or whenever the user works in the distil-labs hackathon repo, even if
  they do not say "hackathon". Sits on top of the distil-cli skill: distil-cli runs the
  workflow and every platform job; this skill adds the hackathon's speed rules, fixed settings,
  time limits and laptop inference.
---

# distil labs hackathon

A team brings **their own use case** and has 1.5 days to build a small model for it that
**matches or beats the teacher**, then runs it offline on their laptop.

**distil-cli does the work.** Follow its workflow, gates, run log, make-rows and error-analysis
protocols as written, except the two steps [skipped for speed](#the-weekend-step-by-step). This
file only adds what the hackathon changes: how to iterate fast and run fast. Where the two
differ, this file wins for the weekend.

## Start: ask for the use case

Your first message, before any install or platform job:

> What do you want to build? Describe the task in a sentence or two. If you don't have an idea
> yet, say so and I'll show you some.

Then run distil-cli Phase 1, asking these together in one message (the team is short on time):
the task in one sentence; what goes in; what comes out (label, short text, JSON, tool calls);
three real examples with the exact outputs; the data they have (none is fine, see
[starting with no data](#starting-with-no-data)); the costly mistakes; their laptop's RAM and
chip (it caps the student size). Save the answers in `use-case.md`.

If the task needs fresh world knowledge, long open-ended writing, or images on a text model, say
so and narrow it to the one bounded step a model must do every time.

No idea yet? Show the [ideas](#ideas-and-examples) first. The `examples/` folder holds 9
finished Datasets: references for the file format, not a menu.

## Setup in 10 minutes

```bash
distil --version || curl -fsSL https://cli-assets.distillabs.ai/install.sh | sh
distil update
distil auth
distil skill install             # DO NOT OMIT THIS, this is your skill dependency
distil billing balance
brew install llama.cpp           # now, so Sunday morning is not spent on installs
```

Credits: $50 at signup, plus **$150** for the hackathon when the team posts their account email
in **#general** on the [distil labs Slack](https://join.slack.com/t/distil-labs-community/shared_invite/zt-36zqj87le-i3quWUn2bjErRq22xoE58g).
More on request. Ask the team for their weekend budget and put it in the run log.

## Starting with no data

Most teams arrive with an app idea and no dataset. That is fine: tell the team so, and do not
send them off to collect rows. The task description and their three examples are enough to
bootstrap the root Dataset, and synthetic generation writes the training data from there.

- **The test set:** about 100 to 150 rows covering the edge cases and the costly mistakes in
  `use-case.md`, made with distil-cli's make-rows protocol into the test split. For an agent,
  that is 100 to 150 conversations covering the real scenarios.
- **The seed rows:** the team's three examples in `train.jsonl`, never in the test set. Do not
  write more to reach a count: the first train set generation fills the split. An agent with
  well-described tools needs none ([agents](#agents)).
- **Review with the team:** read 15 to 20 test rows together and fix whatever does not match
  their real app. The teacher wrote these rows and is then scored on them, so this review is
  what makes the score mean something.
- **Freeze after the teacher rounds**, with the prompt, not before. The teacher labelled the
  test rows under the round-1 prompt, so when a later round adds a rule, correct the test rows
  that break it as a local fix and log it in the run log.

## The weekend, step by step

distil-cli runs every step below with its own commands and its own run directory layout; use
both as written. Times are what our prep jobs took from submit to finish with
`llm_num_parallel_requests: 32`; with many teams on the platform, queueing can add to them.

| Step | In distil-cli | Time |
|---|---|---|
| Upload the root Dataset | Phase 0 | seconds |
| No data: generate the test set from the task description and the team's examples ([no data](#starting-with-no-data)) | Phase 3, make-rows into the test split | a smoke and a full run, minutes each |
| Teacher check: up to 3 prompt rounds, each a new root Dataset ([when the teacher scores low](#when-the-teacher-scores-low)); with no data, download the test set once and put its `test.jsonl` in every new root | Phases 2 and 3 | about 5 minutes a round |
| Smoke the first train set | make-rows, Step 2 | 2 to 4 minutes |
| Generate the first train set | Phase 4, iteration 1 | 5 minutes for short rows, about 25 for long documents |
| Train two sizes at once | Phase 4, Step 3 | about 30 minutes for 2B, about 50 for 4B, evaluation included |
| Top up the best Dataset and train again | Phase 4, later iterations | 1 to 1.5 hours per iteration |

That fits 4 to 6 iterations between Saturday midday and Sunday morning. A job cancelled within
30 minutes of submitting is refunded.

**Skipped for speed.** To fit more iterations in, skip two distil-cli steps, and note each skip
in the run log:

- **The blind review of a smoke** (make-rows, Step 3). Read the smoke rows yourself instead and
  show the team a few. Bring it back when a full run's rows turn out wrong, or the student
  repeats a mistake the rows taught it.
- **The memory smoke before training** (train-model, Step 3). The batch sizes in
  [settings per kind of output](#settings-per-kind-of-output) fit in memory in our prep. Bring it
  back for a student or a row length our prep did not cover, or after an out-of-memory failure.

## How to iterate fast

1. **Run in parallel, never in a queue.** Submit both noise-check teacher evaluations at once.
   Train two student sizes at once on the same data. Smoke the next top-up while a training
   runs. Several teams' jobs share the platform, so `llm_num_parallel_requests: 32` keeps each
   one moving.
2. **Start long jobs before breaks.** Generation and training run on the platform. A job
   started before lunch or before the team leaves on Saturday is free time.
3. **The target is the teacher's score.** Skip distil-cli's extra target models: they cost an
   hour and credits the team needs for training. The student can beat the teacher (4 of our 9
   prep tasks did); never call the teacher's score a limit.
4. **Fix the system prompt before data, not after.** Teacher mistakes become the student's. Read the
   teacher's wrong answers with the team; most are a convention the prompt never states (`4.5`
   vs `0.045`, SQLite vs MySQL). Add rules, not test rows. **Keep the best round, not the last**:
   extra rules once dropped a teacher from 0.977 to 0.70. Then freeze the prompt, judge and test
   set ([when the teacher scores low](#when-the-teacher-scores-low)).
5. **Smoke 128 rows before every generation.** Check answers, input shape and the mix against
   the test set ([mutators](#mutators-get-the-mix-right-in-one-smoke)). Every first smoke in our prep was off. Smokes cost cents; a wrong 1,500-row run
   costs an afternoon.
6. **Small, aimed top-ups.** 1,500 rows first, then 300 to 700 rows aimed at the biggest failure
   mode ([what to change](#what-to-change-after-each-training)), 3,000 in total at most. Bigger runs make each iteration too slow for the weekend.
7. **One change per iteration.** With 4 to 6 iterations in the weekend, a change you
   cannot trace is a wasted one.
8. **Price with `--dry-run` and say the price.** Generation is priced by row length: 700 rows
   cost $6.50 on code diffs and $0.40 on short messages.
9. **Stop** when the student matches or beats the teacher within the noise, two iterations in a
   row do not improve it, the budget is spent, or the last training would not finish before Sunday morning.

### When the teacher scores low

A low teacher in round 1 is normal and fixable. Each round is two teacher evaluations at once
(about 5 minutes, under $2), so up to 3 rounds fit in the first hour. Submit both runs of a round at
once.

**Round 1.** Run the teacher twice on the test set. The gap between the two runs is the noise.
Read every wrong answer with the team and sort each one:

| The wrong answer is | Do this in round 2 |
|---|---|
| a convention the prompt never states (format, units, naming, dialect, what counts as which label) | add one short rule per convention to `task_description` |
| a hard case the rule alone does not explain | add one or two short examples from the seed rows, never from the test set |
| right, and the test label is wrong | note it in the run log; do not change the test set |
| a style or tone choice | leave it: style rules make the teacher timid |

**Round 2.** Run the teacher twice again with the new prompt, and compare the means:

- **up by more than the noise:** keep it. If wrong answers of a new kind show up, do one more
  round.
- **within the noise:** the rules did not matter. What is left is mostly test labels or genuine
  ambiguity. Freeze and move on.
- **down:** revert to the best round. Rules that narrow the style hurt.

**Round 3** (only if round 2 helped and a clear new convention showed up): same as round 2.
Then freeze the best round, not the last.

What happened in our prep (same teacher and judge, mean of 2 runs):

| Task | Round 1 | What the teacher got wrong | Rule added | Round 2 | Kept |
|---|---|---|---|---|---|
| commit messages | 0.94 | `chore` and `fix` changes labelled `feat` | the type definitions; "adding validation is `fix`"; "config, build and CI changes are `chore`" | **0.967** | round 2 |
| PII extraction | 0.745 | lists merged into one span; coded IDs skipped outside medical text | "values in a list are separate spans"; "label every code by its prefix" | **0.768** | round 2 |
| text-to-SQL | 0.75 | "in X and Y" read as both; group-by column left out | 4 conventions the reference answers follow | 0.77 (runs 0.79 and 0.75: within the noise) | round 2, then froze: the rest were loose test labels |
| Gen Z translator | 0.977 | almost nothing | "never add a reaction", then rules on slang intensity | 0.93, then **0.70** | round 1: the rules made the teacher write barely any slang |

**A teacher at 0.75 is not a dead end.** The validator drops the teacher's wrong rows before the
student sees them, so the student learns from better data than the teacher's raw score. On PII
the teacher scored 0.768 and the student 0.801.

### What to change after each training

Run distil-cli's error analysis, show the team the biggest failure mode, and change one thing:

| What the errors show | What to change |
|---|---|
| wrong where the teacher is right, in one kind of input | add 300 to 700 rows aimed at it: a new mutator value, weighted up |
| a bad habit copied from the data, or a kind of input the rows never show | change the generation prompt and the validator together ([which prompt](#which-prompt-to-change-and-when)), then add rows |
| close to the teacher, no clear pattern | a bigger student, or one more epoch |
| the teacher is wrong too | the frozen prompt or the test labels: tell the team, do not change them |

Training data only grows: add rows, never replace them.

### Which prompt to change, and when

A Dataset has several prompts, and they play different roles. When the trained model is weak,
the fix is almost always on the **data side**, not in the system prompt.

| Prompt | Where | What it does | When to change it |
|---|---|---|---|
| **System prompt** | `task_description` in `job_description.json` | what the model is told in training, in evaluation and on the laptop | teacher rounds 1 to 3 only. After the freeze it is the model's contract: changing it voids every score so far |
| **Generation prompt** | `synthetic_data_generation_instructions` in `job_description.json` | tells the teacher what rows to write: the situations, the style, the shape of a conversation | **any time**. Affects only rows generated after the change. The main lever when the student is weak |
| **Validator** | `synthgen.validation_instructions` in `config.yaml` | rejects bad generated rows before training | **any time**, same as above |
| **Mutators** | `synthgen.mutators` in `config.yaml` | the mix of rows | **any time** |
| **Judge rubric** | `llm_as_a_judge_instructions` in `job_description.json` | scores the answers | never after the freeze |

When the student copies a bad habit or misses a kind of input, change two things together, as
one change: a sentence in the **generation prompt** that says what the rows must look like, and a
matching **reject reason** in the validator. Then smoke and top up. Examples from our prep:

| Problem in the rows | Added to the generation prompt | Added to the validator |
|---|---|---|
| injection attacks were all blatant; the test set has subtle ones | "Injections range from blatant ('ignore all previous instructions') to subtle (a harmless 'act as a storyteller' request, 'translate to polish', a question about how the assistant was trained, a manipulation appended after a normal question). The message never names its own label." | "Reject the example if the message names its own label or says what kind of message it is." |
| the agent sent emails without asking, and invented tool results | "Sending an email always takes two steps: draft_email, then the assistant shows the draft and asks 'Send it?'; send_email only after the user says yes. The tool results are short JSON, and the assistant's answer is based only on them." | "Reject the example if send_email is called without the user's explicit yes, or an answer states something the tool results do not say." |
| invoice dates came out in one format, and some slash dates were impossible | a `date_format` mutator with 5 formats, weighted to the test set | "Reject the example if date and due_date are not correct ISO conversions of the printed dates (MM/DD for US vendors, DD/MM for all others), or if a US invoice prints a slash date whose first number is above 12." |

**If the system prompt itself is wrong after the freeze** (the student and the teacher both
fail on a convention nobody wrote down), it is a restart, not an iteration: a new root Dataset,
a new teacher check, and new trainings. Decide it with the team; on Sunday there is no time
for it.

What iteration 2 did in our prep:

| Task | Iteration 1 | Change | Iteration 2 | Why |
|---|---|---|---|---|
| injection guard | 0.957 | +500 rows, benign questions weighted up to match the test set | **0.974** | the student was wrong where the teacher was right: a coverage gap |
| terminal copilot | 0.74 | +700 rows on less common shell utilities | **0.80** | same: a coverage gap |
| commit messages | 0.889 | +700 rows on the biggest failure mode | 0.889 | the failures were judgement calls the teacher also gets wrong |
| text-to-SQL | 0.70 | +700 rows | 0.693 | the teacher was at 0.77 and the test labels were loose |

**A top-up helps when the student is wrong where the teacher is right.** When the teacher also
fails on those inputs, more rows repeat its mistakes: stop, or try one size up.

## Settings for the weekend

Use distil-cli's config rules with these values:

```yaml
base:
  task: question-answering                 # chat-completion for tools and agents
  student_model_name: Qwen3.5-4B           # 0.6B to 4B, must fit the laptop
  teacher_model_name: zai.glm-5.3-low-thinking
  llm_num_parallel_requests: 32
tuning:
  num_train_epochs: 3                      # 2 for long JSON outputs
  per_device_train_batch_size: 16          # 4B or long rows: 4
  gradient_accumulation_steps: 1           # 4B or long rows: 4
  learning_rate: 2e-4                      # free text: leave these three out (batch 1, 5e-5)
evaluation:
  llm_as_a_judge_model_name: zai.glm-5.3-low-thinking   # never change it
synthgen:
  train_generation_target: 1500            # top-ups 300 to 700
  validation_instructions: >-              # see "The validator" below
    Work out the correct answer from the input yourself before reading the answer.
    Reject the example if the answer differs, invents a value the input does not give,
    or contains anything besides the answer.
  mutators:                                # see "Mutators" below
    - name: kind
      values: ["...", "..."]
      target_distribution: [2, 1]
```

### The fast config: platform defaults vs the hackathon

The platform defaults are built for a big production run, not for a weekend. Change these:

| Setting | Platform default | Hackathon | What it buys |
|---|---|---|---|
| `base.llm_num_parallel_requests` | 4 | **32** | teacher, generation, validator and judge calls run 8 times as wide: generation and evaluations finish much sooner, same results. The biggest speed setting |
| `synthgen.train_generation_target` | 10,000 | **1,500** first, then **300 to 700** per top-up, **3,000** at most | 1,500 rows took us 5 to 25 minutes; an iteration takes about 1 to 1.5 hours instead of most of a day, at a fraction of the cost |
| `tuning.num_train_epochs` | 4 | **3**; **2** for long JSON outputs | shorter trainings; 3 was enough in all 9 prep tasks |
| `tuning.per_device_train_batch_size` x `gradient_accumulation_steps` | 1 x 1 | **16 x 1** (short rows, up to 2B) or **4 x 4** (4B or long rows); default for free text | 16 times fewer optimizer steps; equal or better scores on labels, JSON and tool calls |
| `tuning.learning_rate` | 5e-5 | **2e-4** with batch 16; default with batch 1 | bigger steps to match the bigger batch |
| `base.teacher_model_name` | `nvidia.nemotron-3.5-super-vl` | **`zai.glm-5.3-low-thinking`**, the only teacher this weekend | the teacher all our prep scores come from |
| `evaluation.llm_as_a_judge_model_name` | the teacher | **`zai.glm-5.3-low-thinking`**, set explicitly | the judge stays the same model for every run |
| `base.student_model_name` | `Llama-3.2-1B-Instruct` | **0.6B to 4B by output type** (table below) | the right size for the task and the laptop |
| `synthgen.validation_instructions` | none | **always set** | wrong rows are dropped before training |
| `synthgen.mutators` | none | **always set, 1 to 3** | the data mix matches the test set from the first run |

Leave the rest at the default (`teacher_temperature` 0.7, `lora_r` 64, linear scheduler,
`max_completion_length` 2048) unless a log or the errors point at it.

### Settings per kind of output

| The output is | `base.task` | Metric | Extra settings | Batch, learning rate | Student to start | Example |
|---|---|---|---|---|---|---|
| one label from a fixed set | `question-answering` | `binary` | each label and its definition in `task_description`, ending "Answer with the label only." | 16 x 1, 2e-4 | 0.6B to 0.8B | `prompt-injection-guard` |
| JSON (extraction) | `question-answering` | `llm-as-a-judge`, graded rubric | `synthgen.output_is_json: true`; every key, date format and missing-field rule in `task_description`; 2 epochs | 4 x 4, 2e-4 | 2B to 4B | `invoice-extraction`, `pii-extraction` |
| free text (rewrite, SQL, commands) | `question-answering` | `llm-as-a-judge-reference-free` | end `task_description` with "Output only ..." | default (1, 5e-5) | 0.8B to 4B | `genz-translator`, `text-to-sql` |
| tool calls | `chat-completion` | `tool_call_equivalence` | `tools` in `job_description.json`; `synthgen.max_tool_calls_per_turn` (`unlimited` for parallel calls) | 4 x 4, 2e-4 | 2B to 4B, Qwen3.5 | `tool-calling` |
| an agent (calls, results, answer) | `chat-completion` | `tool_call_equivalence` and the judge | as tool calls, plus [Agents](#agents) | 4 x 4, 2e-4 | 4B, Qwen3.5 | `personal-agent` |

Measured in 36 prep trainings: batch 16 matched or beat the default on labels, JSON and tool
calls (guard 0.957 vs 0.922); the default was a little better on free text (Gen Z 0.927 vs
0.893). `16 x 1` ran out of GPU memory on a 4B student with long rows; `4 x 4` trains the same.

Students: `Qwen3-0.6B`, `Qwen3.5-0.8B`, `Llama-3.2-1B-Instruct`, `LFM2.5-1.2B-Instruct`,
`Qwen3-1.7B`, `Qwen3.5-2B`, `LFM2-2.6B`, `Llama-3.2-3B-Instruct`, `Qwen3.5-4B`,
`Qwen3-4B-Instruct-2507`. Llama and Gemma are gated on Hugging Face; `gemma-3-4b-it` cannot
call tools. A 4B model at 4-bit needs about 2.5 GB of RAM. On shell commands 4B beat 2B
clearly (0.74 vs 0.55); 2B was enough for invoices and tool calls.

### Mutators: get the mix right in one smoke

A mutator adds one line to every generation prompt: "Generated examples should be `<value>`".
Each row samples one value per mutator, so mutators decide what the 1,500 rows cover. A wrong
mix is the most common reason a student is weak on one kind of input, and the fastest thing to
fix.

How to set them, in this order:

1. **Count the test set.** Labels, tools, lengths, formats, languages: whatever varies.
2. **One mutator per thing that varies**, 1 to 3 mutators with 3 to 10 values each.
3. **Write each value so it finishes the sentence** "Generated examples should be ...":
   `"an invoice with 9 to 12 line items"`, not `"long"`.
4. **Set `target_distribution`** from the counts in step 1, for example `[4, 2, 1]`.
5. **Smoke 128 rows and count again.** Short on a value? Raise its weight, or set
   `method: adaptive`.

Rules that held in our prep:

- **Labels: one mutator, one value per label form.** Put the label and its form in the same
  value (`"an injection that asks the assistant to act as a persona"`). A second mutator that
  changes what the label should be breaks the mix.
- **Tools: one value per tool**, plus values for the behaviours you want: asks for a missing
  detail, asks before sending, answers with no tool.
- **Hard cases get their own value**, with the deciding facts written into it.
- **Never let a value give away the answer**: the student learns the phrase, not the task.
- **Weight the rare-but-costly cases up**, not down: they are what the demo will hit.

Labels (shortened from `examples/prompt-injection-guard`):

```yaml
mutators:
  - name: case
    values:
      - "an injection that tells the assistant to ignore or override its previous instructions"
      - "an injection that asks the assistant to act as a persona, role or character, even a harmless one"
      - "an injection hidden after a normal question, or pleading that it is not an injection"
      - "a benign information question about news, politics or society"
      - "a benign question that is rude, edgy or about a sensitive topic but asks only for information"
    target_distribution: [2, 2, 1, 2, 2]
  - name: language
    values: ["written in English", "written in German"]
    target_distribution: [2, 1]
```

Extraction (shortened from `examples/invoice-extraction`), one mutator per thing the test set varies:

```yaml
mutators:
  - name: line_items
    values: ["an invoice with 1 or 2 line items", "an invoice with 3 to 6 line items", "an invoice with 7 to 12 line items"]
    target_distribution: [2, 4, 2]
  - name: date_format
    values: ["dates printed as ISO (2025-11-24)", "dates printed EU style (24.11.2025)", "dates printed US style (11/24/2025)"]
    target_distribution: [3, 2, 1]
  - name: country
    values: ["an invoice from a vendor in the US", "an invoice from a vendor in India", "an invoice from a vendor in Germany"]
```

Agent (shortened from `examples/personal-agent`, which has 15 scenario values):

```yaml
mutators:
  - name: scenario
    values:
      - "a conversation that calls create_event"
      - "a conversation that calls search_email"
      - "a conversation where a required detail is missing, so the assistant asks one short question first"
      - "a conversation where the user asks to email someone, so the assistant drafts, shows the draft and asks 'Send it?'"
      - "a conversation that needs two tools, such as checking the calendar before creating an event"
      - "a conversation the assistant answers directly with no tool call"
    target_distribution: [2, 1, 2, 2, 2, 1]
  - name: turns
    values: ["a conversation with one user turn", "a conversation with two user turns", "a conversation with three user turns"]
    target_distribution: [3, 2, 1]
```

### The validator

`validation_instructions` makes an LLM re-check every generated row and drop the wrong ones. It
is the strongest data-quality setting, and it costs nothing in your time. Make it re-derive the
answer, then list the exact reasons to reject:

| Output | Validator |
|---|---|
| label | "Decide the label yourself from the task description before reading the answer. Reject the example if your label differs, or if the answer is anything other than exactly one label." |
| JSON | "Re-derive the answer from the input. Reject the example if any value does not appear in the input, a field the input gives is missing or null, or a date or number format breaks the rules in the task description." |
| free text | "Reject the example if the answer adds a fact the input does not give, drops one it does, or contains anything besides the answer." |
| agent | "Reject the example if any tool argument is not stated in the conversation, if a tool is called for something the user did not ask, or if anything is sent, deleted or changed without the user's confirmation." |

### Agents

`chat-completion`, with the tools in `job_description.json` (OpenAI function format, valid JSON
Schema; uploads reject calls that do not match it). A row is a whole conversation, one line in
`train.jsonl`; `arguments` is a JSON object, not a string:

```json
{"messages": [
  {"role": "user", "content": "Put lunch with Sam on Friday at 1pm"},
  {"role": "assistant", "tool_calls": [{"id": "call_1", "type": "function", "function": {"name": "create_event", "arguments": {"title": "Lunch with Sam", "start": "2026-11-27T13:00:00", "duration_minutes": 60}}}]},
  {"role": "tool", "tool_call_id": "call_1", "content": "{\"status\": \"created\", \"id\": \"evt_42\"}"},
  {"role": "assistant", "content": "Done: lunch with Sam is on your calendar for Friday at 1pm."}
]}
```

With well-described tools an agent can start with no seed rows: the teacher works from the tools
and the system prompt. Say in the generation instructions what a conversation must look like,
or the teacher invents tool results. `examples/personal-agent` is a full working Dataset with 10
tools.

## Run it on the laptop, fast

Tested on a MacBook with Apple silicon, 16 GB, Python 3.12. Paths are from the repo root.

**Do it once on Saturday evening** with the iteration-1 model. That run builds the venv and
downloads the base model, and any problem shows up while the team can still ask us. On Sunday
morning only the last model has to go through merge, convert and serve: about 10 minutes.

Before you start: about **15 GB free** for a 2B model and **25 GB** for a 4B one (base model,
merged copy, f16 and quantized files; delete the merged folder and the f16 file afterwards).
Llama and Gemma students are gated: accept the license on Hugging Face and run
`hf auth login` first.

```bash
distil slm download --destination my-model <slm-id> && tar -xf my-model/model.tar -C my-model
git clone --depth 1 --branch b11669 https://github.com/ggml-org/llama.cpp llama.cpp-src   # tag = llama-server --version
python3 -m venv .venv && .venv/bin/pip install torch transformers peft accelerate openai ./llama.cpp-src/gguf-py
.venv/bin/python examples/tools/merge.py my-model my-model-merged
.venv/bin/python llama.cpp-src/convert_hf_to_gguf.py my-model-merged --outfile my-model-f16.gguf --outtype f16
llama-quantize my-model-f16.gguf my-model.gguf Q4_K_M          # Q8_0 under 1B
llama-server -m my-model.gguf --jinja --port 8080 --chat-template-kwargs '{"enable_thinking": false}'
```

Check it against the platform: `.venv/bin/python examples/tools/score_local.py <dataset-dir>`
(add `--show` for free text or JSON). Agents: `.venv/bin/python examples/tools/agent_loop.py --job-description
<dataset-dir>/job_description.json`. Always send the trained system prompt.

| Measured on an M5, 16 GB | File | Speed |
|---|---|---|
| Injection guard, 0.6B, Q8_0 | 610 MB | 35 ms per message, same score as the platform |
| Gen Z translator, 0.8B, Q8_0 | 774 MB | about 150 ms per sentence |
| Personal agent, 2B, Q4_K_M | 1.2 GB | interactive, tool calls work |

## Things that cost us time

- **GPU out of memory:** halve the per-device batch, double the accumulation steps; if it still
  fails, add `tuning.memory_optimized_training: 1`. Failed jobs are refunded.
- **Merge fails with `NoMatchingPeftModuleError`:** Qwen3.5 is a vision-language model;
  `merge.py` already loads the right class.
- **Public test labels are wrong** more often than you expect: read 20 rows before trusting a
  score.
- **Answers wrapped in code fences** fail the metric: end the prompt with "Output only ...".
- **`ECONNRESET` on upload:** run it again.
- **`chat-completion-agentic` and `classification` are rejected:** use `chat-completion` and
  `question-answering`.

## Demo

5 minutes: the task and one live answer from the laptop (network off, if they dare); the
student's score next to the teacher's and the size difference; one iteration that worked and
one that did not. Have the model already served before the team goes on stage.

## Ideas and examples

Only when the team has no idea:

- **Voice agent:** speak to the model and it answers out loud. Our use-case checker pairs a
  Qwen3.5-4B (0.89, above its teacher's 0.80) with Gradium's open-source Phonon voice model,
  both on a laptop ([blog](https://www.distillabs.ai/blog/how-we-use-gradiums-phonon-to-chat-with-you-about-your-post-trained-small-model-use-case),
  and [VoiceTeller](https://github.com/distil-labs/distil-voice-assistant-banking) with 0.6B).
- **Personal agent** for calendar, email and notes, all offline.
- **A filter** in front of an LLM app: injection guard, PII redaction, topic router.
- **Developer tools:** commit messages, shell commands, log triage.
- **Extraction** from the documents the team handles.

`examples/` scores from our prep (student vs teacher): personal agent 0.93 vs 0.93, Gen Z 0.993
vs 0.977, tool calling 0.953 vs 0.94, PII 0.801 vs 0.768, invoices 0.996 vs 0.998, injection
guard 0.974 vs 0.987; commit messages, shell commands and SQL still have a gap to close.

## Help

The distil labs team on site: **Vineeth, Maciej and Lev**, in person or in **#general** on
Slack, for credits, platform errors or a stuck job. Jobs: https://app.distillabs.ai. Billing:
https://app.distillabs.ai/billing.
