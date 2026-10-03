# Classification and reporting reference

Use this reference to make consistent public-readiness decisions after reviewing scanner findings in context.

## Severity

### CRITICAL

- Live access keys, API keys, OAuth tokens, bearer tokens, session secrets, JWT secrets, private keys, passwords, or database credentials.
- Credential-shaped values assigned to names such as `AWS_SECRET_ACCESS_KEY`, `GITHUB_TOKEN`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `CF_API_TOKEN`, `PASSWORD`, `PRIVATE_KEY`, or `Authorization`.
- A database connection string containing a password.

Any confirmed CRITICAL finding makes the result FAIL. Recommend immediate revocation or rotation when the value may ever have been valid.

### HIGH

- Tracked `.env`, `.env.local`, `.env.production`, `.env.development`, or `.envrc` files containing non-placeholder operational values.
- Internal API URLs, private network addresses, authentication endpoints, session information, database URLs, or confidential infrastructure details.
- Sensitive key, certificate, database, dump, or backup files whose contents cannot be safely verified as synthetic.

Any confirmed HIGH finding makes the result FAIL.

### MEDIUM

- Personal email addresses, phone numbers, names, addresses, usernames, or stable personal identifiers.
- Absolute developer paths such as `/Users/<username>/`, `/home/<username>/`, and `C:\\Users\\<username>\\`.
- AWS account IDs and ARNs, S3 bucket names, AgentCore runtime IDs or ARNs, Bedrock Knowledge Base IDs, Cloudflare account or gateway IDs, API Gateway IDs, Google project IDs, tenant IDs, and similar infrastructure identifiers.
- Symbolic links that resolve outside the repository.

Confirmed MEDIUM findings normally produce WARN unless context raises them to HIGH.

### INFO

- Public URLs, AWS regions, service names, clearly marked sample IDs, and other intentionally public metadata.
- Binary or oversized files noted for manual review without evidence that they contain sensitive material.

INFO alone does not prevent PASS.

## Context and false positives

- Treat blank values and obvious placeholders such as `<TOKEN>`, `${TOKEN}`, `example`, `sample`, `changeme`, `redacted`, `xxx`, and repeated mask characters as non-secrets.
- Do not downgrade a value merely because it appears in documentation, a fixture, a test, or an old commit. Confirm that it is synthetic first.
- `.env.example` and `.env.sample` are acceptable only when their sensitive fields contain placeholders.
- A variable name without an assigned value is not a credential leak.
- A public ARN or account ID is not normally a secret, but it can disclose infrastructure and should remain MEDIUM unless publication is intentional.
- A tracked file remains in publication scope even if it now matches `.gitignore`.
- Findings in any reachable commit or tag remain publicly retrievable after a normal push. Removing them from the current file is not enough.
- Match `/Users/<username>/...` and `/home/<username>/...` case-sensitively. Do not classify lowercase application namespaces such as `/users/{actorId}/facts` as developer-local paths. Windows drive paths beginning with `C:\\Users\\...` may be matched case-insensitively.

## URL review

- Automatically flag localhost, loopback addresses, RFC 1918 private IPv4 ranges, link-local addresses, direct IP-address HTTP(S) endpoints, and hosts ending in `.local` or `.internal`.
- Do not flag a domain merely because it is absent from a hand-written allowlist. Public package registries, source archives, documentation sites, license links, schema URLs, and integrity metadata are not internal endpoints by default.
- For URL-only supplemental scans, skip dependency lockfiles including `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `uv.lock`, `poetry.lock`, `Cargo.lock`, and `Gemfile.lock`. This exception applies only to ordinary URL findings; always retain credential, token, private-key, and authenticated-connection-string scanning in those files.
- Treat a direct public-IP endpoint as HIGH when it identifies an operational service. Downgrade clearly synthetic documentation addresses, such as the ranges reserved for examples, after context review.

## Suggested replacements

Use meaningful uppercase placeholders:

| Value | Replacement |
|---|---|
| AWS access key | `<AWS_ACCESS_KEY_ID>` |
| AWS account ID | `<AWS_ACCOUNT_ID>` |
| AWS secret key | `<AWS_SECRET_ACCESS_KEY>` |
| AgentCore runtime ARN | `<AGENTCORE_RUNTIME_ARN>` |
| Bedrock Knowledge Base ID | `<BEDROCK_KNOWLEDGE_BASE_ID>` |
| Cloudflare account ID | `<CF_ACCOUNT_ID>` |
| Cloudflare gateway ID | `<CF_GATEWAY_ID>` |
| GitHub token | `<GITHUB_TOKEN>` |
| OpenAI key | `<OPENAI_API_KEY>` |
| Internal endpoint | `<INTERNAL_API_URL>` |
| Email address | `<CONTACT_EMAIL>` |
| Local username or path | `<LOCAL_USER>` or `<PROJECT_PATH>` |

## Decision rules

- **FAIL**: one or more confirmed CRITICAL or HIGH findings exist in the working tree, diff, or Git history.
- **WARN**: no confirmed CRITICAL/HIGH finding exists, but one or more MEDIUM findings or material coverage limitations require confirmation.
- **PASS**: no major issue was detected and no unresolved MEDIUM finding remains.
- If history was not scanned, say so explicitly. Do not imply that repository history is ready for publication.
- If the scan was truncated, skipped unreadable content, or could inspect only binary metadata, describe the limitation and prefer WARN when it materially affects confidence.

## Required report shape

```text
GitHub Public Readiness
=======================
Result: FAIL

Scanned:
- Working tree: YES
- Git history: YES
- Ignored files: SKIPPED

Findings:
CRITICAL
- path/to/file:12 — credential description
  Suggested replacement: <TOKEN_NAME>

HIGH
- None

MEDIUM
- path/to/file:8 — infrastructure identifier description
  Suggested replacement: <SERVICE_ID>

INFO
- None

Recommendation:
DO NOT PUSH
```

Use `DO NOT PUSH` for FAIL, `REVIEW BEFORE PUSH` for WARN, and `Ready for public GitHub repository.` for PASS. Include the scanner's coverage limitations. Never include the matched secret value in the report.
