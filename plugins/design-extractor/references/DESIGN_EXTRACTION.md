# DESIGN_EXTRACTION.md

既存アプリから `DESIGN.md` を作成するための手順書。

この手順の目的は、コードベースにすでに存在するデザイン判断を抽出し、再利用可能な言語に変換することである。新しいデザインを発明するのではなく、実装から一貫性、例外、暗黙のルールを読み取る。

## 1. Preparation

最初に以下を読む。

- `AGENTS.md`
- `DESIGN.md`
- `design-audit.md`
- 既存の `README`、開発ドキュメント、デザイン関連ドキュメント

次に、アプリの技術構成を把握する。

- フレームワーク
- スタイリング方式
- ルーティング構成
- 共通コンポーネントの場所
- アセットの場所
- Storybook やスクリーンショットの有無

## 2. Design File Inventory

以下を優先して探す。

### Tokens and Theme

- `tailwind.config.*`
- `theme.*`
- `tokens.*`
- `variables.css`
- `globals.css`
- `app.css`
- `index.css`
- Sass variables
- CSS custom properties
- design token JSON

見るポイント:

- 色
- フォント
- spacing
- radius
- shadow
- breakpoint
- z-index
- animation
- focus ring

### Components

- `Button`
- `Card`
- `Input`
- `Select`
- `Dialog`
- `Modal`
- `Toast`
- `Tooltip`
- `Tabs`
- `Navbar`
- `Sidebar`
- `Header`
- `Footer`
- `Table`
- `List`
- `EmptyState`

見るポイント:

- variant 名
- size 名
- state
- className の組み合わせ
- disabled / loading / error の扱い
- どのコンポーネントが基準になっているか

### Layout and Screens

- app shell
- dashboard
- landing / home
- auth
- settings
- detail page
- creation / edit flow
- checkout / payment
- onboarding
- error pages

見るポイント:

- 画面密度
- 主要アクションの位置
- セクション分割
- コンテナ幅
- グリッド
- ナビゲーション
- モバイル時の優先順位

### Assets

- logo
- icons
- illustrations
- product images
- background images
- favicon

見るポイント:

- 線幅
- 角丸
- 塗り / 線
- 写真かイラストか
- 抽象的か具体的か
- ブランド色との関係

## 3. Extraction Method

各観察を、以下の形に変換する。

```text
Observation:
<実装で見つけた事実>

Pattern:
<複数箇所に共通する使い方>

Design Rule:
<DESIGN.md に書けるルール>

Rationale:
<なぜそのルールがプロダクトに合っているか>

Evidence:
<ファイルパス、コンポーネント名、ページ名>
```

例:

```text
Observation:
Primary buttons use bg-blue-600, white text, 8px radius, and appear in form submit and onboarding start actions.

Pattern:
Blue is not decorative. It marks the highest-priority action.

Design Rule:
Use the accent blue only for primary actions, links, and focus states.

Rationale:
The rest of the app is neutral and data-heavy, so a single blue accent makes interaction targets reliable without visual noise.

Evidence:
components/Button.tsx, app/onboarding/page.tsx, app/settings/profile-form.tsx
```

## 4. Write `design-audit.md` First

`DESIGN.md` を書く前に、`design-audit.md` に調査結果を記録する。

必ず記録する項目:

- 調査対象ファイル
- 発見したトークン
- 主要コンポーネントの実装傾向
- 主要画面のレイアウト傾向
- 例外
- 推測
- 未確認事項

`design-audit.md` は作業ログであり、多少粗くてもよい。`DESIGN.md` は整理された最終判断だけを書く。

## 5. Compose `DESIGN.md`

`DESIGN.md` は以下の9セクションで書く。

1. Visual Theme & Atmosphere
2. Color Palette & Roles
3. Typography Rules
4. Component Styles
5. Layout Principles
6. Depth & Elevation
7. Do's & Don'ts
8. Responsive Behavior
9. Agent Prompt Guide

### Section Guidance

