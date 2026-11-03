#!/usr/bin/env python3
"""Download MLB draft picks from the MLB Stats API as CSV files."""

import argparse
from pathlib import Path
from typing import Optional, Sequence

import pandas as pd
import requests

API_URL = "https://statsapi.mlb.com/api/v1/draft/{year}"
REQUEST_TIMEOUT_SECONDS = 30


def fetch_draft(year: int, session: requests.Session) -> pd.DataFrame:
    """Fetch and normalize one year's draft picks."""
    response = session.get(
        API_URL.format(year=year),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError(f"The MLB Stats API returned invalid JSON for {year}.") from exc

    if not isinstance(payload, dict):
        raise ValueError(f"The MLB Stats API response for {year} was not an object.")

    drafts = payload.get("drafts")
    rounds = drafts.get("rounds") if isinstance(drafts, dict) else None
    if not isinstance(rounds, list) or not rounds:
        raise ValueError(f"The MLB Stats API response for {year} had no draft rounds.")

    for round_data in rounds:
        if (
            not isinstance(round_data, dict)
            or "round" not in round_data
            or not isinstance(round_data.get("picks"), list)
        ):
            raise ValueError(
                f"The MLB Stats API response for {year} had an unexpected round format."
            )

    if not any(round_data["picks"] for round_data in rounds):
        raise ValueError(f"The MLB Stats API response for {year} had no draft picks.")

    frame = pd.json_normalize(
        rounds,
        record_path="picks",
        meta=["round"],
        sep="_",
    )
    if "pickNumber" not in frame.columns:
        raise ValueError(
            f"The MLB Stats API response for {year} did not include pick numbers."
        )

    frame["pick"] = frame["pickNumber"]
    frame["year"] = year
    return frame


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download MLB draft pick data from the MLB Stats API."
    )
    parser.add_argument(
        "--start-year",
        required=True,
        type=int,
        help="First draft year to download (inclusive).",
    )
    parser.add_argument(
        "--end-year",
        required=True,
        type=int,
        help="Last draft year to download (inclusive).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data"),
        help="Directory for CSV files (default: ./data).",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.start_year < 1 or args.end_year < args.start_year:
        parser.error("--start-year and --end-year must be positive, and end must be >= start.")

    try:
        with requests.Session() as session:
            frames = [
                fetch_draft(year, session)
                for year in range(args.start_year, args.end_year + 1)
            ]

        args.output_dir.mkdir(parents=True, exist_ok=True)
        for year, frame in zip(range(args.start_year, args.end_year + 1), frames):
            frame.to_csv(args.output_dir / f"draft_{year}.csv", index=False)

        combined = pd.concat(frames, ignore_index=True, sort=False)
        combined_path = (
            args.output_dir / f"draft_{args.start_year}_{args.end_year}.csv"
        )
        combined.to_csv(combined_path, index=False)
    except (requests.RequestException, ValueError, OSError) as exc:
        parser.error(str(exc))

    print(
        f"Saved {len(frames)} yearly CSV file(s) and "
        f"{combined_path.name} to {args.output_dir}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
