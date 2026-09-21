#!/usr/bin/env python3
"""
Assemble a flat, self-contained preview bundle from the repo pages.

The repo pages are normal documents with an external stylesheet, which is what
GitHub Pages wants. The preview host wants the CSS inlined and everything on one
flat level, so this rewrites paths rather than keeping a second copy of the HTML
by hand.

Output: build/artifact/
  index.html      the library, stripped of its document skeleton (main page)
  stocks.html     the tracker, full document
  data/tracker.json
"""

import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "build", "artifact")

CSS = open(os.path.join(ROOT, "assets", "style.css"), encoding="utf-8").read()


def flatten(html):
    """Inline the stylesheet and pull every path up to one flat level."""
    html = html.replace(
        '<link rel="stylesheet" href="../assets/style.css">',
        "<style>\n" + CSS + "\n</style>",
    )
    html = html.replace('href="../index.html"', 'href="index.html"')
    html = html.replace('href="guides/index.html"', 'href="index.html"')
    html = html.replace('href="guides/stocks.html"', 'href="stocks.html"')
    html = html.replace('"../data/tracker.json"', '"data/tracker.json"')
    return html


def strip_skeleton(html):
    """Keep <title> and <style> and the body contents; drop the wrapper tags."""
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    styles = re.findall(r"<style>.*?</style>", html, re.S)
    fonts = re.findall(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>', html)
    body = re.search(r"<body>(.*)</body>", html, re.S)
    parts = []
    if title:
        parts.append("<title>%s</title>" % title.group(1))
    parts.extend(fonts)
    parts.extend(styles)
    parts.append(body.group(1).strip() if body else html)
    return "\n".join(parts)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)

    library = flatten(open(os.path.join(ROOT, "guides", "index.html"), encoding="utf-8").read())
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(strip_skeleton(library))

    tracker = flatten(open(os.path.join(ROOT, "guides", "stocks.html"), encoding="utf-8").read())
    open(os.path.join(OUT, "stocks.html"), "w", encoding="utf-8").write(tracker)

    shutil.copy(os.path.join(ROOT, "data", "tracker.json"), os.path.join(OUT, "data", "tracker.json"))

    for name in ("index.html", "stocks.html"):
        size = os.path.getsize(os.path.join(OUT, name))
        print("%-14s %6.1f KB" % (name, size / 1024))


if __name__ == "__main__":
    main()
