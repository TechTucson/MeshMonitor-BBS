# Mesh Radio Reference Bot

`radio.py` is an offline radio-frequency reference for Meshtastic DM use. It follows the same private-response style as the BBS, mail, and check-in scripts.

> Always verify current rules, license requirements, and band plans before transmitting. This script is a field reference, not legal authority.

## Trigger setup

Create a trigger that invokes `radio.py` when a DM starts with:

```text
radio
```

Pass the sender node id with the same flag style used by the mail and check-in bots:

```text
--nid {NODE_ID}
```

If `--nid` is not provided, the script falls back to `FROM_NODE`.

## Included reference categories

- `frs` — FRS channels 1-22.
- `gmrs` — GMRS main/simplex and repeater input channels.
- `vhf` — common VHF amateur calling/simplex references.
- `uhf` — common UHF amateur calling/simplex references.
- `hf` — common HF FT8 working frequencies.
- `digital` — common JS8Call and WSPR references.
- `custom` — user-added entries stored locally.

The built-in FRS/GMRS entries are based on the FCC 462/467 MHz channel structure and 47 CFR Part 95 references. VHF/UHF entries follow common US amateur band-plan calling/simplex references, and the digital entries are common WSJT-X/JS8Call working-frequency references.

## Commands

- `radio cats`  
  Show available categories.

- `radio list <cat>`  
  List a category such as `frs`, `gmrs`, `vhf`, `uhf`, `hf`, `digital`, or `custom`.

- `radio find <text>`  
  Search built-in and custom entries by name, frequency, mode, note text, or category.

- `radio custom`  
  Show custom entries.

- `radio add <name> | <freq> | <mode> | <notes>`  
  Add a custom local reference entry owned by your node id.

- `radio del <id> [admin_pw]`  
  Delete one of your custom entries. The configured admin password can delete any custom entry.

- `radio help`  
  Show command help.

- `radio more`  
  Continue paginated output when a response exceeds message size limits.

## Examples

```text
radio cats
radio list frs
radio list digital
radio find 146.520
radio add Local repeater | 146.940 MHz -0.6 | FM | PL 100.0, town repeater
radio custom
radio del 1
```

## Storage

Files are stored under `/data/bbs`:

- `radio_custom.json` — custom radio-reference entries keyed by numeric id
- `radio_pending.json` — per-user pagination state for `radio more`

Custom entries store `name`, `freq`, `mode`, `notes`, and the owner `node_id`.

## Sources for future updates

Useful source material for maintaining the built-in table:

- FCC Family Radio Service overview: https://www.fcc.gov/wireless/bureau-divisions/mobility-division/family-radio-service-frs
- 47 CFR Part 95 GMRS rules: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-E
- ARRL band plans: https://www.arrl.org/band-plan-1
- WSJT-X user guide: https://wsjt.sourceforge.io/wsjtx-main_en.html
- JS8Call user guide: https://js8call.com/JS8Call-improved/d6/d14/md_docs_2user__guide_2JS8Call__User__Guide.html
