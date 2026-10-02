#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from huggingface_hub import hf_hub_download


HF_DATASET = "rissin/nse-options-intraday"
NIFTY_OPTION_TEMPLATE = "upstox_intraday/NIFTY/NIFTY_{year}.parquet"
SPOT_BASE = "https://raw.githubusercontent.com/technovusin/nifty50-historical-data/main/nifty/1min"


def parse_years(value: str) -> list[int]:
    years = []
    for item in value.split(","):
        item = item.strip()
        if not item:
            continue
        year = int(item)
        if year < 2010 or year > 2100:
            raise ValueError(f"unsupported year: {year}")
        years.append(year)
    if not years:
        raise ValueError("at least one year is required")
    return sorted(set(years))


def download_option_year(year: int, out_dir: Path, token: str | None) -> Path:
    target = out_dir / "options" / f"NIFTY_{year}.parquet"
    target.parent.mkdir(parents=True, exist_ok=True)
    downloaded = hf_hub_download(
        repo_id=HF_DATASET,
        filename=NIFTY_OPTION_TEMPLATE.format(year=year),
        repo_type="dataset",
        token=token,
        local_dir=str(out_dir / "hf"),
    )
    source = Path(downloaded)
    if source.resolve() != target.resolve():
        target.write_bytes(source.read_bytes())
    return target


def download_url(url: str, target: Path) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={"User-Agent": "Final-Stand-v4-Phase11/1.0"})
    try:
        with urlopen(request, timeout=120) as response:
            target.write_bytes(response.read())
        return True
    except HTTPError as exc:
        if exc.code == 404:
            return False
        raise
    except URLError as exc:
        raise RuntimeError(f"download failed for {url}: {exc}") from exc


def download_spot_year(year: int, out_dir: Path) -> list[Path]:
    saved: list[Path] = []
    if year <= 2025:
        url = f"{SPOT_BASE}/{year}/NIFTY50_1min_{year}.csv"
        target = out_dir / "spot" / str(year) / f"NIFTY50_1min_{year}.csv"
        if download_url(url, target):
            saved.append(target)
        return saved

    for month in range(1, 13):
        suffix = f"{year}-{month:02d}"
        url = f"{SPOT_BASE}/{year}/NIFTY50_1min_{suffix}.csv"
        target = out_dir / "spot" / str(year) / f"NIFTY50_1min_{suffix}.csv"
        if download_url(url, target):
            saved.append(target)
    return saved


def write_spot_manifest(years: Iterable[int], out_dir: Path, files: list[Path]) -> Path:
    manifest = out_dir / "spot" / "source_manifest.txt"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "Phase 11 NIFTY spot source: technovusin/nifty50-historical-data",
        "Primary snapshot field: 1-minute 10:00 IST bar OPEN; expiry outcome: latest CLOSE on expiry date",
        "Source URL base: " + SPOT_BASE,
        "Missing monthly files are treated as unavailable rather than fabricated.",
        "Downloaded files:",
    ]
    lines.extend(str(path) for path in sorted(files))
    manifest.write_text("\n".join(lines) + "\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--years", required=True, help="Comma-separated years, e.g. 2024,2025")
    parser.add_argument("--output", default="data_cache/phase11")
    args = parser.parse_args()

    years = parse_years(args.years)
    out_dir = Path(args.output)
    token = os.getenv("HF_TOKEN")

    for year in years:
        path = download_option_year(year, out_dir, token)
        print(f"downloaded options: {year} -> {path}")

    spot_files: list[Path] = []
    for year in years:
        downloaded = download_spot_year(year, out_dir)
        spot_files.extend(downloaded)
        print(f"downloaded spot files: {year} -> {len(downloaded)}")

    manifest = write_spot_manifest(years, out_dir, spot_files)
    print(f"spot manifest: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())