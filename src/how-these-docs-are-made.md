# How these docs are made

Every crate's README, guide and pictures follow one rulebook, and one command keeps them true.

- [`DOCUMENTATION.md`](https://github.com/dark-incorporated/.github/blob/main/DOCUMENTATION.md) says which documents a crate has, how each is laid out, which checks measure them and what the reviewer looks for.
- [`STYLE.md`](https://github.com/dark-incorporated/.github/blob/main/STYLE.md) says what things are called, how the prose reads, and what the pictures look like: a gothic industrial machine cathedral meeting a neon night city, in 16 EGA colours.
- A crate's own `DOCUMENTATION.md` holds only that crate's facts, and links both guides.

## The command

[`/regenerate-docs`](https://github.com/dark-incorporated/dark-incorporated.github.io/blob/main/.omp/commands/regenerate-docs.md) is an agent command in this repository. It checks every crate against the rulebook, fixes only what a check measured as stale, retakes the pictures whose code changed, regenerates art whose inputs changed, rebuilds this book, and has the result reviewed by a model from a different family than the one that wrote it. It opens one pull request per repository and stops: a person reads the report, merges the pull requests, and only then publishes the book.

## What in this book is synced

The guide pages under each crate are copied from that crate's `docs/guide/` folder by `tools/sync_crates.py`, pinned to the crate's `main`. Edit them in the crate's repository, never here: the sync overwrites a page edited in the book, and `sync_crates.py --check` fails on it. The glossary is generated from the org's `names.json` by `tools/glossary.py`.
