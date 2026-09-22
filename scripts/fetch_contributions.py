#!/usr/bin/env python3
"""Fetches the public contribution calendar for a user without a token, writes data/contributions.json.
Parses github.com/users/<user>/contributions, which GitHub serves as plain HTML.
Run from repo root: python3 scripts/fetch_contributions.py MiguelPimienta19"""
import json, os, re, sys, urllib.request
from datetime import date

user = sys.argv[1] if len(sys.argv) > 1 else "MiguelPimienta19"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url = f"https://github.com/users/{user}/contributions"
html = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "profile-readme-tide/1.0"}), timeout=30).read().decode()

# day cells carry data-date and an id; the count lives in a <tool-tip for="<id>"> element
cells = {m.group("id"): m.group("date") for m in re.finditer(r'<td[^>]*data-date="(?P<date>\d{4}-\d{2}-\d{2})"[^>]*id="(?P<id>[^"]+)"', html)}
if not cells:  # attribute order varies; try the other way round
    cells = {m.group("id"): m.group("date") for m in re.finditer(r'<td[^>]*id="(?P<id>[^"]+)"[^>]*data-date="(?P<date>\d{4}-\d{2}-\d{2})"', html)}
tips = {m.group("id"): m.group("txt") for m in re.finditer(r'<tool-tip[^>]*for="(?P<id>[^"]+)"[^>]*>(?P<txt>[^<]*)</tool-tip>', html)}
days = []
for cid, d in cells.items():
    txt = tips.get(cid, "")
    m = re.match(r"\s*(\d+|No)\s+contribution", txt)
    n = 0 if not m or m.group(1) == "No" else int(m.group(1))
    days.append({"date": d, "count": n})
days.sort(key=lambda x: x["date"])
if len(days) < 300: sys.exit(f"parsed only {len(days)} days from {url}; markup probably changed")
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
json.dump({"user": user, "fetched": date.today().isoformat(), "days": days}, open(os.path.join(ROOT, "data", "contributions.json"), "w"), indent=0)
print(f"wrote data/contributions.json: {len(days)} days, {sum(d['count'] for d in days)} contributions")
