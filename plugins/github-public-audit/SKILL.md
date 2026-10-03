---
name: github-public-audit
description: Audit a local Git repository before publishing it as a public GitHub repository. Use for GitHub public-readiness checks, secret and credential scanning, PII and internal identifier review, redaction guidance, changed-file audits, and Git-history exposure checks. This skill never publishes, pushes, commits, opens pull requests, deploys, or changes repository visibility.
---

# GitHub Public Audit

Assess whether a local Git repository is ready to be made public. Treat the audit as evidence-based risk detection, not a guarantee of safety.

## Safety boundary

- Default to scan-only. Do not edit repository files unless the user explicitly asks for automatic fixes.
- Never run `git commit`, `git push`, `gh pr create`, deployment commands, or repository visibility changes.
- Never rewrite Git history automatically. Explain rotation and history-cleaning options if a committed secret is found.
- Do not print detected secret values. Report rule, severity, path, line, and a meaningful replacement placeholder.
- Skip ignored files. Do scan tracked files even when a current ignore rule matches them.
- Do not follow symbolic links.

## Select the audit mode

- Use **full** for a general pre-publication audit. It scans publishable working-tree files and all reachable Git history.
- Use **diff** when the user asks to inspect only recent or uncommitted changes. It scans staged changes, unstaged changes, and untracked non-ignored files. State clearly that Git history was not scanned.

## Run the deterministic scanner

1. Resolve the requested path. If none is given, use the current working directory.
2. Confirm it is a Git repository with `git -C <path> rev-parse --is-inside-work-tree`. Stop with a clear error if it is not.
3. From this skill directory, run:

   ```bash
   python3 scripts/audit_repo.py --repo <path> --mode full --format json
   ```

   Replace `full` with `diff` when appropriate. Exit codes are `0` for PASS, `1` for WARN, `2` for FAIL, and `3` for an operational error.
4. Review every finding in context before presenting it. The scanner supplies conservative leads; downgrade or dismiss obvious examples, placeholders, generated test data, and public identifiers only when the surrounding evidence supports that decision.
5. If `gitleaks` is already installed, optionally use it as an additional full-mode check. Do not install it without permission, do not expose its raw secret matches, and merge only validated findings into the report.

Read [references/classification.md](references/classification.md) when classifying findings, choosing replacements, or preparing the final report.

## Inspect efficiently

- Prioritize `.env`, logs, dumps, SQL, backups, keys, certificates, databases, CSV, JSON, YAML, TOML, shell scripts, Markdown, and files under `docs/`, `examples/`, `scripts/`, `fixtures/`, and `tests/`.
- For large JSON, CSV, and log files, search by rules first and inspect only suspicious snippets.
- For binary files, inspect only metadata such as path, extension, size, and tracking state.
- Warn when a symlink resolves outside the repository; never traverse it.
- Treat Unix paths case-sensitively: `/Users/<name>/...` is a macOS path, while `/users/{actorId}/...` can be an application namespace and must not match that rule. Match Windows `C:\\Users\\...` case-insensitively.
- Do not perform broad "unknown public URL" scans. For supplemental endpoint review, limit automatic findings to localhost, private or link-local networks, direct IP-address URLs, and `.local` or `.internal` hosts.
- Exclude dependency-distribution URLs in lockfiles such as `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `uv.lock`, `poetry.lock`, `Cargo.lock`, and `Gemfile.lock` from URL-only supplemental findings. Continue scanning those files for credentials and other secret patterns.

## Apply fixes only when requested

When the user explicitly requests fixes:

1. Replace confirmed sensitive values with descriptive placeholders such as `<AWS_ACCOUNT_ID>` or `<INTERNAL_API_URL>`.
2. Preserve syntax and behavior where possible. Avoid replacing values that are demonstrably public or intentionally synthetic.
3. Do not alter Git history as part of ordinary file fixes.
4. Re-run the same audit mode and report what remains.
5. If a real credential appeared anywhere, recommend revoking or rotating it even after replacing the file content.

## Report the decision

Return `PASS`, `WARN`, or `FAIL` using the fixed report shape in the classification reference. A PASS means no major issue was detected by this audit; never describe it as absolute proof of safety.
