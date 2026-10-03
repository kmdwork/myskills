# <Product Name> DESIGN.md

このファイルは、既存アプリの実装から抽出したデザイン判断基準である。

色、余白、フォント、コンポーネントの値だけではなく、それらがどこで使われ、なぜそのプロダクトに適しているのかを記述する。根拠、例外、未確認事項は `design-audit.md` に分離する。

## 1. Visual Theme & Atmosphere

`<既存アプリから読み取れる視覚テーマを文章で書く。単に「モダン」「ミニマル」と書かず、情報密度、余白、装飾、ブランドの態度、ユーザー体験との関係を説明する。>`

### Key Characteristics

- token: `<主要な視覚特徴>`
  - rule: `<どこで使われるか / どこで使うべきか>`
  - rationale: `<なぜこのプロダクトに合うか>`
- token: `<主要な視覚特徴>`
  - rule: `<どこで使われるか / どこで使うべきか>`
  - rationale: `<なぜこのプロダクトに合うか>`
- token: `<主要な視覚特徴>`
  - rule: `<どこで使われるか / どこで使うべきか>`
  - rationale: `<なぜこのプロダクトに合うか>`

## 2. Color Palette & Roles

### Core Colors

| Token | Value | Role | Rationale |
|------|-------|------|-----------|
| `<background>` | `<value>` | `<ページ背景>` | `<理由>` |
| `<surface>` | `<value>` | `<カード、パネル、入力背景>` | `<理由>` |
| `<text-primary>` | `<value>` | `<主要テキスト>` | `<理由>` |
| `<text-muted>` | `<value>` | `<補足、メタ情報、無効状態>` | `<理由>` |
| `<border>` | `<value>` | `<区切り、入力、カード境界>` | `<理由>` |

### Interactive & Semantic Colors

| Token | Value | Role | Rationale |
|------|-------|------|-----------|
| `<accent>` | `<value>` | `<主要操作、リンク、フォーカス>` | `<理由>` |
| `<success>` | `<value>` | `<成功、完了>` | `<理由>` |
| `<warning>` | `<value>` | `<注意、未完了>` | `<理由>` |
| `<danger>` | `<value>` | `<エラー、破壊的操作>` | `<理由>` |

### Color Rules

- `<アクセント色の使用条件>`
- `<背景色とsurfaceの使い分け>`
- `<状態色の使い方>`
- `<コントラスト上の制約>`

## 3. Typography Rules

### Font Families

- Display: `<font-family>`
- Body: `<font-family>`
- Mono: `<font-family, if used>`

### Type Scale

| Role | Size | Weight | Line Height | Letter Spacing | Use |
|------|------|--------|-------------|----------------|-----|
| Display | `<value>` | `<value>` | `<value>` | `<value>` | `<ヒーロー、最上位見出し>` |
| H1 | `<value>` | `<value>` | `<value>` | `<value>` | `<ページタイトル>` |
| H2 | `<value>` | `<value>` | `<value>` | `<value>` | `<セクション見出し>` |
| Body | `<value>` | `<value>` | `<value>` | `<value>` | `<本文、説明>` |
| Label | `<value>` | `<value>` | `<value>` | `<value>` | `<フォーム、設定項目>` |
| Caption | `<value>` | `<value>` | `<value>` | `<value>` | `<メタ情報、補足>` |
| Button | `<value>` | `<value>` | `<value>` | `<value>` | `<操作ラベル>` |

### Typography Principles

- token: `<例: restrained heading hierarchy>`
  - rule: `<サイズ、太さ、使う場所>`
  - rationale: `<情報構造にどう効くか>`
- token: `<例: dense but readable body copy>`
  - rule: `<行間、行長、密度>`
  - rationale: `<読みやすさや作業効率にどう効くか>`

## 4. Component Styles

### Buttons

#### Primary

- token: `<background, text, radius, padding, border, shadow>`
- rule: `<主要操作に使う。1画面内の使用上限や配置ルールを書く>`
- rationale: `<行動優先度をどう伝えるか>`
- states:
  - hover: `<value>`
  - active: `<value>`
  - focus: `<value>`
  - disabled: `<value>`

#### Secondary

- token: `<background, text, radius, padding, border, shadow>`
- rule: `<補助操作に使う条件>`
- rationale: `<Primaryとの差をどう作るか>`

#### Destructive

- token: `<background, text, radius, padding, border, shadow>`
- rule: `<削除、取消不能操作に使う条件>`
- rationale: `<危険操作をどう区別するか>`

### Cards & Containers

- token: `<background, border, radius, shadow, padding>`
- rule: `<カード化する情報 / カード化しない情報>`
- rationale: `<まとまり、比較、階層にどう効くか>`

### Inputs & Forms

- token: `<height, padding, border, background, focus, error>`
- rule: `<通常入力、検索、フィルター、エラー状態の使い分け>`
- rationale: `<入力可能性と状態をどう伝えるか>`

