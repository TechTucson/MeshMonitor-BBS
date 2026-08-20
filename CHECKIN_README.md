# Mesh Check-in Bot

`checkin.py` is a Meshtastic DM command handler for simple node check-ins. It follows the same command style as the BBS and mail scripts: send a DM that starts with `checkin`, and the script replies privately.

## Trigger setup

Create a trigger that invokes `checkin.py` when a DM starts with:

```text
checkin
```

Pass the sender node id with the same flag style used by the mail bot:

```text
--nid {NODE_ID}
```

If `--nid` is not provided, the script falls back to `FROM_NODE`.

## Commands

- `checkin [message]`  
  Record a check-in for your node id. If no message is supplied, the message is saved as `OK`.

- `checkin add [message]`  
  Explicit form of `checkin [message]`.

- `checkin last [count]`  
  Show the latest check-ins across all nodes. The default count is 5 and the maximum is 20.

- `checkin user <!node_id> [count]`  
  Show check-ins for a specific node id. Node ids may be entered with or without the leading `!`.

- `checkin mine [count]`  
  Show check-ins for your own node id.

- `checkin help`  
  Show command help.

- `checkin more`  
  Continue paginated output when a response exceeds message size limits.

## Examples

```text
checkin at trailhead
checkin add battery 87% near repeater
checkin last 10
checkin user !abcd1234 5
checkin mine
```

## Storage

Files are stored under `/data/bbs`:

- `checkins.json` — check-in records keyed by numeric id
- `checkin_pending.json` — per-user pagination state for `checkin more`

Each check-in stores the sender `node_id`, a UTC timestamp, and the check-in message.
