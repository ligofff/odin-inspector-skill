#!/usr/bin/env python3
"""Validate repository structure and local links; no network or Unity required."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
skill = root / "skills" / "odin-inspector"
required = [root / "README.md", root / "LICENSE", root / "NOTICE.md",
            skill / "SKILL.md", skill / "agents" / "openai.yaml"]
required += [skill / "references" / (name + ".md") for name in
             ("attributes", "attribute-catalog", "serialization", "serializer-api", "editor-tools",
              "menu-windows", "processors-resolvers", "validator", "setup", "verification", "sources")]
errors = [f"Missing file: {p.relative_to(root)}" for p in required if not p.is_file()]
if (skill / "SKILL.md").is_file():
    content = (skill / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.S)
    if not match:
        errors.append("Missing frontmatter")
    else:
        fields = dict(line.split(": ", 1) for line in match[1].splitlines() if ": " in line)
        if fields.get("name") != "odin-inspector":
            errors.append("Unexpected skill name")
        if len(fields.get("description", "")) > 1024:
            errors.append("Description longer than 1024 characters")
        if not fields.get("description", "").strip():
            errors.append("Empty description")
for path in root.rglob("*.md"):
    for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        if "://" in target or target.startswith("#"):
            continue
        target = target.split("#", 1)[0]
        if not (path.parent / target).exists():
            errors.append(f"Broken local link in {path.relative_to(root)}: {target}")
sources = skill / "references" / "sources.md"
if sources.is_file() and len(set(re.findall(r"https://odininspector\.com/[^\s|)`]+", sources.read_text(encoding="utf-8")))) < 40:
    errors.append("Expected at least forty official source links")
if errors:
    raise SystemExit("\n".join(errors))
print("PASS: package structure, frontmatter, local links and official source index")
