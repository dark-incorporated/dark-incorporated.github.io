#!/usr/bin/env python3
"""Sync every crate's `docs/guide/*.md` into the book, and regenerate the crates block of SUMMARY.md.

    sync_crates.py --workspace DIR [--worktrees STATEDIR/wt] [--crates FILE] [--check]

The family registry is `<workspace>/.github/crates.json` (or `--crates FILE`). For each crate:

* with `--worktrees`, a `<worktrees>/<repo>` directory is the source: its files as they are on disk,
  pinned to its `HEAD`. Without one, or when the crate has none, the source is `<workspace>/<repo>` at
  `origin/main`, read from git objects: the book never depends on an unmerged branch or an
  uncommitted file of a clone;
* each guide page is copied to `src/crates/<repo>/guide/`, with its relative links rewritten to
  absolute ones pinned to the source's sha (links between guide pages stay relative);
* `src/crates/<repo>/.synced.json` records the sha and the hash of every written file, so `--check`
  can tell a hand-edited page from a synced one.

`--check` exits 1 when a synced file was edited by hand, a crate was never synced, or the recorded sha
is not the crate's `origin/main`. A crate directory missing from the workspace exits 1 with
`missing <repo>: clone it into <DIR>`.
"""

import argparse
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
SRC = BOOK / "src"
SUMMARY = SRC / "SUMMARY.md"
ORG = "dark-incorporated"
GUIDE_DIR = "docs/guide"
GUIDE_INDEX = "README.md"
SYNCED_FILE = ".synced.json"
CRATES_BEGIN = "<!-- crates:begin -->"
CRATES_END = "<!-- crates:end -->"
ORIGIN_MAIN = "origin/main"
BLOB_URL = f"https://github.com/{ORG}/{{repo}}/blob/{{sha}}/{{path}}"
RAW_URL = f"https://raw.githubusercontent.com/{ORG}/{{repo}}/{{sha}}/{{path}}"
FENCE_RE = re.compile(r"^\s*(```|~~~)")
LINK_RE = re.compile(r"(!?)\[((?:[^\[\]]|\[[^\]]*\])*)\]\(([^)\s]+)((?:\s+\"[^\"]*\")?)\)")
REFERENCE_RE = re.compile(r"^(\s*\[[^\]]+\]:\s*)(\S+)(.*)$")
IMG_TAG_RE = re.compile(r"(<img\s[^>]*?src=\")([^\"]+)(\")", re.IGNORECASE)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


class SyncError(Exception):
    pass


def git(directory: Path, *arguments: str) -> str:
    result = subprocess.run(["git", "-C", str(directory), *arguments], capture_output=True, text=True)
    if result.returncode != 0:
        raise SyncError(f"git {' '.join(arguments)} failed in {directory}: {result.stderr.strip()}")
    return result.stdout


class Source:
    """Where one crate's guide comes from: a worktree on disk, or `origin/main` of a clone."""

    def __init__(self, repo: str, directory: Path, from_worktree: bool) -> None:
        self.repo = repo
        self.directory = directory
        self.from_worktree = from_worktree
        self.sha = git(directory, "rev-parse", "HEAD" if from_worktree else ORIGIN_MAIN).strip()

    def pages(self) -> dict[str, str]:
        """Every `docs/guide/*.md` page's text, by file name."""
        pages: dict[str, str] = {}
        if self.from_worktree:
            guide = self.directory / GUIDE_DIR
            if guide.is_dir():
                for path in sorted(guide.glob("*.md")):
                    pages[path.name] = path.read_text()
            return pages
        listing = git(self.directory, "ls-tree", "--name-only", self.sha, f"{GUIDE_DIR}/")
        for line in listing.splitlines():
            if line.endswith(".md") and posixpath.dirname(line) == GUIDE_DIR:
                pages[posixpath.basename(line)] = git(self.directory, "show", f"{self.sha}:{line}")
        return pages


def locate(entry: dict, workspace: Path, worktrees: Path | None) -> Source:
    repo = entry["repo"]
    if worktrees is not None and (worktrees / repo).is_dir():
        return Source(repo, worktrees / repo, from_worktree=True)
    if not (workspace / repo).is_dir():
        raise SyncError(f"missing {repo}: clone it into {workspace}")
    return Source(repo, workspace / repo, from_worktree=False)


def rewrite_target(target: str, is_image: bool, repo: str, sha: str, siblings: set[str]) -> str:
    """One link target, pinned. Anchors, absolute URLs and links between guide pages are kept."""
    if target.startswith("#") or SCHEME_RE.match(target):
        return target
    path, _, rest = target.partition("#")
    path = path.split("?")[0]
    resolved = posixpath.normpath(posixpath.join(GUIDE_DIR, path))
    if resolved.startswith(".."):
        raise SyncError(f"{repo}: link {target!r} leaves the repository")
    if posixpath.dirname(resolved) == GUIDE_DIR and posixpath.basename(resolved) in siblings:
        return target
    template = RAW_URL if is_image else BLOB_URL
    url = template.format(repo=repo, sha=sha, path=resolved)
    return f"{url}#{rest}" if rest else url


def rewrite_text(text: str, repo: str, sha: str, siblings: set[str]) -> str:
    def convert(match: re.Match) -> str:
        bang, label, target, title = match.groups()
        label = LINK_RE.sub(convert, label)
        return f"{bang}[{label}]({rewrite_target(target, bang == '!', repo, sha, siblings)}{title})"

    out: list[str] = []
    fenced = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            out.append(line)
            continue
        if fenced:
            out.append(line)
            continue
        line = LINK_RE.sub(convert, line)
        line = IMG_TAG_RE.sub(
            lambda m: f"{m.group(1)}{rewrite_target(m.group(2), True, repo, sha, siblings)}{m.group(3)}", line
        )
        reference = REFERENCE_RE.match(line)
        if reference:
            head, target, tail = reference.groups()
            line = f"{head}{rewrite_target(target, False, repo, sha, siblings)}{tail}"
        out.append(line)
    return "\n".join(out) + "\n"


