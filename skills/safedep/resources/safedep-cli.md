# The safedep CLI: SafeDep Cloud in the terminal

The `safedep` CLI is SafeDep Cloud's client in the terminal. It covers the whole cloud surface, not
only queries, and it grows. Current command domains (names only, not exhaustive):

| Domain | What it does |
|---|---|
| `safedep auth` | Sign in (device flow), sign out, session and tenant status, profiles |
| `safedep endpoint` | The fleet: list endpoints, per-endpoint detail, fleet health, activity and inventory |
| `safedep project` | Projects from linked repositories, their labels and cloud-hosted scans |
| `safedep policy` | The tenant's cloud policy: block and trust rules, changes (draft, preview, publish), decisions, revisions |
| `safedep audit` | Audit events for the tenant |
| `safedep package` | On-demand malware analysis of one package version: submit, poll, list, report |
| `safedep query` | SQL over tenant data: run statements, discover the schema |
| `safedep subscription` | Plan and billing: status, trial, addons, on-demand billing, billing portal |
| `safedep integration` | Integrations such as Bitbucket and JFrog |
| `safedep protect` / `safedep setup` | Install the SafeDep MCP server into AI coding agents |

## Discover, don't memorize

The CLI is a strict noun-verb tree built for discovery. Do not guess or recall flags:

1. Run `safedep --help` and `safedep <noun> --help` to find the right command.
2. Ask for JSON (`-o json`) on data commands so you can parse the output.
3. Server errors come back verbatim. Read them and correct course.
4. Exact flags live in `--help` and the `docs/cmd/` pages of github.com/safedep/cli.
5. The CLI can do more than docs.safedep.io shows. Before you say a command does not exist,
   check `safedep <noun> --help`, or with no shell, the `docs/cmd/` page list (one page per
   command).

## Pick the cheapest tool that answers

Move to the next rung only when the previous one cannot answer:

1. **A purpose-built command first.** Fleet health, silent endpoints, blocked installs, endpoint
   activity, scan status and plan status each have a direct command (mostly under
   `safedep endpoint`). One command, no schema work.
2. **A SQL query second** (`safedep query`), for questions the purpose-built commands cannot
   answer. Follow the SQL rules below.
3. **An on-demand scan last** (`safedep package scan`), for a deep-dive verdict. It is metered.
   Follow the verdict rules below.

## The human signs in, not you

Commands that read a tenant's data need a signed-in session, and only a human can create one.

1. If the CLI is not installed, fetch `/get-started/cli-tools` and give the user the install
   command for their platform. The CLI repository (github.com/safedep/cli) lists every option.
2. Check sign-in state with `safedep auth status`.
3. If it fails, stop and ask the user to sign in with `safedep auth login`. Continue only after
   they confirm.
4. Confirm current authentication behavior in `/governance/cloud/authentication` rather than
   assuming it.

## The human approves changes and spending

- **Spending.** `safedep subscription` changes (trial, addons, on-demand billing) change what the
  tenant pays, and rescanning an analyzed package spends the scan allowance. Run them only when
  the user asks, and say what it changes or costs first. Reading `safedep subscription status` is
  always fine.
- **Policy.** A published cloud policy change applies to every endpoint and project it targets.
  Draft the change, show the user the preview, and publish only on their explicit go-ahead. See
  `/concepts/policy-revisions` for how changes, previews and rollback work.

## SQL queries: confirm the schema, never guess joins

Table names, column names and the joins between tables are easy to get wrong. Before you write
or run a query:

1. Fetch `/reference/sql-query` for the syntax and `/governance/cloud/query-with-sql` for worked
   examples. For endpoint investigations (exposure to a compromised package, blocks, bypasses,
   endpoints that stopped reporting), fetch `/governance/cloud/endpoint-hub/agentic-investigation`
   for ready playbooks.
2. Confirm the tables and columns at runtime with the `safedep query schema` commands. The full
   schema also returns the server's usage rules and example queries. Read the rules before your
   first query: queries that break them are rejected.
3. Do not invent column names or join conditions. If you are unsure of a join, say so and check
   the schema. A wrong join silently returns wrong data, which is worse than no answer.
4. When the server rejects a query, the error names the rule you broke. Fix the query from the
   error and retry. Prefer narrow, filtered queries over dumping tables.

## Package verdicts: fast path first

1. **Fast path (free).** Check SafeDep's known malicious packages database first. It is built
   into vet, PMG and the SafeDep MCP server. Fetch `/package-security/scan/malware-lookup` for
   the current commands. It answers in milliseconds but only covers packages SafeDep has already
   analyzed.
2. **Slow path (metered).** An on-demand scan (`safedep package scan`) runs a new analysis of the
   exact version and spends the tenant's scan allowance. Offer it only when the fast path has no
   verdict and the user wants a deep dive. Fetch `/package-security/scan/overview` for the
   commands and cost model.
3. **Gate on the verdict, not the exit code.** Read the result contract in
   `/package-security/scan/automation`. Only a clean verdict passes. Treat anything else,
   including an inconclusive result, as needs-review, never as safe.
