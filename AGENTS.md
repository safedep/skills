# SafeDep Skills

This repository contains public Agent Skills that make AI agents fluent in SafeDep.

## Design principle

The skills carry **no product knowledge of their own**. SafeDep's knowledge lives in two places:

- **safedep.io** is the source of truth for messaging: what SafeDep is, who it is for, which
  product fits which problem, pricing and trust. Agents read it through `https://safedep.io/llms.txt`.
- **docs.safedep.io** is the source of truth for technical documentation: how to install,
  configure and use each feature. Agents read it through the Docs MCP server, `llms.txt`, and
  each page as `.md`.

A skill here is a thin "context plug": it sends the agent to the right source and makes it act
safely. Do not copy site or doc content into a skill.

## Drift boundary (what a skill may embed)

- **May embed (stable):** product names, a one-line purpose in safedep.io's words, open source
  repos, the source entry points (`llms.txt` URLs, the Docs MCP server URL and its tool names),
  and routing: which product and which docs path answer which intent.
- **Always defer to the source (volatile):** command flags, version behavior, supported
  ecosystem lists, SQL queries, hostnames, env vars, prices. Quote these from the docs or
  safedep.io, never from memory.
- **Refer to docs pages by path** (for example `/package-security/pmg/quickstart`), in
  backticks, so `scripts/check_skills.py` can check them against the docs `llms.txt`.

## Repository structure

- `skills/<skill-name>/SKILL.md` — each skill in its own directory
- `skills/<skill-name>/resources/*.md` — detailed reference files, linked from `SKILL.md` and
  loaded by agents on demand (keeps `SKILL.md` a small router)
- `skills/<skill-name>/evals/evals.json` — behavioral evals for that skill
- `eval_set.json` — triggering evals (does the skill activate on the right queries?)
- `scripts/check_skills.py` — spec limits and link drift check, run in CI
- `.mcp.json` — the Docs MCP server, bundled with the Claude Code plugin
- `README.md` — public index + install instructions
- `.claude-plugin/marketplace.json` — Claude Code plugin marketplace entry

## Rules

- When adding a skill, add a row to the Skills table in `README.md`.
- When adding or significantly changing a skill, update the plugin `description` in
  `.claude-plugin/marketplace.json`.
- Keep each `SKILL.md` under ~500 lines and each `description` under 1,024 characters. Verify
  every product fact against safedep.io or the docs before embedding it.
- Run `python3 scripts/check_skills.py` before opening a pull request.
- Do not add a fixed `version` to the plugin entry: Claude Code then tracks updates by commit.
  A fixed version blocks updates unless it is bumped on every release.
