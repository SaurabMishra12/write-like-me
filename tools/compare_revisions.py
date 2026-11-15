"""Compare exact preservation and descriptive metrics; leave voice preference to readers."""

import argparse
import difflib
import json
from pathlib import Path

from preservation_checker import check
from style_analyzer import analyze
from writing_auditor import audit


def compare(original, revised, genre="general", locks=None, minimal=False):
    return {"preservation": check(original, revised, locks=locks, minimal=minimal),
            "original_metrics": analyze(original), "revised_metrics": analyze(revised),
            "original_audit": audit(original, genre), "revised_audit": audit(revised, genre),
            "diff": "\n".join(difflib.unified_diff(original.splitlines(), revised.splitlines(), fromfile="original", tofile="revised", lineterm="")),
            "preferred_version": None, "preference_reason": "User/reader judgment required; surface metrics are not a voice or quality score."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original", type=Path)
    parser.add_argument("revised", type=Path)
    parser.add_argument("--genre", default="general")
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()
    print(json.dumps(compare(args.original.read_text(encoding="utf-8"), args.revised.read_text(encoding="utf-8"), args.genre, minimal=args.minimal), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
