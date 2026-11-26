# SafeDep Skills

Agent Skills for Software Supply Chain Security.

Install this and your AI agent (Claude Code, Cursor, and others) becomes fluent in SafeDep:
it reaches for the right SafeDep tool, with current commands and honest limits, grounded in
SafeDep's own sources: [safedep.io](https://safedep.io) for what SafeDep is and
[docs.safedep.io](https://docs.safedep.io) for how to use it.

## Installation

```
npx skills add safedep/skills
```

To update to the latest version:

```
npx skills update
```

### Claude Code

1. Add this repo as a plugin marketplace:
   ```
   /plugin marketplace add safedep/skills
   ```
2. Install the plugin:
   ```
   /plugin install safedep-agent-skills@safedep-agent-skills
   ```
3. Enable auto-update in Claude Code settings to keep the skill current.

The plugin also adds the SafeDep Docs MCP server (`https://docs.safedep.io/mcp`), so the agent
can search the docs directly. Other install methods fall back to fetching the docs pages.

### Cursor

1. Clone this repo and copy the skill into your project:
   ```
   git clone https://github.com/safedep/skills.git
   cp -r skills/skills/safedep .cursor/skills/
   ```
2. Cursor auto-discovers skills from `.cursor/skills/` on startup.

## Skills

| Skill | Description |
|-------|-------------|
| [safedep](skills/safedep/SKILL.md) | Routes SafeDep questions to the right source and helps set up SafeDep: PMG, vet, Gryph, xBom, the SafeDep MCP server, SafeDep Cloud and Threat Intel |

## How it works

The skill carries no product knowledge of its own. It routes each question to the source that
owns the answer:

- **safedep.io** (`https://safedep.io/llms.txt`): what SafeDep is, who it is for, which product
  fits a problem, pricing and trust.
- **docs.safedep.io** (Docs MCP, `llms.txt`, and any page as `.md`): how to install, configure
  and use each feature.
- **The tool's GitHub repository**: debugging and edge cases the docs do not cover.

The skill adds what those sources do not: a map from what users ask to the right product and
docs page, and rules for acting safely (the human signs in, approves spending and policy
changes, and OKs installs). See [the skill](skills/safedep/SKILL.md).

## Development

- `python3 scripts/check_skills.py` checks spec limits and that every docs path and SafeDep URL
  in a skill still resolves. CI runs it on every pull request and weekly, because the docs can
  change without a commit here.
- To try a local change in Claude Code, start a session with `claude --plugin-dir .` from the
  repository root.
