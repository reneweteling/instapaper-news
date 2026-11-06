#!/usr/bin/env python3
"""Regenerate index.html from all YYYY-MM-DD.html digest pages (newest first).

Usage: python3 build_index.py   (run from the repo root)
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.html$")
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)

items = []
for page in sorted(ROOT.iterdir(), reverse=True):
    if not DATE_RE.match(page.name):
        continue
    m = TITLE_RE.search(page.read_text(encoding="utf-8"))
    title = html.unescape(m.group(1).strip()) if m else page.stem
    items.append((page.name, title))

lis = "\n".join(
    f'<li><a href="{name}">{html.escape(title)}</a></li>' for name, title in items
)

ROOT.joinpath("index.html").write_text(
    f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI-digest archief</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>AI-digest archief</h1>
<ul>
{lis}
</ul>
</body>
</html>
""",
    encoding="utf-8",
)
print(f"index.html: {len(items)} digests")
