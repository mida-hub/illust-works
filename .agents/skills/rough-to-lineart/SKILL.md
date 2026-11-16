---
name: rough-to-lineart
description: ラフ画像（手描き写真など）からコンセプトをヒアリングし、線入れ（清書）画像の生成・修正サイクルを回し、Tシャツプリント等に使用できる背景透過PNGを作成するワークフロー。
---

# Rough to Lineart Skill

手描きのラフイラスト（iPhone等で撮影した写真）をもとに、チャットでコンセプトや修正要望を対話しながら清書（線入れ）し、最終的に背景透過済みのクリーンなPNG画像を出力するためのスキルです。

## ディレクトリ構造ルール

作品ごとに `<YYYYMMDD_テーマ名>/` ディレクトリを作り、以下の3段階のフォルダ構成で管理します。

```text
<YYYYMMDD_テーマ名>/
├── 1_raw/      # ① ラフ（初期データ・一切加工しない）
├── 2_work/     # ② 加工・修正サイクル用（01_resized.jpg, 02_lineart_v1.jpg, v2...）
└── 3_output/   # ③ 最終成果物（背景透過PNG・Tシャツプリント用）
```

## ワークフロー

### Step 0: 作品ディレクトリの初期化
新しいイラストを始める際は、`scripts/process_image.py init` で `1_raw` / `2_work` / `3_output` を一括作成し、`1_raw/` にラフ画像を配置します。

```bash
uv run .agents/skills/rough-to-lineart/scripts/process_image.py init <YYYYMMDD_テーマ名>
```

### Step 1: 前処理（リサイズ・トークン節約）
`1_raw/` 内の元画像を直接編集せず、`scripts/process_image.py` を使って長辺 1280px 程度にリサイズした画像を `2_work/01_resized.jpg` に出力します。

```bash
uv run .agents/skills/rough-to-lineart/scripts/process_image.py resize <作品フォルダ>/1_raw/<ラフ画像> <作品フォルダ>/2_work/01_resized.jpg --max-size 1280
```

### Step 2: コンセプト確認と線入れ（清書）生成
ユーザーにコンセプト・用途（例：Tシャツプリント、線の太さ、残したいディテール、テイストなど）を確認し、`image-generator` サブエージェントを呼び出して `2_work/01_resized.jpg` から線入れ画像を生成します。生成した画像は `2_work/02_lineart_v1.jpg` として保存します。

**`image-generator` へのプロンプト指針：**
- 元ラフの構図、表情、主要なディテールを忠実に保つこと
- 背景は完全な純白（`#FFFFFF`）にし、紙の質感やグレーの影・塗りは一切入れないこと
- 線は黒一色（`#000000`）で、均一で滑らかなベクター風のきれいな主線（線画）にすること

### Step 3: 対話による修正サイクル
生成した線入れ画像を `read_file` で確認・ユーザーに提示し、「もう少し線を太く」「この模様を残して」などのフィードバックを受けて `image-generator` で再生成・微調整を繰り返します。修正版は `2_work/02_lineart_v2.jpg`, `v3`... と連番で保存し、過去案と比較できるようにします。

### Step 4: 後処理（背景透過PNG化）
線入れ画像が確定したら、`scripts/process_image.py` を使って白背景を透過（アルファチャンネル化）し、黒線のみのクリーンな PNG を `3_output/` に出力します。

```bash
uv run .agents/skills/rough-to-lineart/scripts/process_image.py transparent <作品フォルダ>/2_work/02_lineart_vN.jpg <作品フォルダ>/3_output/<テーマ名>_線画_透過.png --threshold 220
```
