#!/usr/bin/env python3
# mm_meta:
#   name: Mesh Radio Reference Bot
#   emoji: 📻

import json
import os
import pathlib
import sys

DATA = "/data/bbs"
pathlib.Path(DATA).mkdir(parents=True, exist_ok=True)

CUSTOM_DB = f"{DATA}/radio_custom.json"
PENDING_DB = f"{DATA}/radio_pending.json"

MAX_LEN = 180
MORE_PROMPT = "\n\n(Type: radio more)"
OVERRIDE_PASSWORD = "meshadmin"

RADIO_REFERENCE = {
    "frs": [
        ("FRS 01", "462.5625 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 02", "462.5875 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 03", "462.6125 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 04", "462.6375 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 05", "462.6625 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 06", "462.6875 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 07", "462.7125 MHz", "FM", "Shared FRS/GMRS simplex"),
        ("FRS 08", "467.5625 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 09", "467.5875 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 10", "467.6125 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 11", "467.6375 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 12", "467.6625 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 13", "467.6875 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 14", "467.7125 MHz", "FM", "FRS low-power interstitial"),
        ("FRS 15", "462.5500 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 16", "462.5750 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 17", "462.6000 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 18", "462.6250 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 19", "462.6500 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 20", "462.6750 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 21", "462.7000 MHz", "FM", "Shared with GMRS main/simplex"),
        ("FRS 22", "462.7250 MHz", "FM", "Shared with GMRS main/simplex"),
    ],
    "gmrs": [
        ("GMRS 15", "462.5500 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 16", "462.5750 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 17", "462.6000 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 18", "462.6250 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 19", "462.6500 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 20", "462.6750 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 21", "462.7000 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 22", "462.7250 MHz", "FM", "Main/simplex or repeater output"),
        ("GMRS 15R", "467.5500 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 16R", "467.5750 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 17R", "467.6000 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 18R", "467.6250 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 19R", "467.6500 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 20R", "467.6750 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 21R", "467.7000 MHz", "FM", "Repeater input (+5 MHz from output)"),
        ("GMRS 22R", "467.7250 MHz", "FM", "Repeater input (+5 MHz from output)"),
    ],
    "vhf": [
        ("2m FM simplex call", "146.520 MHz", "FM", "US national simplex calling"),
        ("2m SSB call", "144.200 MHz", "USB", "Weak-signal calling"),
        ("6m SSB call", "50.125 MHz", "USB", "Weak-signal calling"),
        ("6m FM simplex call", "52.525 MHz", "FM", "Common FM calling"),
        ("1.25m FM simplex", "223.500 MHz", "FM", "Common simplex/calling"),
    ],
    "uhf": [
        ("70cm FM simplex call", "446.000 MHz", "FM", "US national simplex calling"),
        ("70cm SSB call", "432.100 MHz", "USB", "Weak-signal calling"),
        ("33cm FM simplex", "927.500 MHz", "FM", "Common simplex/calling"),
        ("23cm SSB call", "1296.100 MHz", "USB", "Weak-signal calling"),
        ("23cm FM simplex", "1294.500 MHz", "FM", "Common simplex/calling"),
    ],
    "hf": [
        ("160m FT8", "1.840 MHz", "USB", "Common WSJT-X working frequency"),
        ("80m FT8", "3.573 MHz", "USB", "Common WSJT-X working frequency"),
        ("40m FT8", "7.074 MHz", "USB", "Common WSJT-X working frequency"),
        ("30m FT8", "10.136 MHz", "USB", "Common WSJT-X working frequency"),
        ("20m FT8", "14.074 MHz", "USB", "Common WSJT-X working frequency"),
        ("17m FT8", "18.100 MHz", "USB", "Common WSJT-X working frequency"),
        ("15m FT8", "21.074 MHz", "USB", "Common WSJT-X working frequency"),
        ("12m FT8", "24.915 MHz", "USB", "Common WSJT-X working frequency"),
        ("10m FT8", "28.074 MHz", "USB", "Common WSJT-X working frequency"),
    ],
    "digital": [
        ("160m JS8", "1.842 MHz", "USB", "Suggested JS8Call area"),
        ("80m JS8", "3.578 MHz", "USB", "Suggested JS8Call area"),
        ("40m JS8", "7.078 MHz", "USB", "Suggested JS8Call area"),
        ("30m JS8", "10.130 MHz", "USB", "Suggested JS8Call area"),
        ("20m JS8", "14.078 MHz", "USB", "Suggested JS8Call area"),
        ("17m JS8", "18.104 MHz", "USB", "Suggested JS8Call area"),
        ("15m JS8", "21.078 MHz", "USB", "Suggested JS8Call area"),
        ("12m JS8", "24.922 MHz", "USB", "Suggested JS8Call area"),
        ("10m JS8", "28.078 MHz", "USB", "Suggested JS8Call area"),
        ("160m WSPR", "1.8366 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("80m WSPR", "3.5686 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("40m WSPR", "7.0386 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("30m WSPR", "10.1387 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("20m WSPR", "14.0956 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("17m WSPR", "18.1046 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("15m WSPR", "21.0946 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("12m WSPR", "24.9246 MHz", "USB", "Common WSJT-X WSPR frequency"),
        ("10m WSPR", "28.1246 MHz", "USB", "Common WSJT-X WSPR frequency"),
    ],
}
ALIASES = {"frs/gmrs": "frs", "ham": "hf", "ft8": "hf", "js8": "digital", "js8call": "digital", "wspr": "digital", "customs": "custom"}


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


def load(path):
    if not os.path.exists(path):
        return {}
    with open(path) as handle:
        return json.load(handle)


def save(path, data):
    with open(path, "w") as handle:
        json.dump(data, handle)


def header(title):
    return f"📻 RADIO REF — {title}\n"


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
        + "radio cats\n"
        + "radio list <cat>\n"
        + "radio find <text>\n"
        + "radio custom\n"
        + "radio add <name> | <freq> | <mode> | <notes>\n"
        + "radio del <id>\n"
        + "radio more"
    )


def entry_line(entry_id, name, freq, mode, notes, custom=False):
    prefix = f"#{entry_id} " if custom else ""
    return f"{prefix}{name}: {freq} {mode} - {notes}"


def custom_items():
    return sorted(custom.items(), key=lambda item: int(item[0]))


def category_items(category):
    if category == "custom":
        return [
            (cid, item.get("name", "?"), item.get("freq", "?"), item.get("mode", "?"), item.get("notes", ""), True)
            for cid, item in custom_items()
        ]
    return [(None, *item, False) for item in RADIO_REFERENCE.get(category, [])]


def resolve_category(raw):
    value = (raw or "").lower().strip()
    return ALIASES.get(value, value)


def list_entries(title, entries, empty_text):
    if not entries:
        dm_chunked(sender, header(title) + empty_text)
    lines = [entry_line(*entry) for entry in entries]
    dm_chunked(sender, header(title) + "\n".join(lines))


def next_custom_id():
    return str(max([int(k) for k in custom.keys()], default=0) + 1)


def is_owner_or_admin(item, supplied_pw):
    return item.get("owner") == sender or (OVERRIDE_PASSWORD and supplied_pw == OVERRIDE_PASSWORD)


sender = get_sender_node_id()
message = os.getenv("MESSAGE", "").strip()
parts = message.split()
custom = load(CUSTOM_DB)
pending = load(PENDING_DB)

if not parts:
    dm_chunked(sender, help_text())

cmd = parts[0].lower()
if not (cmd == "radio" and len(parts) > 1 and parts[1].lower() == "more"):
    if sender in pending and pending[sender]:
        pending[sender] = []
        save(PENDING_DB, pending)

if cmd != "radio":
    dm_chunked(sender, header("Unknown Command") + "Use: radio help")

if len(parts) == 1:
    dm_chunked(sender, help_text())

action = parts[1].lower()

if action == "help":
    dm_chunked(sender, help_text())

elif action == "more":
    if sender not in pending or not pending[sender]:
        dm_chunked(sender, header("Info") + "No more radio reference pages.")
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

elif action in ("cats", "categories"):
    cats = ", ".join(list(RADIO_REFERENCE.keys()) + ["custom"])
    dm_chunked(sender, header("Categories") + cats + "\nUse: radio list <cat>")

elif action in ("list", "show"):
    if len(parts) < 3:
        dm_chunked(sender, header("List") + "Usage:\nradio list <cat>\nTry: radio cats")
    category = resolve_category(parts[2])
    if category not in RADIO_REFERENCE and category != "custom":
        dm_chunked(sender, header("List") + "Unknown category.\nTry: radio cats")
    list_entries(category.upper(), category_items(category), "No custom frequencies saved yet.")

elif action in ("custom", "mine"):
    list_entries("Custom", category_items("custom"), "No custom frequencies saved yet.\nUse: radio add <name> | <freq> | <mode> | <notes>")

elif action == "find":
    if len(parts) < 3:
        dm_chunked(sender, header("Find") + "Usage:\nradio find <text>")
    needle = " ".join(parts[2:]).lower()
    matches = []
    for category in RADIO_REFERENCE:
        for entry in category_items(category):
            haystack = " ".join(str(value) for value in entry[1:5]).lower()
            if needle in haystack or needle in category:
                entry_id, name, freq, mode, notes, is_custom = entry
                matches.append((entry_id, f"{category}: {name}", freq, mode, notes, is_custom))
    for entry in category_items("custom"):
        haystack = " ".join(str(value) for value in entry[1:5]).lower()
        if needle in haystack or needle == "custom":
            matches.append(entry)
    list_entries("Find", matches[:20], "No matches.")

elif action == "add":
    payload = " ".join(parts[2:]).strip()
    fields = [field.strip() for field in payload.split("|")]
    if len(fields) != 4 or not all(fields[:3]):
        dm_chunked(sender, header("Add") + "Usage:\nradio add <name> | <freq> | <mode> | <notes>")
    cid = next_custom_id()
    custom[cid] = {
        "name": fields[0],
        "freq": fields[1],
        "mode": fields[2],
        "notes": fields[3],
        "owner": sender,
    }
    save(CUSTOM_DB, custom)
    dm_chunked(sender, header("Added") + entry_line(cid, fields[0], fields[1], fields[2], fields[3], True))

elif action in ("del", "delete"):
    if len(parts) < 3:
        dm_chunked(sender, header("Delete") + "Usage:\nradio del <id> [admin_pw]")
    cid = parts[2]
    if cid not in custom:
        dm_chunked(sender, header("Delete") + "Custom entry not found.")
    supplied_pw = parts[3] if len(parts) > 3 else ""
    if not is_owner_or_admin(custom[cid], supplied_pw):
        dm_chunked(sender, header("Delete") + "Only the entry owner can delete it.")
    del custom[cid]
    save(CUSTOM_DB, custom)
    dm_chunked(sender, header("Delete") + f"Deleted custom entry #{cid}.")

else:
    dm_chunked(sender, header("Unknown Command") + "Use: radio help")
