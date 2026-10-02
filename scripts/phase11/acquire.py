#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Iterable

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


def write_spot_manifest(years: Iterable[int], out_dir: Path) -> Path:
    manifest = out_dir / "spot" / "source_manifest.txt"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "Phase 11 NIFTY spot source: technovusin/nifty50-historical-data",
        "Primary field: 1-minute NIFTY50 OHLC with timestamp",
        "Source URL base: " + SPOT_BASE,
        "NOTE: exact year file names are validated during acquisition; do not assume an unavailable year exists.",
        "",
    ]
    for year in years:
        lines.append(f"{year}: {SPOT_BASE}/{year}/")
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

    manifest = write_spot_manifest(years, out_dir)
    print(f"spot manifest: {manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
