#!/usr/bin/env python3
"""Write `src/glossary.md` from the `canonical` table of the org's `names.json`.

    glossary.py [--names FILE]

The glossary is the only page that writes a former name, so a reader who arrives from an old link can
learn what the thing is called now. `names.json` is `<workspace>/.github/names.json`, where the
workspace is the directory holding this book's clone, unless `--names` says otherwise.
"""

import argparse
import json
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
GLOSSARY = BOOK / "src" / "glossary.md"
DEFAULT_NAMES = BOOK.parent / ".github" / "names.json"

INTRO = (
    "The names Dark Incorporated uses, and what each one was called before. "
    "This is the only page in the book that writes a former name."
)


def render(canonical: list[dict]) -> str:
    rows = []
    for item in canonical:
        formerly = "; ".join(item["formerly"]) if item["formerly"] else "-"
        rows.append(f"|{item['thing']}|{item['canonical']}|{formerly}|")
    return "\n".join(["# Glossary", "", INTRO, "", "|Thing|Canonical|Formerly|", "|---|---|---|", *rows, ""])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--names", default=str(DEFAULT_NAMES), metavar="FILE")
    args = parser.parse_args()
    try:
        names = json.loads(Path(args.names).read_text())
        GLOSSARY.write_text(render(names["canonical"]))
    except FileNotFoundError as error:
        print(f"{error.filename}: not found", file=sys.stderr)
        return 1
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"{args.names}: malformed ({error})", file=sys.stderr)
        return 1
    print(f"wrote {GLOSSARY}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
