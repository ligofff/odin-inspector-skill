# Odin Inspector Agent Skill

A community-authored Agent Skill for Unity C# work with Sirenix Odin Inspector, based on official Sirenix documentation. Not affiliated with or endorsed by Sirenix. The skill is written in English for reuse across agents; it instructs agents to answer in the user's language.

## What it covers

- A categorized catalog of every attribute on the official attribute page, plus layout, conditional, dropdown and validation patterns.
- Display versus serialization, backend ownership, persistence diagnostics, `SerializationUtility` save data, refactoring, AOT/IL2CPP and Editor Only mode.
- `OdinEditorWindow`, `OdinMenuEditorWindow` menu trees, selectors and `OdinEditor`.
- Custom value, attribute and group drawers, drawer matching, IMGUI helpers and `PropertyTree` lifecycle.
- Value/action resolvers, named values, property states, attribute and property processors.
- `ISelfValidator`, Odin Validator custom validators, fixes, rules and CI pipelines.
- Installation detection, asmdefs, modules, source control, and honest Unity/build verification.

The reusable skill is `skills/odin-inspector/`. It contains `SKILL.md`, `agents/openai.yaml` and focused reference files under `references/` that the agent loads on demand. Official sources and review date are listed in [sources.md](skills/odin-inspector/references/sources.md).

## Install

Copy the entire `skills/odin-inspector` directory, preserving `references/` and `agents/`, into your agent's skills directory so that it contains `odin-inspector/SKILL.md`. For example:

- Claude Code: `~/.claude/skills/odin-inspector/` (personal) or `<project>/.claude/skills/odin-inspector/` (per project).
- Other agents: consult their documentation for the skills discovery path.

You can also give an agent the explicit path and ask it to read the skill:

> Use skills/odin-inspector/SKILL.md to build an inspector for this ScriptableObject. Preserve the current serializer and verify APIs against my installed Odin version.

Other example tasks:

> Diagnose why this dictionary appears in the inspector but is empty after restarting Unity.

> Implement a custom Odin drawer and check null labels, Undo and multi-object editing.

## Requirements and compatibility

The consuming project needs its own lawful Odin installation and Unity environment. Nothing here includes Odin or enables its serializer. There is no pinned minimum version or tested Unity/Odin compatibility matrix. The workflow is designed to verify the project's installed API before implementation. Online Sirenix documentation may describe different versions on different pages.

Documentation reviewed on 2026-11-09. The Markdown package and local references were checked; C# examples have not been compiled in Unity. They are original illustrative examples, not copied Sirenix tutorial code. Manual behavior scenarios live in [evals/scenarios.md](evals/scenarios.md).

## Validate

Run with Python 3 (standard library only):

```bash
python3 tools/validate.py
```

This checks package structure, frontmatter fields, local Markdown links and required official-source references. It does not compile C#, test Unity, or check remote URL availability.

## License and attribution

Original repository text, scripts and illustrative examples are under the MIT license; see [LICENSE](LICENSE). Official Sirenix documentation, Odin software and trademarks remain their owners' property and are not relicensed by this repository. See [NOTICE.md](NOTICE.md).
