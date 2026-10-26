"""Convert a chapter to HTML for pasting into the Vocus editor.

- Title (H1) and the draft note are dropped: the title goes in Vocus's title box.
- Images point at the public GitHub copy; Vocus re-uploads them on paste.
- The italic caption line under an image is dropped: Vocus shows the alt text as caption.

Usage: python scripts/md_to_vocus.py docs/blog/01-two-mics.md out/ch1_vocus.json
Needs `markdown` (dev only: pip install markdown). Push the images to GitHub first.
"""
import json
import re
import sys
import pathlib

import markdown

RAW = "https://raw.githubusercontent.com/HsinNan123/acoustic-camera/main/docs/blog/"

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
lines = src.splitlines()
title = lines[0].lstrip("# ").strip()
body = lines[1:]
# Drop the draft note: the first block of "> " lines.
i = 0
while i < len(body) and not body[i].startswith(">"):
    i += 1
j = i
while j < len(body) and body[j].startswith(">"):
    j += 1
body = body[:i] + body[j:]
# Drop italic caption lines right after an image.
out = []
for k, line in enumerate(body):
    if line.startswith("*") and line.endswith("*") and not line.startswith("**"):
        prev = [l for l in out if l.strip()][-1] if any(l.strip() for l in out) else ""
        if prev.startswith("!["):
            continue
    out.append(line)
md = "\n".join(out)
md = re.sub(r"\]\(img/", "](" + RAW + "img/", md)
md = re.sub(r"(?<![(\"])(https://github\.com/[^\s）)]+)", r"[\1](\1)", md)

html = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists"])
html = re.sub(r"(?<=[A-Za-z0-9.,;:])\n\s*(?=[A-Za-z0-9<])", " ", html)  # English keeps its space
html = re.sub(r"\n\s*", "", html)  # line breaks inside Chinese text would become spaces
pathlib.Path(sys.argv[2]).write_text(json.dumps({"title": title, "html": html}, ensure_ascii=False),
                                     encoding="utf-8")
print(title)
print(len(html), "chars;", html.count("<img"), "images;", html.count("<table"), "tables;",
      html.count("<pre"), "code blocks;", html.count("<blockquote"), "quotes")
