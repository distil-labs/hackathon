"""A minimal personal-agent loop: your trained model (served locally) + local tools backed by a JSON file.

1. Serve the model:  llama-server -m agent.gguf --jinja --port 8080 --chat-template-kwargs '{"enable_thinking": false}'
2. Chat:             python agent_loop.py --job-description job_description.json
   or one-shot:      python agent_loop.py --job-description job_description.json --say "Put lunch with Sam on Friday at 1pm"

The system prompt and the tools come from the Dataset's job_description.json, exactly as the model was trained.
Replace the functions in TOOLS with real integrations (your calendar, mail client, notes) when you are ready.
"""
import argparse
import json
import uuid
from pathlib import Path

from openai import OpenAI

STATE = Path("agent_state.json")


def load():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"events": [{"id": "evt_1", "title": "Team standup", "start": "Monday 09:30", "duration_minutes": 15}],
            "emails": [{"id": "em_1", "sender": "Dr. Smith", "subject": "Appointment confirmation",
                        "snippet": "Your appointment is on Thursday at 10:00."}],
            "drafts": {}, "tasks": [], "notes": [{"title": "Wifi", "text": "Guest wifi password is in the drawer."}],
            "reminders": []}


def save(s):
    STATE.write_text(json.dumps(s, indent=2))


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def list_events(s, start, end):
    return {"events": s["events"]}


def create_event(s, title, start, duration_minutes=60, attendees=None, location=None):
    e = {"id": new_id("evt"), "title": title, "start": start, "duration_minutes": duration_minutes,
         "attendees": attendees or [], "location": location}
    s["events"].append(e)
    return {"status": "created", "id": e["id"]}


def search_email(s, query, sender=None, unread_only=False):
    q = query.lower()
    hits = [m for m in s["emails"] if q in (m["subject"] + m["snippet"]).lower()
            and (not sender or sender.lower() in m["sender"].lower())]
    return {"emails": hits}


def draft_email(s, to, subject, body):
    d = new_id("draft")
    s["drafts"][d] = {"to": to, "subject": subject, "body": body}
    return {"draft_id": d}


def send_email(s, draft_id):
    if draft_id not in s["drafts"]:
        return {"error": f"no draft {draft_id}"}
    print(f"   (pretend-sending {s['drafts'][draft_id]})")
    return {"status": "sent"}


def add_task(s, title, due=None):
    t = {"id": new_id("task"), "title": title, "due": due, "status": "open"}
    s["tasks"].append(t)
    return {"status": "added", "id": t["id"]}


def list_tasks(s, status="open"):
    return {"tasks": [t for t in s["tasks"] if status == "all" or t["status"] == status]}


def search_notes(s, query):
    return {"notes": [n for n in s["notes"] if query.lower() in (n["title"] + n["text"]).lower()]}


def set_reminder(s, text, at):
    s["reminders"].append({"text": text, "at": at})
    return {"status": "set"}


def get_weather(s, location, day="today"):
    return {"location": location, "day": day, "forecast": "14C, light rain"}  # plug in a real weather API here


TOOLS = {f.__name__: f for f in (list_events, create_event, search_email, draft_email, send_email, add_task,
                                 list_tasks, search_notes, set_reminder, get_weather)}


def run_turn(client, messages, tools, state):
    """Call the model until it answers in text; run every tool call it makes in between."""
    for _ in range(5):
        msg = client.chat.completions.create(model="local", messages=messages, tools=tools,
                                             temperature=0).choices[0].message
        messages.append(msg.model_dump(exclude_none=True))
        if not msg.tool_calls:
            return msg.content
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments or "{}")
            print(f"   -> {call.function.name}({args})")
            fn = TOOLS.get(call.function.name)
            result = fn(state, **args) if fn else {"error": f"unknown tool {call.function.name}"}
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
        save(state)
    return "(stopped after 5 tool rounds)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job-description", required=True)
    ap.add_argument("--base-url", default="http://127.0.0.1:8080/v1")
    ap.add_argument("--say", action="append", help="send these messages instead of chatting")
    a = ap.parse_args()
    jd = json.load(open(a.job_description))
    client = OpenAI(base_url=a.base_url, api_key="EMPTY")
    messages = [{"role": "system", "content": jd["task_description"]}]
    state = load()
    for text in a.say or iter(lambda: input("you> "), "quit"):
        if a.say:
            print(f"you> {text}")
        messages.append({"role": "user", "content": text})
        print(f"agent> {run_turn(client, messages, jd['tools'], state)}")


if __name__ == "__main__":
    main()
