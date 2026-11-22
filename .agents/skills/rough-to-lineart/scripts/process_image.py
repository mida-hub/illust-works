#!/usr/bin/env python3
"""
rough-to-lineart スキル用の画像前処理・後処理スクリプト
- resize: ラフ画像を長辺指定サイズにリサイズ（トークン節約・高速化）
- transparent: 白背景の線画画像から白背景を除去し、黒線のみの透過PNGを出力
"""

import argparse
from pathlib import Path
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()


def init_project(project_dir: str) -> None:
    """作品ディレクトリと 1_raw / 2_work / 3_output サブディレクトリを作成する。"""
    base = Path(project_dir)
    for sub in ("1_raw", "2_work", "3_output"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    print(f"Initialized project structure at: {base}/ (1_raw, 2_work, 3_output)")


def resize_image(input_path: str, output_path: str, max_size: int = 1280) -> None:
    """画像をアスペクト比を維持したまま長辺 max_size 以下にリサイズする。"""
    img = Image.open(input_path)
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    print(f"Resized saved to: {output_path} ({img.size[0]}x{img.size[1]})")


def make_transparent(input_path: str, output_path: str, threshold: int = 220) -> None:
    """白背景の線画画像から背景を透過し、黒線のみの透過PNGを作成する。"""
    img = Image.open(input_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for r, g, b, a in datas:
        # 輝度を計算し、しきい値以上なら背景（完全透過）にする
        luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
        if luminance >= threshold:
            new_data.append((255, 255, 255, 0))
        else:
            # アンチエイリアスを活かすため、明るさに応じて不透明度を設定し色は黒に統一
            alpha = max(0, min(255, int((threshold - luminance) / threshold * 255 * 1.5)))
            new_data.append((0, 0, 0, alpha))

    img.putdata(new_data)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")
    print(f"Transparent PNG saved to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Rough-to-Lineart image processor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="Initialize project directory structure")
    p_init.add_argument("project_dir", help="Project directory path (e.g. 20260806_whale)")

    p_resize = subparsers.add_parser("resize", help="Resize rough image")
    p_resize.add_argument("input", help="Input image path")
    p_resize.add_argument("output", help="Output image path")
    p_resize.add_argument("--max-size", type=int, default=1280, help="Max edge length (default: 1280)")

    p_trans = subparsers.add_parser("transparent", help="Convert white background lineart to transparent PNG")
    p_trans.add_argument("input", help="Input lineart image path")
    p_trans.add_argument("output", help="Output transparent PNG path")
    p_trans.add_argument("--threshold", type=int, default=220, help="White threshold 0-255 (default: 220)")

    args = parser.parse_args()
    if args.command == "init":
        init_project(args.project_dir)
    elif args.command == "resize":
        resize_image(args.input, args.output, args.max_size)
    elif args.command == "transparent":
        make_transparent(args.input, args.output, args.threshold)


if __name__ == "__main__":
    main()