#### 1. Visual Theme & Atmosphere

コードから読み取れるブランドの態度を書く。

見るもの:

- 背景の使い方
- 情報密度
- 画像やアイコンの扱い
- 装飾の多さ
- 余白の取り方
- 文言やUIコピーの雰囲気

書くこと:

- このUIが何を重視しているか
- 何を避けているか
- なぜその雰囲気がプロダクトに合うか

#### 2. Color Palette & Roles

色を値ではなく役割として整理する。

書くこと:

- primary
- surface
- text
- muted text
- border
- accent
- success / warning / danger
- focus

注意:

- 似た色が複数ある場合は、使い分けを書く
- 使われていない色は主要パレットに入れない
- ブランドカラーと状態色を混同しない

#### 3. Typography Rules

フォント、サイズ、太さ、行間、階層を整理する。

書くこと:

- display / heading / body / caption / label / button
- どの画面で大きな見出しを使うか
- body text の標準サイズ
- テーブルやフォームの密度
- 英数字、コード、価格、メタ情報の扱い

注意:

- `font-size` の一覧だけにしない
- 情報階層と読みやすさの理由を書く

#### 4. Component Styles

共通部品を、見た目と使い方の両方で書く。

必須候補:

- Button
- Card
- Input
- Navigation
- Modal / Dialog
- Table / List

各コンポーネントで書くこと:

- variants
- sizes
- states
- 使う場面
- 使わない場面
- 優先度の表現方法

#### 5. Layout Principles

画面構成のルールを書く。

書くこと:

- spacing scale
- container width
- grid
- section rhythm
- form layout
- dashboard / list / detail の基本構成
- mobile の並び順

#### 6. Depth & Elevation

shadow、border、background差、overlay、z-index の意味を整理する。

書くこと:

- 基本はフラットか立体的か
- card は border か shadow か
- modal はどう前面化するか
- focus state はどう表すか
- hover で奥行きを変えるか

#### 7. Do's & Don'ts

実装者が迷いやすい境界線を書く。

Do:

- 既存UIに合う選択
- 繰り返し確認できたパターン
- 推奨される使い方

Don't:

- 既存UIと衝突する表現
- 例外を一般化したもの
- 平均的なAI UIに寄りやすい表現

#### 8. Responsive Behavior

ブレークポイントと変化のルールを書く。

見るもの:

- CSS breakpoint
- container query
- mobile nav
- grid collapse
- hidden / shown elements
- touch target
- table の扱い

書くこと:

- どの幅で何が変わるか
- 情報の優先順位
- モバイルで残す操作
- モバイルで隠す補助情報

#### 9. Agent Prompt Guide

AIに短く渡せる実装指示を書く。

含めること:

- 1文の雰囲気
- 主要色
- フォント
- component rules
- layout rules
- depth rules
- top don'ts

## 6. Handling Conflicts

### Multiple Design Systems

旧UIと新UIが混在している場合:

- 主要画面で使われている方を `DESIGN.md` の基準にする
- 旧UIは `design-audit.md` の `Legacy / Exceptions` に残す

### One-off Marketing Page

マーケティングページだけ大きく違う場合:

- プロダクトUIとは分けて書く
- `DESIGN.md` では `Marketing exceptions` として明記する

### Unused Components

未使用のコンポーネントは基準にしない。

判断できない場合は、`design-audit.md` に `Usage unknown` として残す。

### Framework Defaults

shadcn/ui、Material UI、Bootstrap などのデフォルト値が残っている場合:

- アプリ固有に調整されている箇所を優先する
- デフォルトのままなら、プロダクト固有の判断として過剰に語らない

## 7. Final Review

提出前に確認する。

- `DESIGN.md` は完成文書として読めるか
- `design-audit.md` は根拠ログとして読めるか
- 同じ内容を両方に重複して長く書いていないか
- 推測が断定に変わっていないか
- token / rule / rationale が揃っているか
- なぜそのデザインなのかが説明されているか