def ordered_pages(pages: dict[str, str]) -> list[tuple[str, str]]:
    """(file, title) in the order of the guide index's links, then the rest by name."""
    titles: dict[str, str] = {}
    order: list[str] = []
    index = pages.get(GUIDE_INDEX, "")
    for match in LINK_RE.finditer(index):
        bang, label, target, _title = match.groups()
        name = target.split("#")[0]
        if bang or name == GUIDE_INDEX or name not in pages or name in titles:
            continue
        titles[name] = label.strip().strip("`").strip()
        order.append(name)
    for name in sorted(pages):
        if name == GUIDE_INDEX or name in titles:
            continue
        first = next((line for line in pages[name].splitlines() if line.startswith("# ")), None)
        titles[name] = first[2:].strip().strip("`") if first else name.removesuffix(".md")
        order.append(name)
    return [(name, titles[name]) for name in order]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sync_crate(entry: dict, source: Source) -> list[tuple[str, str]]:
    repo = entry["repo"]
    crate_dir = SRC / "crates" / repo
    guide_dir = crate_dir / "guide"
    crate_dir.mkdir(parents=True, exist_ok=True)
    previous = {}
    synced_path = crate_dir / SYNCED_FILE
    if synced_path.is_file():
        previous = json.loads(synced_path.read_text()).get("files", {})

    pages = source.pages()
    listing = ordered_pages(pages)
    siblings = {name for name, _ in listing}
    header = f"<!-- synced from {ORG}/{repo}@{source.sha[:7]}; edit it there -->\n"
    written: dict[str, str] = {}
    for name, _title in listing:
        body = header + rewrite_text(pages[name], repo, source.sha, siblings)
        guide_dir.mkdir(parents=True, exist_ok=True)
        (guide_dir / name).write_text(body)
        written[name] = sha256(body)
    for stale in set(previous) - set(written):
        (guide_dir / stale).unlink(missing_ok=True)
    synced_path.write_text(json.dumps({"sha": source.sha, "files": written}, indent=1) + "\n")
    return listing


def summary_block(entries: list[dict], listings: dict[str, list[tuple[str, str]]]) -> str:
    lines: list[str] = []
    seen_parts: list[str] = []
    for entry in entries:
        if entry["part"] not in seen_parts:
            seen_parts.append(entry["part"])
    for part in seen_parts:
        lines += [f"# {part}", ""]
        for entry in entries:
            if entry["part"] != part:
                continue
            repo = entry["repo"]
            lines.append(f"- [{entry['title']}](crates/{repo}/index.md)")
            lines += [f"  - [{title}](crates/{repo}/guide/{name})" for name, title in listings[repo]]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_summary(block: str) -> None:
    text = SUMMARY.read_text()
    if CRATES_BEGIN not in text or CRATES_END not in text:
        raise SyncError(f"{SUMMARY} has no {CRATES_BEGIN} ... {CRATES_END} block")
    head, rest = text.split(CRATES_BEGIN, 1)
    _old, tail = rest.split(CRATES_END, 1)
    SUMMARY.write_text(f"{head}{CRATES_BEGIN}\n\n{block}\n{CRATES_END}{tail}")


def check(entries: list[dict], workspace: Path) -> list[str]:
    problems: list[str] = []
    for entry in entries:
        repo = entry["repo"]
        crate_dir = SRC / "crates" / repo
        synced_path = crate_dir / SYNCED_FILE
        if not synced_path.is_file():
            problems.append(f"{repo}: never synced ({synced_path} is missing)")
            continue
        record = json.loads(synced_path.read_text())
        for name, digest in record["files"].items():
            path = crate_dir / "guide" / name
            if not path.is_file():
                problems.append(f"{repo}: {path} is missing")
            elif sha256(path.read_text()) != digest:
                problems.append(f"{repo}: {path} was edited by hand; edit it in {ORG}/{repo}")
        if not (workspace / repo).is_dir():
            problems.append(f"missing {repo}: clone it into {workspace}")
            continue
        main = git(workspace / repo, "rev-parse", ORIGIN_MAIN).strip()
        if record["sha"] != main:
            problems.append(f"{repo}: synced at {record['sha'][:7]}, origin/main is {main[:7]}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workspace", required=True, metavar="DIR")
    parser.add_argument("--worktrees", metavar="DIR")
    parser.add_argument("--crates", metavar="FILE")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    worktrees = Path(args.worktrees).expanduser().resolve() if args.worktrees else None
    registry = Path(args.crates) if args.crates else workspace / ".github" / "crates.json"
    try:
        entries = json.loads(registry.read_text())
        if args.check:
            problems = check(entries, workspace)
            for problem in problems:
                print(problem, file=sys.stderr)
            return 1 if problems else 0
        listings: dict[str, list[tuple[str, str]]] = {}
        for entry in entries:
            source = locate(entry, workspace, worktrees)
            listings[entry["repo"]] = sync_crate(entry, source)
            print(f"{entry['repo']}: {len(listings[entry['repo']])} pages @ {source.sha[:7]}"
                  f"{' (worktree)' if source.from_worktree else ''}")
        write_summary(summary_block(entries, listings))
    except FileNotFoundError as error:
        print(f"{error.filename}: not found", file=sys.stderr)
        return 1
    except (SyncError, json.JSONDecodeError) as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
