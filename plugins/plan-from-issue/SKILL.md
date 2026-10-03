---
name: plan-from-issue
description: Analyze a GitHub Issue against its repository without implementing it, divide the work into independently reviewable phases with acceptance criteria, and create a planning-only Draft PR when requested and unblocked. Use when turning an Issue into an implementation plan or Draft planning PR; do not use to implement the Issue.
---

# Plan From Issue

Turn a GitHub Issue into an evidence-based implementation plan. The deliverable is analysis and, when authorized, a Draft PR containing planning documentation only.

## Hard boundaries

- Do not implement any part of the Issue.
- Do not modify source code, tests, schemas, configuration, manifests, lockfiles, snapshots, generated files, or build outputs.
- Do not stage or commit changes already present in the user's worktree.
- Read-only repository inspection does not authorize a branch, commit, comment, or PR. Create a Draft PR only when the current request explicitly asks to run this workflow or create the planning PR.
- The only repository change this workflow may create is one Markdown plan document on a dedicated planning branch.
- Do not close the Issue. Link the Draft PR with `Related to #<number>`, never `Closes`, `Fixes`, or `Resolves`.
- Do not convert the Draft PR to ready-for-review and do not start Phase 1.

## 1. Read the Issue and repository

Prefer the connected GitHub tooling for Issue and remote repository data. Read the complete Issue body and all comments, then inspect linked Issues, PRs, documents, or code when they affect scope.

Inspect the repository before planning:

- every applicable `AGENTS.md`, starting at the repository root and following scoped instructions for relevant paths;
- `README` and relevant contributor, architecture, security, or design documentation;
- the repository tree, manifests, and existing test structure;
- source files that establish current behavior and the likely change boundary;
- current branch and worktree status when a local checkout is available;
- existing branches or PRs for the Issue before creating a new one.

Do not install dependencies, run formatters, generate files, or execute commands that mutate the repository. Do not treat the Issue description alone as proof of current behavior.

## 2. Build the requirement model

Record:

- **Goal:** the observable outcome requested by the Issue;
- **Current behavior:** evidence from the repository;
- **Required behavior:** explicit Issue requirements and acceptance conditions;
- **Constraints and non-goals:** Issue and repository instructions;
- **Assumptions:** minor interpretations that do not materially change scope;
- **Questions:** missing decisions that would materially affect the solution;
- **Risks:** compatibility, security, data, migration, state, concurrency, performance, UX, or verification concerns relevant to this Issue.

Distinguish requirements from implementation ideas. Do not invent product scope to make the plan look complete.

## 3. Ambiguity gate

Do not create a branch or Draft PR when an unresolved question could materially change any of the following:

- data model, persistence, migration, or destructive behavior;
- authorization, security boundary, privacy, or secret handling;
- public API, compatibility promise, supported platform, or external integration;
- user-visible behavior with multiple plausible outcomes;
- the files, repository, base branch, or Issue actually in scope;
- phase boundaries or acceptance criteria;
- a contradiction between the Issue and repository instructions.

When blocked, stop before all external writes. Summarize the evidence, explain why the ambiguity is material, and ask the smallest number of concrete questions needed to proceed.

Minor ambiguity may be resolved with a conservative assumption. State that assumption under `Risks` in the proposed plan.

Also stop without creating a PR when repository write access is unavailable, a planning PR already exists, or the intended branch exists with unrelated work. Report the safe next action instead of overwriting or duplicating work.

## 4. Divide work into phases

Create the smallest useful set of phases; do not force a fixed count. Each phase must be:

- independently reviewable as a coherent change;
- independently verifiable through observable behavior;
- narrow enough that its acceptance criteria can be evaluated without completing unrelated later phases;
- ordered by real dependencies;
- explicit about what is out of scope when scope could otherwise expand.

Avoid phases that only rename files, create abstractions, or add scaffolding unless those actions form a necessary and reviewable prerequisite. Prefer vertical behavior slices over layer-by-layer tasks when the repository supports them.

For every phase, define acceptance criteria that are specific, testable, and written as outcomes. Include relevant success cases, edge cases, regression boundaries, and validation commands already supported by the repository. Do not prescribe a new test dependency merely to make the plan look complete.

Represent progress in this form:

```markdown
## Plan

- [ ] Phase 1: <reviewable outcome>
- [ ] Phase 2: <reviewable outcome>
```

All implementation phases remain unchecked in a planning-only PR.

## 5. Prepare the planning document

Follow an existing repository convention for plans when one exists. Otherwise use:

```text
docs/plans/issue-<number>-<short-slug>.md
```

The document should contain the requirement model, phase checklist, per-phase scope and acceptance criteria, risks, dependencies, expected change boundary, and non-goals. Keep code-level prescriptions limited to decisions supported by repository evidence.

## 6. Create the Draft PR

Only after the ambiguity gate passes:

1. Choose the repository's default branch as the base unless the user or Issue specifies another base.
2. Use a dedicated branch such as `plan/issue-<number>-<short-slug>`.
3. Prefer a remote GitHub API/connector workflow so the user's local worktree remains untouched.
4. Commit exactly the planning Markdown document. Verify the branch diff contains no source or generated changes.
5. Open the PR with Draft status and link the Issue using `Related to #<number>`.
6. Verify the returned PR is Draft, targets the intended base, and has only the planning change.

Use the following PR-body contract. Additional sections are allowed when they improve reviewability, but none of these headings may be omitted:

```markdown
## Goal

<Issue outcome and relevant non-goals>

Related to #<number>

## Plan

- [ ] Phase 1: <reviewable outcome>
- [ ] Phase 2: <reviewable outcome>

## Acceptance Criteria

### Phase 1

- [ ] <observable criterion>

### Phase 2

- [ ] <observable criterion>

## Risks

- <risk, assumption, or edge case and its planned handling>

## Current Phase

Planning complete. Implementation has not started. Next: Phase 1.
```

Do not post a separate Issue comment unless the user explicitly requests it. The `Related to` reference is the default Issue linkage.

## 7. Report the result

Return:

- the Draft PR link;
- the Issue link;
- branch name and plan-document path;
- confirmation that no implementation or source-code changes were made;
- any assumptions carried into `Risks`;
- the next unchecked phase.

If no Draft PR was created, say exactly which gate stopped it and what answer or permission is required.