### Navigation

- token: `<height, background, typography, active, hover>`
- rule: `<グローバルナビ、サイドバー、タブ、パンくずの使い分け>`
- rationale: `<現在位置と主要導線をどう伝えるか>`

### Modals, Popovers, Tooltips

- token: `<surface, shadow, border, radius, scrim>`
- rule: `<一時的な操作、確認、補助情報の出し分け>`
- rationale: `<作業の中断度合いをどう表現するか>`

### Lists, Tables, Data Views

- token: `<row height, border, typography, hover, selected>`
- rule: `<一覧、比較、管理画面での使い分け>`
- rationale: `<スキャン性と密度をどう両立するか>`

## 5. Layout Principles

### Spacing System

- Base unit: `<value>`
- Scale: `<values>`
- rule: `<余白の選び方>`
- rationale: `<密度、可読性、操作性への影響>`

### Containers & Grid

- Page max width: `<value>`
- Content max width: `<value>`
- Grid: `<columns / gap>`
- Gutters: `<value>`

### Layout Rules

- `<ページ全体の構成>`
- `<主要アクションの配置>`
- `<フォーム、一覧、詳細画面の基本構成>`
- `<セクション間のリズム>`

### Radius Scale

| Token | Value | Use |
|------|-------|-----|
| Small | `<value>` | `<小さな部品>` |
| Medium | `<value>` | `<標準コンポーネント>` |
| Large | `<value>` | `<大きな面、モーダル、画像>` |
| Full | `<value>` | `<ピル、丸ボタン>` |

## 6. Depth & Elevation

| Level | Token | Treatment | Use | Rationale |
|-------|-------|-----------|-----|-----------|
| 0 | `<flat>` | `<value>` | `<通常面>` | `<理由>` |
| 1 | `<raised>` | `<value>` | `<カード、メニュー>` | `<理由>` |
| 2 | `<overlay>` | `<value>` | `<モーダル、ポップオーバー>` | `<理由>` |
| Focus | `<focus>` | `<value>` | `<キーボードフォーカス>` | `<理由>` |

### Depth Rules

- `<shadow を使う条件>`
- `<border を使う条件>`
- `<背景色差で階層を作る条件>`
- `<hover / active で奥行きを変えるか>`

## 7. Do's & Don'ts

### Do

- `<既存アプリで一貫している推奨ルール>`
- `<既存アプリで一貫している推奨ルール>`
- `<既存アプリで一貫している推奨ルール>`
- `<既存アプリで一貫している推奨ルール>`
- `<既存アプリで一貫している推奨ルール>`

### Don't

- `<既存アプリと衝突する表現>`
- `<既存アプリと衝突する表現>`
- `<既存アプリと衝突する表現>`
- `<既存アプリと衝突する表現>`
- `<既存アプリと衝突する表現>`

## 8. Responsive Behavior

### Breakpoints

| Name | Width | Behavior |
|------|-------|----------|
| Mobile | `<value>` | `<1カラム、ナビ、主要操作の扱い>` |
| Tablet | `<value>` | `<中間レイアウト>` |
| Desktop | `<value>` | `<標準レイアウト>` |
| Wide | `<value>` | `<最大幅、余白、情報量の扱い>` |

### Responsive Rules

- `<グリッドの変化>`
- `<ナビゲーションの変化>`
- `<見出しと本文サイズの変化>`
- `<テーブルや一覧の扱い>`
- `<タッチターゲットの最小サイズ>`

## 9. Agent Prompt Guide

### Quick Reference

- Theme: `<1文で視覚テーマ>`
- Primary background: `<token / value>`
- Primary surface: `<token / value>`
- Primary text: `<token / value>`
- Accent: `<token / value / 使用条件>`
- Font: `<display / body>`
- Radius: `<標準値>`
- Spacing: `<基準値>`
- Depth: `<shadow / border / surface の基本方針>`
- Avoid: `<最重要 Don't 3つ>`

### Implementation Prompt

```text
Build UI for <Product Name> using the existing design language:
- Visual atmosphere: <theme and attitude>.
- Color: use <core colors>; reserve <accent> for <interactive role>.
- Typography: use <font rules>; keep hierarchy consistent with <type scale>.
- Components: buttons, cards, inputs, navigation, and overlays should follow <component rules>.
- Layout: use <spacing scale>, <container width>, and <responsive behavior>.
- Depth: use <elevation rules>.
- Avoid: <top don'ts>.
```

### Review Checklist

- Does the screen match the existing visual atmosphere?
- Are colors used by role, not decoration?
- Is typography consistent with the extracted hierarchy?
- Do components follow existing variants and states?
- Does spacing follow the extracted scale?
- Is depth used only where it clarifies hierarchy?
- Are exceptions documented in `design-audit.md` instead of hidden in `DESIGN.md`?
- Does the mobile layout preserve the primary workflow?
