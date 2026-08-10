# Working with SafeDep Cloud from the CLI

The `safedep` CLI is SafeDep Cloud's client in the terminal. Its surface is broad and
growing (onboarding, endpoints, projects, queries, scans, billing, and more); run
`safedep --help` or fetch the docs for what it currently covers. Read this file before
running the first `safedep` cloud command in a session. It carries the stable behavior
rules for the workflows agents run most: signing in, SQL queries, and package verdicts.
Quote current commands, flags, and contracts from the docs at `https://docs.safedep.io`,
never from memory.

## The human signs in, not you

Commands that read a tenant's cloud data (for example `safedep query` and `safedep package
scan`) run through the safedep CLI with a signed-in session, and only a human can establish
one.

1. If the `safedep` CLI is not installed, fetch the docs page **Get Started › Install the
   SafeDep Skill** and give the human the minimal install command that fits their platform.
   The CLI's GitHub repository (github.com/safedep/cli) carries the full option list; lead
   with the docs steps.
2. Check sign-in state with `safedep auth status`.
3. If it fails, stop and ask the human to sign in with `safedep auth login`. Continue only
   after they confirm they signed in.
4. Confirm current authentication behavior against the docs (Cloud Platform › Authentication)
   rather than assuming it.

## SQL queries: confirm the schema, never guess joins

SafeDep Cloud exposes a SQL query interface (`safedep query exec --sql "..."`). Table and column
names, and the join edges between tables, are easy to get wrong, and a summarized index like
`llms.txt` may not carry them faithfully. Before writing or running a query:

1. Fetch the **Reference › SQL Query** page from the docs for the query syntax and examples.
   For endpoint investigations (a suspicious install, blocks, bypasses, stale endpoints),
   fetch **Cloud Platform › Endpoint Hub › Agentic Endpoint Investigation** for ready
   playbooks.
2. Confirm the actual columns and tables at runtime with `safedep query schema show <table>`
   (e.g. `endpoints`, `package_guard_events`). The full schema (`safedep query schema get`)
   also returns the server's usage rules and example queries. Read the rules before your
   first query: they are the query contract, and queries that break them are rejected.
3. Do not invent column names or join conditions. If you are unsure of a join, say so and have
   the user run `safedep query schema show` rather than guessing. A wrong join silently returns
   wrong data, which is worse than no answer.
4. When the server rejects a query, the error states the rule you broke. Correct the query
   from the error text and retry. Prefer narrow, filtered queries over dumping tables.

## Package verdicts: fast path first

To judge one specific package version, check SafeDep's known malicious packages database
first (through vet or the SafeDep MCP server): the free fast path. With `curl` available,
you can also hit the free community API directly. Pipe through `jq` and select only the
inference so the full report does not flood your context:

```bash
curl --http2 --json '{"target":{"package_version":{"package": {"ecosystem": "ECOSYSTEM_NPM", "name": "safedep-test-pkg"}, "version":"0.1.2"}}}' \
  https://community-api.safedep.io/safedep.services.malysis.v1.MalwareAnalysisService/QueryPackageAnalysis | jq '.report.inference'
```

An on-demand scan
(`safedep package scan`) is the slow path: a metered deep-dive analysis of the exact version
that spends the tenant's scan allowance. Offer it only when the fast path has no verdict and
the human wants a deep dive. Fetch **Package Security › On-Demand Package Scanning** for the
current commands, cost model, and result contract before running one.
