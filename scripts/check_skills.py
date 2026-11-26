#!/usr/bin/env python3
"""Check every skill for spec limits and drift against SafeDep's live sources.

- Frontmatter: name matches its directory and the spec's format; description and
  compatibility stay within the spec's length limits.
- SKILL.md stays under 500 lines.
- Every docs path written as `/some/path` exists in https://docs.safedep.io/llms.txt.
- Every https URL to a SafeDep host answers without an error.

Standard library only. Run: python3 scripts/check_skills.py
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS_INDEX = "https://docs.safedep.io/llms.txt"
USER_AGENT = "safedep-skills-check/1.0"
SAFEDEP_HOSTS = ("safedep.io", "docs.safedep.io", "safedep.trust.site")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DOCS_PATH_RE = re.compile(r"`(/[a-z0-9][a-z0-9-]*(?:/[a-z0-9][a-z0-9-]*)*)`")
URL_RE = re.compile(r"https://[^\s`'\")<>|]+")


def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return err.code, ""


def parse_frontmatter(text):
    """Return {key: value} for top-level keys, folding block scalars into one line."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None
    fields, key = {}, None
    for line in match.group(1).splitlines():
        top = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if top:
            key, value = top.group(1), top.group(2).strip()
            fields[key] = "" if value in (">", ">-", "|", "|-") else value
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def docs_paths_index():
    status, body = fetch(DOCS_INDEX)
    if status != 200:
        sys.exit(f"cannot fetch {DOCS_INDEX}: HTTP {status}")
    paths = set(re.findall(r"https://docs\.safedep\.io(/[^\s)]+?)\.md\)", body))
    if not paths:
        sys.exit(f"no page paths found in {DOCS_INDEX}; has its format changed?")
    return paths


def main():
    errors = []
    known_paths = docs_paths_index()
    checked_urls = {}

    for skill_md in sorted(ROOT.glob("skills/*/SKILL.md")):
        skill_dir = skill_md.parent
        rel = skill_md.relative_to(ROOT)
        text = skill_md.read_text()

        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"{rel}: missing YAML frontmatter")
            continue
        name = fm.get("name", "")
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{rel}: name {name!r} is not 1-64 lowercase letters, digits and hyphens")
        if name != skill_dir.name:
            errors.append(f"{rel}: name {name!r} does not match directory {skill_dir.name!r}")
        desc = fm.get("description", "")
        if not 1 <= len(desc) <= 1024:
            errors.append(f"{rel}: description is {len(desc)} characters (spec: 1-1024)")
        if re.search(r"<[a-zA-Z/][^>]*>", desc):
            errors.append(f"{rel}: description contains an XML tag")
        if len(fm.get("compatibility", "")) > 500:
            errors.append(f"{rel}: compatibility is over 500 characters")
        lines = text.count("\n") + 1
        if lines > 500:
            errors.append(f"{rel}: {lines} lines (keep SKILL.md under 500)")

        for md in [skill_md, *sorted(skill_dir.glob("resources/*.md"))]:
            md_rel = md.relative_to(ROOT)
            body = md.read_text()
            for path in sorted(set(DOCS_PATH_RE.findall(body))):
                if path not in known_paths:
                    errors.append(f"{md_rel}: docs path {path} is not in {DOCS_INDEX}")
            for url in sorted(set(URL_RE.findall(body))):
                url = url.rstrip(".,;:")
                host = url.split("/")[2]
                if host not in SAFEDEP_HOSTS:
                    continue
                if url not in checked_urls:
                    status, _ = fetch(url)
                    # 405: the endpoint exists but wants another method (the Docs MCP server).
                    checked_urls[url] = status
                if checked_urls[url] >= 400 and checked_urls[url] != 405:
                    errors.append(f"{md_rel}: {url} returned HTTP {checked_urls[url]}")

    if errors:
        print("Skill check failed:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"Skill check passed ({len(known_paths)} docs pages indexed, {len(checked_urls)} URLs checked).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
