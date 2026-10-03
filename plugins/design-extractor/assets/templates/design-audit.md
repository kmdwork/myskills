# design-audit.md

このファイルは、既存アプリから `DESIGN.md` を作成するための根拠ログである。

`DESIGN.md` には整理された最終判断だけを書く。このファイルには、調査対象、観察、例外、未確認事項、推測を残す。

## Audit Summary

- App name: `<app name>`
- Audit date: `<YYYY-MM-DD>`
- Auditor: `<agent / person>`
- Scope: `<調査した範囲>`
- Out of scope: `<調査していない範囲>`

## Source Inventory

| Area | Files / Paths | Notes |
|------|---------------|-------|
| Theme / tokens | `<path>` | `<観察メモ>` |
| Global styles | `<path>` | `<観察メモ>` |
| Components | `<path>` | `<観察メモ>` |
| Layout / shell | `<path>` | `<観察メモ>` |
| Pages / routes | `<path>` | `<観察メモ>` |
| Assets | `<path>` | `<観察メモ>` |
| Docs / stories | `<path>` | `<観察メモ>` |

## Visual Theme Evidence

| Evidence | Observation | Extracted Rule | Confidence |
|----------|-------------|----------------|------------|
| `<path / component / screen>` | `<見つけた事実>` | `<DESIGN.md に反映するルール>` | `<high / medium / low>` |

## Color Evidence

| Token / Value | Found In | Usage | Notes | Confidence |
|---------------|----------|-------|-------|------------|
| `<value>` | `<path>` | `<button / bg / text / state>` | `<使い分けや例外>` | `<high / medium / low>` |

## Typography Evidence

| Style | Found In | Usage | Notes | Confidence |
|-------|----------|-------|-------|------------|
| `<size / weight / line-height>` | `<path>` | `<heading / body / label>` | `<使い分けや例外>` | `<high / medium / low>` |

## Component Evidence

| Component | Found In | Variants / States | Extracted Rule | Confidence |
|-----------|----------|-------------------|----------------|------------|
| `<Button>` | `<path>` | `<primary / secondary / disabled>` | `<ルール>` | `<high / medium / low>` |
| `<Card>` | `<path>` | `<default / interactive>` | `<ルール>` | `<high / medium / low>` |
| `<Input>` | `<path>` | `<default / focus / error>` | `<ルール>` | `<high / medium / low>` |

## Layout Evidence

| Screen / Layout | Found In | Observation | Extracted Rule | Confidence |
|-----------------|----------|-------------|----------------|------------|
| `<dashboard>` | `<path>` | `<構成、余白、グリッド>` | `<ルール>` | `<high / medium / low>` |

## Depth & Elevation Evidence

| Treatment | Found In | Usage | Extracted Rule | Confidence |
|-----------|----------|-------|----------------|------------|
| `<shadow / border / overlay>` | `<path>` | `<card / modal / menu>` | `<ルール>` | `<high / medium / low>` |

## Responsive Evidence

| Breakpoint / Pattern | Found In | Behavior | Extracted Rule | Confidence |
|----------------------|----------|----------|----------------|------------|
| `<md / 768px>` | `<path>` | `<grid collapse / nav change>` | `<ルール>` | `<high / medium / low>` |

## Exceptions

既存デザインから外れているが、実装上存在するものを記録する。

| Exception | Found In | Why It Is Exception | Action |
|-----------|----------|---------------------|--------|
| `<例外>` | `<path>` | `<通常ルールと違う理由>` | `<ignore / document / ask user>` |

## Legacy / Unused / Unclear

旧UI、未使用と思われるコンポーネント、利用状況が不明なものを記録する。

| Item | Found In | Status | Notes |
|------|----------|--------|-------|
| `<item>` | `<path>` | `<legacy / unused / unclear>` | `<メモ>` |

## Weak Signals

根拠が少なく、`DESIGN.md` で断定しない観察を記録する。

- `<弱い観察>`
- `<弱い観察>`

## Open Questions

ユーザー確認が必要な事項。

- `<質問>`
- `<質問>`

## Recommendations

必要に応じて、DESIGN.md とは別に改善案を記録する。

- `<改善案>`
- `<改善案>`

## Final Consistency Check

- [ ] `DESIGN.md` は9セクション構造になっている
- [ ] `DESIGN.md` にプレースホルダーが残っていない
- [ ] 主要な色の根拠がこのファイルにある
- [ ] 主要なタイポグラフィの根拠がこのファイルにある
- [ ] 主要コンポーネントの根拠がこのファイルにある
- [ ] レイアウトとレスポンシブの根拠がこのファイルにある
- [ ] 例外と未確認事項が `DESIGN.md` に混ざっていない
- [ ] 推測を断定として書いていない
