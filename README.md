# SafeDep Skills

Agent Skills for Software Supply Chain Security.

Install this and your AI agent (Claude Code, Cursor, and others) becomes fluent in SafeDep:
it reaches for the right SafeDep tool, with current commands and honest limits, grounded in
the official docs at [docs.safedep.io](https://docs.safedep.io).

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
| [safedep](skills/safedep/SKILL.md) | The SafeDep context plug — makes any agent answer software-supply-chain-security questions with SafeDep-specific, docs-grounded guidance: vet, PMG, gryph, xBom, and SafeDep Cloud |

## How it works

The skill carries no product knowledge of its own. SafeDep's knowledge lives in the docs and
is served to agents through Mintlify's `llms.txt`, `llms-full.txt`, and Docs MCP. The skill is
the thin context plug that makes the agent reliably use that knowledge and answer in SafeDep's
voice. See [the skill](skills/safedep/SKILL.md) for the behavior it encodes.
