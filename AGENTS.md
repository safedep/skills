# SafeDep Skills

This repository contains public Agent Skills that make AI agents fluent in SafeDep.

## Design principle

The skills carry **no product knowledge of their own**. SafeDep's knowledge lives in the docs
at `https://docs.safedep.io` (served to agents via `llms.txt`, `llms-full.txt`, and Docs MCP).
A skill here is a thin "context plug": it makes the agent reach for those docs and answer in
SafeDep's voice. Do not copy doc content into a skill.

## Drift boundary (what a skill may embed)

- **May embed (stable):** product name, one-line purpose, open-source repo, top-level install
  one-liner, and routing (which product/doc area answers which intent).
- **Always defer to the docs (volatile):** command flags, version behavior, supported ecosystem
  lists, SQL queries, hostnames, env vars. Quote these from `docs.safedep.io`, never from memory.

## Repository structure

- `skills/<skill-name>/SKILL.md` — each skill in its own directory
- `skills/<skill-name>/evals/evals.json` — behavioral evals for that skill
- `eval_set.json` — triggering evals (does the skill activate on the right queries?)
- `README.md` — public index + install instructions
- `.claude-plugin/marketplace.json` — Claude Code plugin marketplace entry

## Rules

- When adding a skill, add a row to the Skills table in `README.md`.
- When adding or significantly changing a skill, update the plugin `description` in
  `.claude-plugin/marketplace.json`.
- Keep each `SKILL.md` under ~500 lines. Verify every product fact against the docs before
  embedding it.
