#!/usr/bin/env python3
"""Read-only GitHub public-readiness scanner.

The scanner intentionally emits metadata only; matched values are never printed.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_HISTORY_LINES = 2_000_000
MAX_FINDINGS = 1000
SENSITIVE_ENV = {".env", ".env.local", ".env.production", ".env.development", ".envrc"}
SENSITIVE_EXTENSIONS = {
    ".pem", ".key", ".p12", ".pfx", ".sqlite", ".db", ".dump", ".bak", ".backup"
}
EXAMPLE_DOMAINS = {"example.com", "example.org", "example.net", "localhost"}


@dataclass(frozen=True)
class Rule:
    name: str
    severity: str
    pattern: re.Pattern[str]
    message: str
    replacement: str
    value_group: int = 0


@dataclass
class Finding:
    severity: str
    rule: str
    scope: str
    path: str
    line: int | None
    message: str
    replacement: str
    commit: str | None = None
    evidence: str = "<REDACTED>"


FLAGS = re.IGNORECASE
RULES = [
    Rule("private_key", "CRITICAL", re.compile(r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
         "Private key material detected", "<PRIVATE_KEY>"),
    Rule("aws_access_key", "CRITICAL", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
         "AWS access key-shaped value detected", "<AWS_ACCESS_KEY_ID>"),
    Rule("github_token", "CRITICAL", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
         "GitHub token-shaped value detected", "<GITHUB_TOKEN>"),
    Rule("openai_key", "CRITICAL", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
         "API key-shaped value detected", "<OPENAI_API_KEY>"),
    Rule("bearer_token", "CRITICAL", re.compile(r"\bBearer\s+([A-Za-z0-9._~+/=-]{16,})", FLAGS),
         "Bearer token detected", "Bearer <ACCESS_TOKEN>", 1),
    Rule("credential_assignment", "CRITICAL", re.compile(
        r"\b(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN|OPENAI_API_KEY|"
        r"ANTHROPIC_API_KEY|CF_API_TOKEN|JWT_SECRET|PASSWORD|PRIVATE_KEY|AUTHORIZATION)"
        r"\b\s*[:=]\s*[\"']?([^\s\"'`,;#]{4,})", FLAGS),
         "Sensitive variable contains a non-placeholder value", "<SECRET>", 2),
    Rule("database_credentials", "CRITICAL", re.compile(
        r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s/:]+:([^\s/@]+)@", FLAGS),
         "Database URL contains credentials", "<DATABASE_URL>", 1),
    Rule("internal_url", "HIGH", re.compile(
        r"https?://(?:localhost|127\.0\.0\.1|10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|"
        r"172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2}|169\.254(?:\.\d{1,3}){2}|"
        r"100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])(?:\.\d{1,3}){2}|"
        r"[A-Za-z0-9.-]+\.(?:internal|local))(?::\d+)?\S*", FLAGS),
         "Internal or private endpoint detected", "<INTERNAL_API_URL>"),
    Rule("direct_ip_url", "HIGH", re.compile(
        r"https?://(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?(?:[/?#][^\s\"']*)?", FLAGS),
         "Direct IP-address endpoint detected", "<IP_ENDPOINT_URL>"),
    Rule("agentcore_arn", "MEDIUM", re.compile(r"arn:aws:bedrock-agentcore:[a-z0-9-]+:\d{12}:runtime/[A-Za-z0-9_-]+", FLAGS),
         "AgentCore runtime ARN detected", "<AGENTCORE_RUNTIME_ARN>"),
    Rule("aws_arn", "MEDIUM", re.compile(r"\barn:aws(?:-[a-z]+)?:[a-z0-9-]+:[a-z0-9-]*:\d{12}:[^\s\"']+", FLAGS),
         "AWS ARN detected", "<AWS_RESOURCE_ARN>"),
    Rule("s3_bucket", "MEDIUM", re.compile(r"\bs3://[a-z0-9][a-z0-9.-]{1,61}[a-z0-9](?:/[^\s\"']*)?", FLAGS),
         "S3 bucket reference detected", "s3://<S3_BUCKET_NAME>"),
    Rule("aws_account_id", "MEDIUM", re.compile(r"\b(?:aws[_ -]?account(?:[_ -]?id)?|account[_ -]?id)\b\s*[:=]\s*[\"']?(\d{12})\b", FLAGS),
         "AWS account ID detected", "<AWS_ACCOUNT_ID>", 1),
    Rule("cloudflare_id", "MEDIUM", re.compile(r"\b(?:CF_|CLOUDFLARE_)(?:ACCOUNT|GATEWAY)_ID\b\s*[:=]\s*[\"']?([a-f0-9]{16,64})\b", FLAGS),
         "Cloudflare account or gateway ID detected", "<CF_ACCOUNT_OR_GATEWAY_ID>", 1),
    Rule("bedrock_kb_id", "MEDIUM", re.compile(r"\b(?:KNOWLEDGE_BASE_ID|BEDROCK_KNOWLEDGE_BASE_ID)\b\s*[:=]\s*[\"']?([A-Z0-9]{10})\b", FLAGS),
         "Bedrock Knowledge Base ID detected", "<BEDROCK_KNOWLEDGE_BASE_ID>", 1),
    Rule("local_path", "MEDIUM", re.compile(
        r"(?:/Users/[^/\s]+/|/home/[^/\s]+/|(?i:C:\\{1,2}Users\\{1,2}[^\\\s]+\\{1,2}))"),
         "Developer-local absolute path detected", "<PROJECT_PATH>"),
    Rule("email", "MEDIUM", re.compile(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", FLAGS),
         "Email address detected", "<CONTACT_EMAIL>", 1),
    Rule("phone", "MEDIUM", re.compile(r"(?<!\w)\+(?:\d[ -]?){9,14}\d(?!\w)"),
         "International phone number detected", "<PHONE_NUMBER>"),
]

ENV_ASSIGNMENT = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$")
PLACEHOLDER = re.compile(
    r"^(?:$|<[^>]+>|\$\{[^}]+\}|\{\{[^}]+\}\}|(?:example|sample|changeme|redacted|dummy|test|none|null)|"
    r"x{3,}|\*{3,}|_+)$", FLAGS
)
KEY_REPLACEMENTS = {
    "AWS_ACCESS_KEY_ID": "<AWS_ACCESS_KEY_ID>",
    "AWS_SECRET_ACCESS_KEY": "<AWS_SECRET_ACCESS_KEY>",
    "GITHUB_TOKEN": "<GITHUB_TOKEN>",
    "OPENAI_API_KEY": "<OPENAI_API_KEY>",
    "ANTHROPIC_API_KEY": "<ANTHROPIC_API_KEY>",
    "CF_API_TOKEN": "<CF_API_TOKEN>",
    "JWT_SECRET": "<JWT_SECRET>",
    "PASSWORD": "<PASSWORD>",
    "PRIVATE_KEY": "<PRIVATE_KEY>",
    "AUTHORIZATION": "<AUTHORIZATION_VALUE>",
}


class AuditError(RuntimeError):
    pass


class Auditor:
    def __init__(self, root: Path, mode: str) -> None:
        self.root = root
        self.mode = mode
        self.findings: list[Finding] = []
        self.limitations: list[str] = []
        self.seen: set[tuple[object, ...]] = set()

    def git(self, *args: str, text: bool = True) -> str | bytes:
        proc = subprocess.run(
            ["git", "-C", str(self.root), *args], capture_output=True, text=text, check=False
        )
        if proc.returncode != 0:
            error = proc.stderr.strip() if text else proc.stderr.decode("utf-8", "replace").strip()
            raise AuditError(error or f"git {' '.join(args)} failed")
        return proc.stdout

    def add(self, finding: Finding) -> None:
        key = (finding.scope, finding.path, finding.line, finding.commit, finding.rule)
        if key in self.seen:
            return
        if len(self.findings) >= MAX_FINDINGS:
            if "Finding limit reached; additional matches were omitted." not in self.limitations:
                self.limitations.append("Finding limit reached; additional matches were omitted.")
            return
        self.seen.add(key)
        self.findings.append(finding)

    @staticmethod
    def is_placeholder(value: str) -> bool:
        value = value.strip().strip("\"'").rstrip(",;")
        return bool(PLACEHOLDER.fullmatch(value)) or "placeholder" in value.lower()

    def scan_line(self, line: str, *, scope: str, path: str, number: int | None,
                  commit: str | None = None) -> None:
        if len(line) > 1_000_000:
            line = line[:1_000_000]
            note = f"An oversized line was truncated while scanning {path}."
            if note not in self.limitations:
                self.limitations.append(note)

        basename = Path(path).name
        if basename in SENSITIVE_ENV:
            env_match = ENV_ASSIGNMENT.match(line)
            if env_match and not env_match.group(1).startswith("#") and not self.is_placeholder(env_match.group(2)):
                self.add(Finding("HIGH", "tracked_env_value", scope, path, number,
                                 "Sensitive environment file contains a non-placeholder value",
                                 f"<{env_match.group(1)}>", commit))

        claimed_spans: list[tuple[int, int]] = []
        for rule in RULES:
            for match in rule.pattern.finditer(line):
                value = match.group(rule.value_group) if rule.value_group else match.group(0)
                if self.is_placeholder(value):
                    continue
                if rule.name == "email" and match.group(1).lower() in EXAMPLE_DOMAINS:
                    continue
                value_span = match.span(rule.value_group) if rule.value_group else match.span()
                if any(value_span[0] < end and start < value_span[1] for start, end in claimed_spans):
                    continue
                replacement = rule.replacement
                if rule.name == "credential_assignment":
                    replacement = KEY_REPLACEMENTS.get(match.group(1).upper(), "<SECRET>")
                self.add(Finding(rule.severity, rule.name, scope, path, number,
                                 rule.message, replacement, commit,
                                 f"<REDACTED:{rule.name}>") )
                claimed_spans.append(value_span)

    def scan_path(self, rel: str, *, scope: str, tracked: bool) -> None:
        path = self.root / rel
        try:
            if path.is_symlink():
                target = (path.parent / os.readlink(path)).resolve(strict=False)
                try:
                    target.relative_to(self.root)
                except ValueError:
                    self.add(Finding("MEDIUM", "external_symlink", scope, rel, None,
                                     "Symlink resolves outside the repository", "<IN_REPOSITORY_PATH>"))
                return
            size = path.stat().st_size
            with path.open("rb") as handle:
                head = handle.read(8192)
                if b"\0" in head:
                    severity = "HIGH" if tracked and path.suffix.lower() in SENSITIVE_EXTENSIONS else "INFO"
                    self.add(Finding(severity, "binary_metadata", scope, rel, None,
                                     f"Binary file requires metadata review ({size} bytes)", "<REMOVE_OR_REPLACE_FILE>"))
                    return
                handle.seek(0)
                consumed = 0
                for line_number, raw in enumerate(handle, 1):
                    consumed += len(raw)
                    if consumed > MAX_FILE_BYTES:
                        self.limitations.append(f"Stopped scanning {rel} after {MAX_FILE_BYTES} bytes.")
                        break
                    self.scan_line(raw.decode("utf-8", "replace"), scope=scope, path=rel,
                                   number=line_number)
        except (OSError, UnicodeError) as exc:
            self.limitations.append(f"Could not inspect {rel}: {type(exc).__name__}.")

    def current_files(self) -> tuple[list[str], set[str]]:
        published = self.git("ls-files", "-c", "-o", "--exclude-standard", "-z", text=False)
        tracked_raw = self.git("ls-files", "-c", "-z", text=False)
        decode = lambda raw: [p.decode("utf-8", "replace") for p in raw.split(b"\0") if p]
        return sorted(set(decode(published))), set(decode(tracked_raw))

    def scan_working_tree(self) -> None:
        paths, tracked = self.current_files()
        for rel in paths:
            self.scan_path(rel, scope="working_tree", tracked=rel in tracked)

    def scan_diff_text(self, diff: str, scope: str) -> None:
        path = "<unknown>"
        new_line = 0
        for raw in diff.splitlines():
            if raw.startswith("+++ b/"):
                path = raw[6:]
            elif raw.startswith("@@"):
                match = re.search(r"\+(\d+)", raw)
                new_line = int(match.group(1)) if match else 0
            elif raw.startswith("+") and not raw.startswith("+++"):
                self.scan_line(raw[1:], scope=scope, path=path, number=new_line)
                new_line += 1
            elif raw.startswith(" "):
                new_line += 1

    def scan_diff(self) -> None:
        self.scan_diff_text(str(self.git("diff", "--no-ext-diff", "--unified=0", "--", ".")), "unstaged_diff")
        self.scan_diff_text(str(self.git("diff", "--cached", "--no-ext-diff", "--unified=0", "--", ".")), "staged_diff")
        published, tracked = self.current_files()
        for rel in published:
            if rel not in tracked:
                self.scan_path(rel, scope="untracked", tracked=False)

    def scan_history(self) -> None:
        command = ["git", "-C", str(self.root), "log", "--all", "--full-history", "-p",
                   "--no-ext-diff", "--no-renames", "--unified=0", "--format=__COMMIT__%H", "--", "."]
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                encoding="utf-8", errors="replace")
        assert proc.stdout is not None
        commit: str | None = None
        path = "<unknown>"
        new_line = 0
        count = 0
        for raw in proc.stdout:
            count += 1
            if count > MAX_HISTORY_LINES:
                self.limitations.append("Git history scan reached its line limit and was truncated.")
                proc.terminate()
                break
            line = raw.rstrip("\n")
            if line.startswith("__COMMIT__"):
                commit = line.removeprefix("__COMMIT__")[:12]
            elif line.startswith("+++ b/"):
                path = line[6:]
            elif line.startswith("@@"):
                match = re.search(r"\+(\d+)", line)
                new_line = int(match.group(1)) if match else 0
            elif line.startswith("+") and not line.startswith("+++"):
                self.scan_line(line[1:], scope="git_history", path=path, number=new_line, commit=commit)
                new_line += 1
            elif line.startswith(" "):
                new_line += 1
        stderr = proc.stderr.read() if proc.stderr else ""
        return_code = proc.wait()
        if return_code not in (0, -15) and count <= MAX_HISTORY_LINES:
            raise AuditError(stderr.strip() or "git history scan failed")

    def result(self) -> str:
        severities = {finding.severity for finding in self.findings}
        if severities & {"CRITICAL", "HIGH"}:
            return "FAIL"
        if "MEDIUM" in severities or self.limitations:
            return "WARN"
        return "PASS"

    def report(self) -> dict[str, object]:
        result = self.result()
        return {
            "title": "GitHub Public Readiness",
            "result": result,
            "scanned": {
                "working_tree": self.mode == "full",
                "diff": self.mode == "diff",
                "git_history": self.mode == "full",
                "ignored_files": "SKIPPED",
            },
            "findings": [asdict(item) for item in sorted(
                self.findings,
                key=lambda item: ({"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "INFO": 3}[item.severity],
                                  item.path, item.line or 0),
            )],
            "limitations": sorted(set(self.limitations)),
            "recommendation": {
                "FAIL": "DO NOT PUSH",
                "WARN": "REVIEW BEFORE PUSH",
                "PASS": "Ready for public GitHub repository.",
            }[result],
        }


def render_text(report: dict[str, object]) -> str:
    scanned = report["scanned"]
    findings = report["findings"]
    assert isinstance(scanned, dict) and isinstance(findings, list)
    lines = ["GitHub Public Readiness", "=======================", f"Result: {report['result']}", "", "Scanned:"]
    lines.extend([
        f"- Working tree: {'YES' if scanned['working_tree'] else 'NO'}",
        f"- Diff: {'YES' if scanned['diff'] else 'NO'}",
        f"- Git history: {'YES' if scanned['git_history'] else 'NO'}",
        "- Ignored files: SKIPPED", "", "Findings:",
    ])
    for severity in ("CRITICAL", "HIGH", "MEDIUM", "INFO"):
        lines.append(severity)
        selected = [item for item in findings if item["severity"] == severity]
        if not selected:
            lines.append("- None")
        for item in selected:
            location = item["path"] + (f":{item['line']}" if item["line"] else "")
            if item["commit"]:
                location += f" (commit {item['commit']})"
            lines.append(f"- {location} — {item['message']}")
            lines.append(f"  Suggested replacement: {item['replacement']}")
        lines.append("")
    limitations = report["limitations"]
    if limitations:
        lines.append("Limitations:")
        lines.extend(f"- {item}" for item in limitations)
        lines.append("")
    lines.extend(["Recommendation:", str(report["recommendation"])])
    return "\n".join(lines)


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="Path inside the Git repository to audit")
    parser.add_argument("--mode", choices=("full", "diff"), default="full")
    parser.add_argument("--format", choices=("json", "text"), default="text")
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    requested = Path(args.repo).expanduser().resolve()
    check = subprocess.run(["git", "-C", str(requested), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=False)
    if check.returncode != 0:
        print(json.dumps({"error": "The requested path is not inside a Git repository."})
              if args.format == "json" else "ERROR: The requested path is not inside a Git repository.",
              file=sys.stderr)
        return 3
    auditor = Auditor(Path(check.stdout.strip()).resolve(), args.mode)
    try:
        if args.mode == "full":
            auditor.scan_working_tree()
            auditor.scan_history()
        else:
            auditor.scan_diff()
        report = auditor.report()
    except AuditError as exc:
        print(json.dumps({"error": str(exc)}) if args.format == "json" else f"ERROR: {exc}", file=sys.stderr)
        return 3
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.format == "json" else render_text(report))
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[str(report["result"])]


if __name__ == "__main__":
    raise SystemExit(main())
