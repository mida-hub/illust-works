# illust-works

手描きのラフイラスト（iPhone等で撮影した写真）から、チャットでコンセプトや修正要望を対話しながら線入れ（清書）を行い、Tシャツプリント等に使える背景透過PNGを作成するイラスト制作リポジトリです。

## ディレクトリ構造

```text
illust-works/
├── .agents/skills/rough-to-lineart/   # Antigravity 用スキル＆画像処理スクリプト
├── pyproject.toml                     # Python 依存管理（uv / Python 3.12）
└── <YYYYMMDD_テーマ名>/               # 作品ごとのディレクトリ
    ├── 1_raw/                         # ① ラフ（初期データ・一切加工しない）
    ├── 2_work/                        # ② 加工・修正サイクル用（リサイズ、線入れ v1, v2...）
    └── 3_output/                      # ③ 最終成果物（背景透過PNG）
```

## 環境

- Python 3.12（`uv` で管理）
- 依存パッケージ: `pillow`

## 基本的な使い方

### 1. 作品ディレクトリの作成
```bash
uv run .agents/skills/rough-to-lineart/scripts/process_image.py init <YYYYMMDD_テーマ名>
```

### 2. ラフ画像の配置
作成した `<YYYYMMDD_テーマ名>/1_raw/` にラフ画像を配置します。

### 3. 線入れ・修正・透過PNG化
Antigravity のチャットでラフ画像を指定し、コンセプトを伝えて線入れを依頼します（`rough-to-lineart` スキルが以下の流れで処理します）。

1. **リサイズ**: `2_work/01_resized.jpg` にリサイズ（トークン節約）
2. **線入れ・修正サイクル**: `2_work/02_lineart_v1.jpg`, `v2`... として対話しながら清書
3. **背景透過PNG化**: `3_output/<テーマ名>_線画_透過.png` を出力

### スクリプト単体での実行例

```bash
# リサイズ
uv run .agents/skills/rough-to-lineart/scripts/process_image.py resize <入力画像> <出力画像> --max-size 1280

# 背景透過PNG化
uv run .agents/skills/rough-to-lineart/scripts/process_image.py transparent <線入れ画像> <出力PNG> --threshold 220
```
