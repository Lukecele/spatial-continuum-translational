#!/usr/bin/env python3
"""Inspect a GEO spatial archive without extracting its full contents."""

import argparse
import json
import tarfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/derived/gse301973_archive_manifest.json"))
    args = parser.parse_args()

    with tarfile.open(args.archive, mode="r:gz") as archive:
        members = [
            {
                "name": member.name,
                "size_bytes": member.size,
                "type": "directory" if member.isdir() else "file",
            }
            for member in archive.getmembers()
        ]

    report = {
        "archive": str(args.archive),
        "member_count": len(members),
        "members": members,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("archive", "member_count")}, indent=2))


if __name__ == "__main__":
    main()
