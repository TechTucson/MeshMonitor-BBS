#!/usr/bin/env python3
# mm_meta:
#   name: Mesh Check-in Bot
#   emoji: ✅

import json
import os
import pathlib
import sys
from datetime import datetime, timezone

DATA = "/data/bbs"
pathlib.Path(DATA).mkdir(parents=True, exist_ok=True)

CHECKINS_DB = f"{DATA}/checkins.json"
PENDING_DB = f"{DATA}/checkin_pending.json"

MAX_LEN = 180  # Keep payload under LoRa-friendly size target
MORE_PROMPT = "\n\n(Type: checkin more)"
DEFAULT_LIST_COUNT = 5
MAX_LIST_COUNT = 20


def normalize_node_id(node_id):
    value = (node_id or "").strip()
    if not value:
        return value
    return value if value.startswith("!") else f"!{value}"


def get_sender_node_id():
    argv = sys.argv[1:]
    if "--nid" in argv:
        idx = argv.index("--nid")
        if idx + 1 < len(argv):
            return normalize_node_id(argv[idx + 1])
    return normalize_node_id(os.getenv("FROM_NODE", "unknown"))


def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as handle:
        return json.load(handle)


def save(path, data):
    with open(path, "w") as handle:
        json.dump(data, handle)


def header(title):
    return f"✅ MESH CHECK-IN — {title}\n"


def send_private(text):
    print(json.dumps({"response": text, "private": True}))
    exit()


def chunk_text(text, limit):
    chunks = []
    current = ""

    for part in text.split("\n"):
        piece = part if not current else f"\n{part}"

        if len(piece) <= limit and len(current) + len(piece) <= limit:
            current += piece
            continue

        if current:
            chunks.append(current)
            current = ""

        while len(part) > limit:
            chunks.append(part[:limit])
            part = part[limit:]

        current = part

    if current:
        chunks.append(current)

    return chunks or [""]


def dm_chunked(sender, text):
    first_limit = MAX_LEN - len(MORE_PROMPT)
    chunks = chunk_text(text, first_limit)

    pending[sender] = chunks[1:]
    save(PENDING_DB, pending)

    first = chunks[0]
    if pending[sender]:
        first += MORE_PROMPT

    send_private(first)


def help_text():
    return (
        header("Help")
        + "checkin [message]\n"
        + "checkin add [message]\n"
        + "checkin last [count]\n"
        + "checkin user <!node_id> [count]\n"
        + "checkin mine [count]\n"
        + "checkin more"
    )


def parse_count(value, default=DEFAULT_LIST_COUNT):
    if not value:
        return default
    try:
        count = int(value)
    except ValueError:
        return default
    return max(1, min(count, MAX_LIST_COUNT))


def next_checkin_id(checkins):
    return str(max([int(k) for k in checkins.keys()], default=0) + 1)


def format_checkin(checkin_id, item):
    node_id = item.get("node_id", "?")
    at = item.get("at", "?")
    message = item.get("message", "OK")
    return f"#{checkin_id} {node_id} @ {at}\n{message}"


def list_checkins(items, title, empty_text):
    if not items:
        dm_chunked(sender, header(title) + empty_text)

    lines = [format_checkin(checkin_id, item) for checkin_id, item in items]
    dm_chunked(sender, header(title) + "\n---\n".join(lines))


sender = get_sender_node_id()
message = os.getenv("MESSAGE", "").strip()
parts = message.split()

checkins = load(CHECKINS_DB, {})
pending = load(PENDING_DB, {})

if not parts:
    dm_chunked(sender, help_text())

cmd = parts[0].lower()

# Clear stale pagination state unless user asked for more.
if not (cmd == "checkin" and len(parts) > 1 and parts[1].lower() == "more"):
    if sender in pending and pending[sender]:
        pending[sender] = []
        save(PENDING_DB, pending)

if cmd != "checkin":
    dm_chunked(sender, header("Unknown Command") + "Use: checkin help")

if len(parts) == 1:
    action = "add"
    action_args = []
else:
    maybe_action = parts[1].lower()
    if maybe_action in ("help", "add", "now", "in", "last", "recent", "user", "node", "mine", "me", "more"):
        action = maybe_action
        action_args = parts[2:]
    else:
        action = "add"
        action_args = parts[1:]

if action == "help":
    dm_chunked(sender, help_text())

elif action == "more":
    if sender not in pending or not pending[sender]:
        dm_chunked(sender, header("Info") + "No more check-ins.")

    next_limit = MAX_LEN - len(MORE_PROMPT)
    next_page = pending[sender].pop(0)
    save(PENDING_DB, pending)

    if len(next_page) > next_limit:
        rest = chunk_text(next_page, next_limit)
        next_page = rest[0]
        pending[sender] = rest[1:] + pending[sender]
        save(PENDING_DB, pending)

    if pending[sender]:
        next_page += MORE_PROMPT

    send_private(next_page)

elif action in ("add", "now", "in"):
    text = " ".join(action_args).strip() or "OK"
    checkin_id = next_checkin_id(checkins)
    at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    checkins[checkin_id] = {"node_id": sender, "at": at, "message": text}
    save(CHECKINS_DB, checkins)
    dm_chunked(sender, header("Checked In") + f"Saved #{checkin_id} for {sender}.\n{at}\n{text}")

elif action in ("last", "recent"):
    count = parse_count(action_args[0] if action_args else None)
    items = sorted(checkins.items(), key=lambda item: int(item[0]), reverse=True)[:count]
    list_checkins(items, f"Last {count}", "No check-ins yet.\nUse: checkin [message]")

elif action in ("mine", "me"):
    count = parse_count(action_args[0] if action_args else None)
    items = [item for item in checkins.items() if item[1].get("node_id") == sender]
    items = sorted(items, key=lambda item: int(item[0]), reverse=True)[:count]
    list_checkins(items, "My Check-ins", "No check-ins for your node id yet.\nUse: checkin [message]")

elif action in ("user", "node"):
    if not action_args:
        dm_chunked(sender, header("User") + "Usage:\ncheckin user <!node_id> [count]")

    node_id = normalize_node_id(action_args[0])
    count = parse_count(action_args[1] if len(action_args) > 1 else None)
    items = [item for item in checkins.items() if item[1].get("node_id") == node_id]
    items = sorted(items, key=lambda item: int(item[0]), reverse=True)[:count]
    list_checkins(items, f"{node_id} Check-ins", f"No check-ins for {node_id} yet.")

else:
    dm_chunked(sender, header("Unknown Command") + "Use: checkin help")
