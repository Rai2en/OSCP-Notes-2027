"""Check local inline Markdown file links and their GitHub-style fragments."""
from pathlib import Path
import html
import re
import unicodedata
from urllib.parse import unquote, urlsplit

LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)")


def prose_lines(text, keep_inline_code=False):
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield line if keep_inline_code else re.sub(r"`+[^`]*`+", "", line)


def document_anchors(text):
    """Resolve ordinary ATX headings and explicit anchors used in this repo."""
    anchors = set()
    seen = {}
    for line in prose_lines(text, keep_inline_code=True):
        anchors.update(re.findall(r"<a\s+(?:id|name)=[\"']([^\"']+)[\"']", line))
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        if not heading:
            continue
        title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading.group(1))
        title = html.unescape(re.sub(r"<[^>]+>", "", title)).lower()
        slug = "".join(c for c in title if c in " -_" or unicodedata.category(c)[0] in "LMN")
        slug = slug.replace(" ", "-")
        candidate = slug
        number = 0
        while candidate in seen:
            number += 1
            candidate = f"{slug}-{number}"
        seen[candidate] = True
        anchors.add(candidate)
    return anchors


def check_documents(root):
    root = Path(root).resolve()
    errors = []
    anchor_cache = {}
    paths = [root / "README.md", root / "CONTRIBUTING.md"]
    for folder in ("docs", "templates"):
        paths.extend(sorted((root / folder).rglob("*.md")))
    for path in paths:
        if not path.exists():
            continue
        for line in prose_lines(path.read_text(encoding="utf-8")):
            for match in LINK.finditer(line):
                href = match.group(1) or match.group(2)
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
                if target != root and root not in target.parents:
                    errors.append(f"{path.relative_to(root)}: link escapes repository: {href}")
                elif not target.exists():
                    errors.append(f"{path.relative_to(root)}: missing file: {href}")
                elif url.fragment and target.suffix.lower() == ".md":
                    if target not in anchor_cache:
                        anchor_cache[target] = document_anchors(target.read_text(encoding="utf-8"))
                    if unquote(url.fragment) not in anchor_cache[target]:
                        errors.append(f"{path.relative_to(root)}: missing fragment: {href}")
    return errors


if __name__ == "__main__":
    problems = check_documents(Path(__file__).resolve().parents[1])
    print("\n".join(problems) if problems else "Local Markdown files and heading fragments OK.")
    raise SystemExit(bool(problems))
