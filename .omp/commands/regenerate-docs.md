---
description: Check every Dark Inc. crate against DOCUMENTATION.md, regenerate only what is measured stale (README, guide, media, art, book), have it reviewed by another model family, and stage PRs for the owner's sign-off.
argument-hint: "check | run [repo ...] | publish <run-id> | publish-book <run-id> | runners"
disable-model-invocation: true
---

# `/regenerate-docs`: the documentation pass

One run compares every Dark Incorporated crate against the org rulebook, fixes only what a check
measured as wrong, recaptures the media that went stale, regenerates the art whose inputs changed,
rebuilds the book, has the result reviewed by a model from another family, and stages a branch and a
PR per repository. **Nothing lands until the owner reads `REPORT.md` and says so.**

The rulebook is two files, and the higher layer wins:

- `.github/STYLE.md`: names, voice, the palette, the art motif and the art pipeline.
- `.github/DOCUMENTATION.md`: which documents exist, their structure, the checks (RC/DC/DR/MC), the
  review rubric (RV01–RV06), and regeneration.
- `<repo>/DOCUMENTATION.md`: only that repo's own facts, terms and recorded exceptions. It never
  restates an org rule.

Read both org guides before you touch anything: they are the spec this command enforces, and every
rule ID below means the rule with that ID in them.

## Run state

```
DI=$(dirname "$(git rev-parse --show-toplevel)")      # run this from the book repo's root
GH=$DI/.github
BOOK=$DI/dark-incorporated.github.io
CRATES=$GH/crates.json
PROMPT=$BOOK/tools/review_prompt.md     # the reviewer's instructions; one copy, in the book repo
RUN_ID=$(date -u +%Y%m%dT%H%MZ)
STATE=~/.local/state/dark-inc-docs/$RUN_ID
```

`$STATE` holds, and is the only place this command writes outside a git worktree:

```
$STATE/wt/<repo>            a worktree on branch docs/regenerate-<run-id>, from origin/main
$STATE/before/<repo>.json   one repo's checks before the run (joined into check-before.json)
$STATE/check-before.json    every check's result before the run
$STATE/check-after.json     every check's result after it
$STATE/json/                ad-hoc per-check JSON (check mode, and the re-check after the subagents)
$STATE/art/<job>/           cand-<k>.png and sheet.png per art job
$STATE/media/               stale-row capture attempts and their logs
$STATE/review/<repo>.json   the reviewer's JSON
$STATE/pr/<repo>.md         the PR body, cut from the report
$STATE/REPORT.md            the run's report
```

`$RUN_ID` is fixed for the whole run. Every worktree branch is `docs/regenerate-$RUN_ID`, and every PR
is titled `docs: regenerate ($RUN_ID)`.

`<repo>` always means a value of `repo` in `crates.json`. Read the list, never hard-code it:

```sh
jq -r '.[].repo' "$CRATES"
```

**Notation.** A word in angle brackets is a value you substitute as you execute a step, exactly as the
plan writes them: `<repo>` is the crate's directory name, `<run-id>` is `$RUN_ID`, `<k>` is a
candidate's index, `<demo>` is a retake name without `.gif`, `<file>` is a manifest row's file.
Nothing here is a template to be filled mechanically; every command that loops over several values
has its loop written out.

## Never do

- **Never force-push** in any form, and never rewrite a branch that was already pushed.
- **Never merge a PR.** The owner merges. `publish` opens them and stops.
- **Never substitute another model** for the reviewer. If `google/gemini-pro-latest` is unavailable,
  stop at the review phase and put the exact error in `REPORT.md`. There is no fallback model.
- **Never edit a test, a golden file, a fixture or a check to make a check pass.** A rule that does not
  fit the crate is a rule to change in the org guide, and that is the owner's call.
- **Never write outside `$STATE`** except inside a worktree, and never inside the shared clones at
  `$DI/<repo>` (they stay on `main`, untouched, so `publish-book` can fast-forward them).
- **Never rename inside `.github/art/archive/**`.** Those job files must still reproduce the images
  they made; `rename.py` skips them for exactly this reason.
- **Never move or rename a media file** a release already points at.
- **Never publish a repo whose compile gate failed**, and never publish a run whose report says the
  review did not run. `check` before a `run` is expected to fail; that failure is the work.
- **Never `git reset --hard`, `checkout --`, `clean` or `rebase`** a worktree you did not create in
  this run.

---

## Phase 0: preflight (every mode, before anything else)

Stop the run and name the missing piece on the first failure. Do not work around any of it.

1. **Every repo is cloned.** For each `repo` in `$CRATES`:

   ```sh
   test -d "$DI/$repo" || gh repo clone "dark-incorporated/$repo" "$DI/$repo"
   git -C "$DI/$repo" fetch origin
   ```

   Then `git -C "$DI/.github" fetch origin` and `git -C "$BOOK" fetch origin`.

2. **The infrastructure repos are present.** `$GH` and `$BOOK` exist, and the foundation_vs_slop clone
   is at `$HOME/foundation_vs_slop`:

   ```sh
   FVS=$HOME/foundation_vs_slop
   test -d "$GH" && test -d "$BOOK" && test -d "$FVS"
   ```

   `$FVS` is needed on a full run only (step 3b and `publish`). Name it in the report if it is missing
   on a single-repo run and skip step 3b.

3. **The tools exist.**

   ```sh
   for t in mdbook lychee ffmpeg ffprobe python3 gh jq rsync plutil; do command -v "$t" >/dev/null || echo "missing $t"; done
   python3 -c 'import PIL; print(PIL.__version__)'
   ```

   Pillow must be 11 or newer (the art and diagram scripts pin nothing else).

4. **The capture hosts answer.**

   ```sh
   ssh -n bmb true && ssh -n big true
   ```

   If `bmb` fails, the media phase (step 4) and the compile gate (step 5) cannot run: stop and say
   `bmb unreachable, so no capture and no compile gate`.

5. **The org repo is public**, because every crate's CI checks out `dark-incorporated/.github@main`.

   ```sh
   gh repo view dark-incorporated/.github --json visibility -q .visibility   # PUBLIC
   ```

6. **Retro Diffusion is reachable and funded** (only on `run`, and only when something is pending).

   ```sh
   test -r ~/.config/retrodiffusion/api_key && stat -f '%Lp' ~/.config/retrodiffusion/api_key   # 600
   ```

   A missing key stops the art phase with `no Retro Diffusion key at ~/.config/retrodiffusion/api_key`;
   it does not stop the rename, the READMEs or the book.

---

## Mode `check` (read-only)

Runs every check against the shared clones, prints one table, and writes nothing outside `$STATE`.
This is how the owner sees the drift before a run.

```sh
STATE=~/.local/state/dark-inc-docs/check-$(date -u +%Y%m%dT%H%MZ)
mkdir -p "$STATE/json"
```

For each `repo` in `$CRATES`:

| Check family | Command | Passes when |
|---|---|---|
| rename | `python3 $GH/tools/rename.py --repo $DI/<repo> --check` | exit 0 |
| README + repo doc | `python3 $GH/tools/readme_check.py --repo $DI/<repo> --json $STATE/json/<repo>-readme.json` | exit 0 |
| code references | `python3 $GH/tools/doc_refs_check.py --repo $DI/<repo> --json $STATE/json/<repo>-refs.json` | exit 0 |
| media | `python3 $GH/tools/media_check.py --repo $DI/<repo> --stale --json $STATE/json/<repo>-media.json` | exit 0 |

Then the two whole-org checks:

```sh
python3 $BOOK/tools/sync_crates.py --workspace "$DI" --check
python3 $GH/art/dark_inc_art.py plan --state "$STATE"
```

Count the failures from the JSON (`jq '[.checks[] | select(.ok | not)] | length'` for the two doc
checks; the number of `FAIL` lines for `rename.py` and `media_check.py`), and print:

```
repo                     rename  readme  refs  media  book  art
bevy_dark_factory        ok      3       0     2      -     pending
bevy_gooey               ok      1       0     0      -     pending
...
```

`book` is one row for the whole book repo, and `art` is one row for the whole art set (`pending` when
`plan` says any job's inputs changed). Print the grand total, then stop. `check` changes nothing.

---

## Mode `run [repo ...]` (default: every repo)

Nine steps, with two extra sub-steps (3b for the mirror list, 3c for the org repo's own generated
files). Do them in order; each one's output is the next one's input. The whole run is about 45 minutes
of agent time plus capture and compile wall-clock, so do not pad it.

The optional `[repo ...]` list narrows the run. `$ARGUMENTS` arrives as the whole argument line, so
drop the mode word first, then resolve the rest once; every per-crate loop below reads `$SEL`:

```sh
SEL=$(printf '%s' "${ARGUMENTS:-}" | sed 's/^run[[:space:]]*//')
SEL=${SEL:-$(jq -r '.[].repo' "$CRATES")}
for r in $SEL; do
  jq -e --arg r "$r" 'map(select(.repo == $r)) | length == 1' "$CRATES" >/dev/null \
    || { echo "$r is not in crates.json"; exit 1; }
done
```

A named repo that is not in `crates.json` stops the run: the registry is the only list. `.github` and
the book are always worktreed; `foundation_vs_slop` only on a full run (`$SEL` equal to every repo).

### Step 1: worktrees, and the "before" snapshot

Create one worktree per selected repo from `origin/main`, plus the two infrastructure repos, plus
`foundation_vs_slop` on a full run:

```sh
mkdir -p "$STATE/wt" "$STATE/json"
for r in $SEL; do
  git -C "$DI/$r" worktree add "$STATE/wt/$r" -b "docs/regenerate-$RUN_ID" origin/main
done
git -C "$GH"   worktree add "$STATE/wt/.github" -b "docs/regenerate-$RUN_ID" origin/main
git -C "$BOOK" worktree add "$STATE/wt/dark-incorporated.github.io" -b "docs/regenerate-$RUN_ID" origin/main
# full run only:
git -C "$FVS"  worktree add "$STATE/wt/foundation_vs_slop" -b "docs/regenerate-$RUN_ID" origin/main
```

If a worktree path already exists (a resumed run), `worktree add` fails; stop and name it rather than
deleting anything.

Set the worktree paths once:

```sh
GHW=$STATE/wt/.github
BOOKW=$STATE/wt/dark-incorporated.github.io
```

Run every check from the `check` table against `$STATE/wt/<repo>`, one per-repo JSON each, then join
them into `$STATE/check-before.json`:

```sh
mkdir -p "$STATE/before"
for r in $SEL; do
  python3 "$GHW/tools/rename.py" --repo "$STATE/wt/$r" --check > "$STATE/before/$r-rename.txt" 2>&1 || true
  python3 "$GHW/tools/readme_check.py"  --repo "$STATE/wt/$r" --json "$STATE/before/$r-readme.json"  >/dev/null || true
  python3 "$GHW/tools/doc_refs_check.py" --repo "$STATE/wt/$r" --json "$STATE/before/$r-refs.json"   >/dev/null || true
  python3 "$GHW/tools/media_check.py"   --repo "$STATE/wt/$r" --stale --json "$STATE/before/$r-media.json" >/dev/null || true
  jq -n --arg r "$r" \
    --rawfile rename "$STATE/before/$r-rename.txt" \
    --slurpfile readme "$STATE/before/$r-readme.json" \
    --slurpfile refs "$STATE/before/$r-refs.json" \
    --slurpfile media "$STATE/before/$r-media.json" \
    '{repo: $r,
      rename: ($rename | split("\n") | map(select(startswith("FORBIDDEN")))),
      readme: [$readme[0].checks[] | select(.ok | not)],
      refs:   [$refs[0].checks[]   | select(.ok | not)],
      media:  [$media[0].checks[]  | select(.ok | not)]}' > "$STATE/before/$r.json"
done
jq -s --arg run_id "$RUN_ID" '{run_id: $run_id, repos: map({(.repo): del(.repo)}) | add}' \
  "$STATE"/before/*.json > "$STATE/check-before.json"
```

Each check exits 1 when it has a failure, so the loop keeps going (`|| true`) and reads the `--json`
file instead of the exit code. The `FORBIDDEN` lines stay verbatim: step 3's brief embeds them.

### Step 2: rename

```sh
for r in $SEL; do
  python3 "$GH/tools/rename.py" --repo "$STATE/wt/$r"
done
python3 "$GH/tools/rename.py" --repo "$BOOKW"
python3 "$GH/tools/rename.py" --repo "$GHW"
[ -d "$STATE/wt/foundation_vs_slop" ] && python3 "$GH/tools/rename.py" --repo "$STATE/wt/foundation_vs_slop"
```

`git mv` for the path renames, then the basenames, the identifiers, the ordered text pairs and the
post-fixes, all per `names.json`. The tool itself skips `art/archive/**`, `*.plist.in`, `Cargo.lock`,
`*.lock`, `target/`, and the three files that quote old names on purpose: `names.json` (the
dictionary), `src/glossary.md` (generated from it) and `tools/rename.py`.

A non-zero exit is either `COLLISION <old> -> <new>` (exit 3, nothing changed in that worktree) or a
malformed `names.json`. On a collision: **abandon that repo for this run**, put the exact line in
`REPORT.md` under "unresolved", and go on with the others. Do not resolve it by hand.

Then refresh every Rust worktree's `Cargo.lock`, because renamed git-dependency URLs change it:

```sh
export CARGO_TARGET_DIR=$HOME/.cargo-target-shared/global
for r in $SEL; do
  ( cd "$STATE/wt/$r" && cargo metadata --format-version 1 >/dev/null )
done
```

A repo that fails `cargo metadata` after the rename is reported and excluded from publish; it is not
"fixed" by editing the lock by hand.

### Step 3: per-crate fixes, one `task` subagent per crate, in parallel

Spawn one subagent per selected crate in a single `task` batch, with `agent: "task"`. Each owns
**only** `$STATE/wt/<repo>` and `$STATE/wt/dark-incorporated.github.io/src/crates/<repo>/index.md`.
Shared edits have one owner: no subagent touches another's worktree or the book's `SUMMARY.md`.

Give each subagent the brief below verbatim, with its own repo substituted, and paste its failing
check lines (from `check-before.json`) into the slot. The brief is the whole of what the subagent does;
it builds, tests and commits nothing — steps 5 and `publish` do those.

````text
You are regenerating the documentation of <repo>, one crate of Dark Incorporated's Bevy family.

# Read first
- $GHW/STYLE.md    (names, voice, palette, art)
- $GHW/DOCUMENTATION.md (structure, checks, rubric)
- $STATE/wt/<repo>/README.md, its docs/ and its DOCUMENTATION.md if present
- $STATE/wt/dark-incorporated.github.io/src/crates/<repo>/index.md (the existing chapter, if any)

The rulebook's higher layer wins: STYLE.md over DOCUMENTATION.md, and both over the repo's own
DOCUMENTATION.md.

# Files you own (change nothing else)
- $STATE/wt/<repo>/**  except .github/art/archive/**
- for bevy_dark_factory only, also crates/bevy_dark_factory/macos/Info.plist.in (step 10; rename.py
  skips every *.plist.in, so this is a hand edit)
- $STATE/wt/dark-incorporated.github.io/src/crates/<repo>/index.md

# The check failures you are fixing, verbatim
<the repo's FAIL lines from check-before.json: rename, RCxx, DCxx, DR01, MCxx>

# Do, in this order
1. Reshape README.md to pass RC01–RC21 in DOCUMENTATION.md, keeping its 14-part order and every
   existing fact. Anything over the 250-line cap (RC16) moves **verbatim** to a page under docs/guide/
   (slug from its heading), gets a row in docs/guide/README.md, and gets a link from the README. Never
   delete content. bevy_elements, isomesh, bevy_light_grid and bevy_devshot need this move; for
   bevy_light_grid and bevy_devshot drop the old "read-only mirror" note, because the
   dark-incorporated repo is now the source of truth.
2. Create docs/guide/README.md if missing: a table `| Page | What is in it |`, one row per page, and
   every page follows the guide rules (task-first H1, a lead saying what the reader gets, numbered
   copy-paste steps, `## If it goes wrong` naming the real error text).
3. Fix every DR01 stale reference: for each identifier the check named, `rg -w -t rust '<segment>'`
   the repo, substitute the current identifier, or delete the clause that named it. Do not invent an
   API.
4. Normalise docs/media/README.md to the canonical five columns
   `| File | Command | Captured | Watches | Shows |`. Fill Watches with the example file plus the
   `src/` globs whose items the example uses; use `-` only for art copied from .github/art/. Leave the
   `Captured` day and sha as they are — the capture phase rewrites them.
5. Add the RC19 README doctest hook if it is missing: under `#[cfg(doctest)]` in a workspace member's
   src/lib.rs (or a tests/*.rs), `#[doc = include_str!("../README.md")] struct ReadmeDoctests;`.
6. Add the `readme` job to .github/workflows/ci.yml, exactly:
       readme:
         name: README rules
         uses: dark-incorporated/.github/.github/workflows/readme-check.yml@main
7. Run `python3 $GHW/tools/repo_doc.py --repo $STATE/wt/<repo>` to create or refresh the root
   DOCUMENTATION.md. Then fill `## Terms used here` with every term the README or a guide page defines
   that is specific to this crate: one clause each, at most 8 terms, `None.` if there are none. Fill
   `## Recorded exceptions` only with a deviation the checks allow but a reader would trip on (for
   example bevy_society's two extra H2s), in the form `<rule ID>: <what differs>, because <why>`, and
   `None.` if there is nothing. Never edit the block between the `dark-inc:generated` markers by hand.
8. In every agent file present (AGENTS.md, CLAUDE.md): replace any line matching
   `follow https://github.com/.*/DOCUMENTATION.md` with this exact line, and if no such line exists
   append it at the end. Change nothing else in those files.
   Documentation follows ./DOCUMENTATION.md, which defers to Dark Inc.'s DOCUMENTATION.md and STYLE.md; a feature is not done until its README line and, if it is visible, its GIF exist.
9. Write the book chapter $STATE/wt/dark-incorporated.github.io/src/crates/<repo>/index.md in the
   template: header image (src/media/chapters/<repo>.png, alt text describing it), the README pitch,
   then `## Add it`, `## What it gives you`, `## Use it in the Dark Factory`, `## Guide` (links to the
   synced pages under guide/) and `## Links`.
10. bevy_dark_factory only — the macOS bundle rename (this file is skipped by rename.py, so it is a
    hand edit): in crates/bevy_dark_factory/macos/Info.plist.in set CFBundleName and
    CFBundleDisplayName to `DarkFactory`, CFBundleIdentifier to `org.dark-incorporated.dark-factory`,
    and CFBundleIconFile to `DarkFactory` (that is the `DarkFactory.icns`
    tools/release/macos/build_app.sh already copies; the old value named an icon that does not exist).
    Leave update.rs's `APP = "DarkFactory.app"` alone, so the updater keeps working. Verify:
        sed 's/@VERSION@/0.0.0/g' crates/bevy_dark_factory/macos/Info.plist.in | plutil -lint -
        sed 's/@VERSION@/0.0.0/g' crates/bevy_dark_factory/macos/Info.plist.in | plutil -extract CFBundleIconFile raw -
    The first prints OK, the second prints DarkFactory.

# Do not
- Do not run cargo build, test, clippy or any example. The compile gate runs later, on another host.
- Do not commit, push, or open a PR.
- Do not touch another repo's worktree, the book's SUMMARY.md, or any file outside the paths above.
- Do not use a former name anywhere except in the generated glossary; run
  `python3 $GHW/tools/rename.py --repo $STATE/wt/<repo> --check` at the end and get exit 0.
- Do not add an emoji, and do not write prose in an in-world voice. Plain technical English, British
  spellings (`colour`, `licence`), as STYLE.md says.

# Finish with
The list of files you changed, and the output of `readme_check.py`, `doc_refs_check.py` and
`media_check.py` (non-stale) on your worktree. Do not judge it a pass if a check still fails; say so.
````

Run the same three checks yourself after all subagents return; a subagent's own output is a claim,
not a measurement:

```sh
for r in $SEL; do
  python3 "$GHW/tools/readme_check.py" --repo "$STATE/wt/$r" --json "$STATE/json/$r-readme-after-subagents.json"
done
```

A repo still failing goes back to its subagent once, with the new `FAIL` lines. A second failure is
reported and excluded from publish.

### Step 3b: foundation_vs_slop (full run only)

The five crates that were mirrors are now their own source of truth, so this one PR takes them off the
mirror list. In `$STATE/wt/foundation_vs_slop/scripts/mirror_crates.sh`:

1. Set `ORG=dark-incorporated` and update the comment above it (it says mirrors live in the old org;
   they no longer do).
2. Remove `bevy_orca`, `bevy_devshot`, `bevy_stigmergy`, `bevy_light_grid` and `bevy_speech_bubbles`
   from the `CRATES=( … )` array, each **replaced in place** by one comment line in the file's existing
   style:

   ```
   # <name> left on 2026-11-21: dark-incorporated/<name> is its own source of truth (its mirror carries releases and merges made there).
   ```

3. Change nothing else: not `LADVIEN_CRATES`, not `PUBLIC_CRATES`, not the fast-forward-only push, not
   the header comment about `--force`.

Verify the file still parses before it leaves the phase:

```sh
bash -n "$STATE/wt/foundation_vs_slop/scripts/mirror_crates.sh"
grep -c 'its own source of truth' "$STATE/wt/foundation_vs_slop/scripts/mirror_crates.sh"   # 7: the 5 new lines plus the 2 already there
grep -n 'ORG=' "$STATE/wt/foundation_vs_slop/scripts/mirror_crates.sh"                      # ORG=dark-incorporated
```

Do not run the script. It pushes; `publish` opens its PR instead.

### Step 3c: the org repo's own files

The `.github` worktree was renamed in step 2, and two of its files are generated rather than written:

```sh
( cd "$GHW" && python3 tools/profile_table.py )
```

`profile_table.py` rewrites the text between `<!-- family:begin -->` and `<!-- family:end -->` in
`profile/README.md` from `crates.json`: Part, Crate (linked), What it does, Latest (`git only` for an
unpublished crate), Docs. The family table is never hand-edited, so this is the only edit it gets.

Then check the org guides survived the rename intact:

```sh
test -f "$GHW/DOCUMENTATION.md" && test -f "$GHW/STYLE.md"
grep -c 'dark-inc:generated' "$GHW/templates/REPO_DOCUMENTATION.md"   # 2, one begin and one end
python3 "$GHW/tools/rename.py" --repo "$GHW" --check                 # exit 0
```

`DOCUMENTATION.md` and `STYLE.md` are owned by hand in the org repo; this command never rewrites them,
it enforces them.

### Step 4: media capture

Ask which rows are stale:

```sh
mkdir -p "$STATE/media"
for r in $SEL; do
  python3 "$GHW/tools/media_check.py" --repo "$STATE/wt/$r" \
    --stale --stale-json "$STATE/media/$r-stale.json"
done
```

Each stale row is `{file, command, watches}`. For each one, **the repo's own `capture_host` from
`crates.json`** decides the host. `bmb` for all but `bevy_dark_factory`, whose standing demos run on
`big`.

A row whose `Watches` is `-` is art copied from `.github/art/`, which code changes never make stale:
it never comes back stale, so it is never captured here. The two diagram rows are the exception
described under "Local diagrams" below.

**On `bmb`** (default):

```sh
rsync -a --delete --exclude .git --exclude target \
  "$STATE/wt/<repo>/" "bmb:~/dark-incorporated/.docs-capture/<repo>/"
ssh bmb 'zsh -lc "cd ~/dark-incorporated/.docs-capture/<repo> && export CARGO_TARGET_DIR=\$HOME/.cargo-target-shared/global && <the row'"'"'s command>"'
rsync -a "bmb:~/dark-incorporated/.docs-capture/<repo>/docs/media/<file>" "$STATE/wt/<repo>/docs/media/<file>"
```

Run the row's command exactly as the manifest writes it, under `zsh -lc` (bmb's login shell loads the
Rust toolchain), with the shared `CARGO_TARGET_DIR`. Record the whole output under
`$STATE/media/<repo>/<file>.log`.

**On `big`, for bevy_dark_factory's eight standing demos.** `tools/demo/retake.sh` refuses `:0`; it
needs a private Xvfb, so:

```sh
ssh big 'pgrep -f "Xvfb :96" >/dev/null || (Xvfb :96 -screen 0 1280x720x24 >/tmp/xvfb96.log 2>&1 &) ; sleep 2'
```

Sync the worktree there, build the two binaries the script requires from that worktree, and run it
with the demo's name in `ONLY` (names are the retake header's, without `.gif`):

```sh
rsync -a --delete --exclude .git --exclude target \
  "$STATE/wt/bevy_dark_factory/" "big:~/dark-incorporated/.docs-capture/bevy_dark_factory/"
ssh big 'zsh -lc "cd ~/dark-incorporated/.docs-capture/bevy_dark_factory && export CARGO_TARGET_DIR=\$HOME/.cargo-target-shared/global && cargo build --release -p bevy_dark_factory -p dark_factory_mcp"'
ssh big 'zsh -lc "cd ~/dark-incorporated/.docs-capture/bevy_dark_factory && \
  export CARGO_TARGET_DIR=\$HOME/.cargo-target-shared/global && \
  DISPLAY=:96 \
  EDITOR_BIN=\$CARGO_TARGET_DIR/release/bevy_dark_factory \
  MCP_BIN=\$CARGO_TARGET_DIR/release/dark_factory_mcp \
  WORK=/tmp/retake-<demo> ONLY=<demo> tools/demo/retake.sh"'
```

The two binaries land in `$CARGO_TARGET_DIR/release/`, not the worktree's `target/`, because the
shared target directory is exported for the build.

`retake.sh` writes `WORK/<demo>.gif` and a contact sheet per take, ending with `ALLDONE` in
`summary.txt`. One `ONLY=<demo>` per stale row. Read `summary.txt`: a take that failed all four times
says `NOT RECORDED`, and the row is a capture failure. Copy back only a recorded GIF, and look at the
sheet: the script's own check is necessary, not sufficient.

```sh
rsync -a "big:/tmp/retake-<demo>/<demo>.gif" "$STATE/wt/bevy_dark_factory/docs/media/<file>"
```

**Local diagrams.** The two crates with no visual output take a scripted still, never a capture:

```sh
python3 "$GHW/art/diagrams.py" devshot   --out "$STATE/wt/bevy_devshot/docs/media/hero.png"
python3 "$GHW/art/diagrams.py" light_grid --out "$STATE/wt/bevy_light_grid/docs/media/hero.png"
```

(The README caption for each says "schematic"; that is what makes a diagram honest.)

**After a successful capture**, set the row's `Captured` to `<UTC date> <worktree HEAD sha7>`:

```sh
printf '%s %s\n' "$(date -u +%Y-%m-%d)" "$(git -C "$STATE/wt/<repo>" rev-parse --short=7 HEAD)"
```

**Capture-failed policy.** A command that exits non-zero, or leaves no file, keeps the old media, is
listed as `capture-failed` for that row, and is retried **once** — never twice. If every row on a host
fails with a window or display error, keep the old media everywhere, write "bmb cannot open windows
over ssh; captures need the owner's session" (or the same for big) into `REPORT.md`, and go on. Do not
switch hosts.

### Step 5: compile gate, on `bmb`, serially

Only for Rust worktrees the rename or the subagents changed. One at a time, so two Bevy builds do not
fight over the shared target directory:

```sh
rsync -a --delete --exclude .git "$STATE/wt/<repo>/" "bmb:~/dark-incorporated/.docs-gate/<repo>/"
ssh bmb 'zsh -lc "cd ~/dark-incorporated/.docs-gate/<repo> && \
  export CARGO_TARGET_DIR=\$HOME/.cargo-target-shared/global && \
  cargo test --doc --all-features && cargo build --examples"'
```

A failure goes back to that crate's subagent **once**, with the error text, and the subagent fixes only
that. A second failure is reported, and the repo is excluded from publish. Do not weaken a test, and do
not add `#![allow(...)]` to get past it.

Save each repo's log under `$STATE/media/<repo>/gate.log`.

### Step 6: art

Run from the `.github` worktree, so `lock.json` and `art/chapters/*` land in the branch that ships them:

```sh
python3 "$GHW/art/dark_inc_art.py" plan --state "$STATE"
python3 "$GHW/art/dark_inc_art.py" cost --state "$STATE" --budget-usd 5
```

`cost` sums the free `check_cost` over every pending candidate. It exits 4 with
`over budget: $X > $5.00` above the cap — stop the art phase there, keep the art that already exists,
and put the figure in the report. Nothing has been charged when `cost` runs.

```sh
python3 "$GHW/art/dark_inc_art.py" run --state "$STATE" --only anchor --budget-usd 5
python3 "$GHW/art/dark_inc_art.py" sheet --state "$STATE"
# score anchor's sheet, pick anchor K, then:
python3 "$GHW/art/dark_inc_art.py" pick anchor <k> --state "$STATE"
python3 "$GHW/art/dark_inc_art.py" run --state "$STATE" --budget-usd 5
python3 "$GHW/art/dark_inc_art.py" sheet --state "$STATE"
```

`anchor` is generated and picked **before** the rest, because every other job sends it as its
reference image; `run` refuses to start the others while the anchor is unpicked. Each `run` writes
candidates to `$STATE/art/<id>/cand-<k>.png` and, beside each, `cand-<k>.json` with `palette_ok`,
`palette_note`, `cost_usd` and `seed`, measured on the native-size image.

**Score and pick with the reviewer.** For each job, send its sheet and the measured palette result to
`google/gemini-pro-latest` in the art-scoring mode of `$PROMPT`. Score `e` comes from the measurement,
never from the model:

```sh
for f in "$STATE"/art/<id>/cand-*.json; do
  jq -r '"\(input_filename | split("/")[-1] | sub("cand-"; "") | sub(".json"; "")): \(if .palette_ok then "palette ok" else "palette_fail" end) - \(.palette_note)"' "$f"
done
```

```sh
mkdir -p "$STATE/review"
omp -p --no-session --model google/gemini-pro-latest --tools read --max-cost 1 \
  "@$PROMPT" "@$STATE/art/<id>/sheet.png" \
  "Art scoring mode. Job <id>, palette subset <subset>. Measured colours per candidate: <the lines above>."
```

The reply is `{"id": "<id>", "scores": [{"k": 0, "a": 2, "b": 1, "c": 2, "d": 2, "e": 2}, ...]}`.
Take the highest `a+b+c+d+e`; break a tie on the lowest `k`; never pick a `palette_fail` candidate. Save
each reply to `$STATE/review/art-<id>.json`, then:

```sh
python3 "$GHW/art/dark_inc_art.py" pick <id> <k> --state "$STATE"
```

`pick` writes `art/lock.json` and scales the winner by NEAREST to the job's `out`. Then copy the picked
chapter art into the book worktree:

```sh
mkdir -p "$BOOKW/src/media/chapters"
for r in $SEL; do
  cp "$GHW/art/chapters/$r.png" "$BOOKW/src/media/chapters/$r.png"
done
```

The avatar and banner jobs also write `profile/avatar.png` and `profile/banner.png`; those land in
`$GHW`, which is the branch `publish` opens for the org repo.

If `cost` refused, or the key is missing, the art phase is skipped and the report says which jobs kept
their old image and why. A skipped art phase does not block the READMEs, the book or publish.

### Step 7: the book

From `$BOOKW`:

```sh
python3 "$BOOKW/tools/sync_crates.py" --workspace "$DI" --worktrees "$STATE/wt"
python3 "$BOOKW/tools/glossary.py"
mdbook build
lychee --offline --root-dir "$PWD/book" book/
```

`sync_crates.py` copies each crate's `docs/guide/*.md` into `src/crates/<repo>/guide/`, rewrites
relative repo-file links to blob URLs at the crate's sha, prepends the synced-from comment, writes
`.synced.json`, and regenerates the `<!-- crates:begin -->` block in `SUMMARY.md` (parts as headings,
each crate's `index.md`, then its pages in the order of its guide index table). A crate missing from
the workspace makes it exit 1 with `missing <repo>: clone it into <DIR>`; that is a preflight failure,
not something to work around.

`glossary.py` regenerates `src/glossary.md` from `names.json` `canonical` — the one place former names
are allowed to appear. `mdbook build` and `lychee --offline --root-dir "$PWD/book" book/` must both be green; a broken link is
fixed in the source page or its synced copy, never by deleting the link.

### Step 8: review, by another model family

For each repo whose worktree changed:

```sh
BOOKW=$STATE/wt/dark-incorporated.github.io
mkdir -p "$STATE/review"
for r in $SEL; do
  [ -n "$(git -C "$STATE/wt/$r" status --porcelain)" ] || continue   # unchanged, nothing to review
  args=("@$PROMPT")
  chapter="$BOOKW/src/crates/$r/index.md"
  [ -f "$chapter" ] && args+=("@$chapter")
  for id in $(jq -r '.[].id' "$GHW/art/jobs.json"); do
    [ "$id" = anchor ] && continue
    [ -f "$STATE/art/$id/sheet.png" ] && args+=("@$STATE/art/$id/sheet.png")
  done
  omp -p --no-session --model google/gemini-pro-latest --tools read --max-cost 1 \
    --cwd "$STATE/wt/$r" "${args[@]}" \
    "Docs review mode. Repo $r. Judge README.md, docs/guide/*.md and the chapter above. Measured checks RC01-RC21, DC01-DC05, DR01, MC01-MC05 and the rename check already pass; judge only RV01-RV06." \
    > "$STATE/review/$r.json" 2> "$STATE/review/$r.err"
done
```

The chapter path is passed only if the subagent wrote one, and only that job's sheets are passed:
nothing is handed to the reviewer that does not exist.

`$PROMPT` is `$BOOK/tools/review_prompt.md`, read from the clone rather than the worktree, because the
worktree is on a fresh branch and the prompt may not have merged yet.

Save stdout to `$STATE/review/<repo>.json`. It must parse as
`{repo, items:[{rule, verdict, file, line, why}]}` with six items, RV01–RV06. A reply that is not that
JSON is a review failure, not a pass: report it and fix the invocation once.

- **Every item `pass`**: the repo is done.
- **Any item `fail`**: send the failing items back to that crate's subagent for **one** fix round,
  then re-run the same `omp` call once. A fail that survives the second review goes in `REPORT.md`
  under "unresolved" and does not block the PR — the owner reads it and decides.
- **The model is unavailable** (an auth or "model not found" error from `omp`): **stop the run here.**
  Write `review not run: <the exact error>` into `REPORT.md`, leave the worktrees as they are, and do
  not run `publish` for this run id. Never call another model in its place.

### Step 9: the report

Re-run every check against `$STATE/wt/<repo>` (the same loop as step 1, writing `$STATE/after/`), then
join it into `$STATE/check-after.json`:

```sh
mkdir -p "$STATE/after"
for r in $SEL; do
  python3 "$GHW/tools/rename.py" --repo "$STATE/wt/$r" --check > "$STATE/after/$r-rename.txt" 2>&1 || true
  python3 "$GHW/tools/readme_check.py"  --repo "$STATE/wt/$r" --json "$STATE/after/$r-readme.json"  >/dev/null || true
  python3 "$GHW/tools/doc_refs_check.py" --repo "$STATE/wt/$r" --json "$STATE/after/$r-refs.json"   >/dev/null || true
  python3 "$GHW/tools/media_check.py"   --repo "$STATE/wt/$r" --stale --json "$STATE/after/$r-media.json" >/dev/null || true
  jq -n --arg r "$r" \
    --rawfile rename "$STATE/after/$r-rename.txt" \
    --slurpfile readme "$STATE/after/$r-readme.json" \
    --slurpfile refs "$STATE/after/$r-refs.json" \
    --slurpfile media "$STATE/after/$r-media.json" \
    '{repo: $r,
      rename: ($rename | split("\n") | map(select(startswith("FORBIDDEN")))),
      readme: [$readme[0].checks[] | select(.ok | not)],
      refs:   [$refs[0].checks[]   | select(.ok | not)],
      media:  [$media[0].checks[]  | select(.ok | not)]}' > "$STATE/after/$r.json"
done
jq -s --arg run_id "$RUN_ID" '{run_id: $run_id, repos: map({(.repo): del(.repo)}) | add}' \
  "$STATE"/after/*.json > "$STATE/check-after.json"
```

Then write `$STATE/REPORT.md`:

1. **Header**: run id, start and end time, repos selected, and any repo excluded (with why).
2. **Before/after table**, one row per repo:

   ```
   repo                  rename  readme  refs  media  book  art
   bevy_orca             FAIL→ok 4→0     1→0   2→0    -     pending→picked
   ```

3. **Per-worktree `git diff --stat`**, one fenced block per repo, plus one for `.github`, the book and
   foundation_vs_slop.
4. **Recaptured media**: each row, its host, whether it was refreshed or `capture-failed`, and the path
   to its log.
5. **Art picks**: each job's sheet path, the reviewer's scores per candidate, the picked `k`, and the
   Retro Diffusion spend from the state files (`art/lock.json` `cost_usd` plus every candidate's
   recorded cost).
6. **Reviewer verdicts**: each repo's JSON path and its six items; then "unresolved" with everything
   that survived a second review.
7. **Compile gates**: each repo, pass or the failing command and its first error line.
8. **SPEND block**, by activity, in the format of `~/.omp/agent/AGENTS.md`:

   ```
   SPEND
     reading + measuring      N min   (what: DOCUMENTATION.md, the crates' READMEs, the diff)
     editing                  N min   (how many crates, how many files)
     compiles on bmb          N min   (how many runs, cold or warm)
     captures                 N min   (how many rows, which host)
     art                      N min   (how many jobs, how many candidates, $N.NN)
     review                   N min   (how many omp calls)
     waiting                  N min   (what, specifically)
     total                    N min
   ```

Print the report path and **stop**. `run` never publishes.

The report's structure is what `publish` cuts its PR bodies from, so build it that way: one `## <repo>`
section per crate, then `## .github`, `## dark-incorporated.github.io` and, on a full run,
`## foundation_vs_slop`. Each section carries that repo's before/after row, its `git diff --stat`, its
recaptured rows, its compile-gate result and its reviewer verdict. The summary tables and the SPEND
block sit above them, under `## Summary`. A section that is not going to be published says `excluded:
<why>` on its first line, which is what `publish` reads.

Add a last section, `## Owner actions on the org page`, which `publish` copies into its closing output.
GitHub has no API for the org's picture or its pinned repositories, so the report lists what the owner
does by hand at `https://github.com/organizations/dark-incorporated/settings/profile`:

- upload the picked `profile/avatar.png` (from the `avatar` job) as the organisation picture;
- pin up to six repositories on `https://github.com/dark-incorporated`, in this order: `bevy_dark_factory`,
  then the next five in `crates.json` order (`bevy_gooey`, `bevy_elements`, `bevy_flora`, `isomesh`,
  `bevy_lights`), or the owner's own choice.

State the avatar's picked `k` and its sheet path, so the owner uploads the file that was reviewed.

---

## Mode `publish <run-id>`

Takes the worktrees a finished run left behind and opens one PR per repository. `STATE` is rebuilt
from the argument:

```sh
RUN_ID=$1
test -n "$RUN_ID" || { echo "usage: /regenerate-docs publish <run-id>"; exit 1; }
STATE=~/.local/state/dark-inc-docs/$RUN_ID
test -f "$STATE/REPORT.md" || { echo "no report at $STATE/REPORT.md"; exit 1; }
```

Refuse if `REPORT.md` says the review did not run: a run without a review cannot be published.

```sh
grep -q '^review not run' "$STATE/REPORT.md" && { echo "review did not run; publish refuses"; exit 1; }
```

For each repo the report lists as passing (checks green, compile gate green, subagent done), below
steps 1 and 2. `$CRATES`'s order decides the order of the PRs, so the report table and the PR list read
the same. `$SEL` is rebuilt from the run's report, and a passing repo is one whose worktree has changes
and whose section is not marked excluded:

```sh
SEL=$(jq -r '.[].repo' "$CRATES")
section() { sed -n "/^## $1\$/,/^## /p" "$STATE/REPORT.md"; }
mkdir -p "$STATE/pr"
PASSING=""
for r in $SEL; do
  [ -d "$STATE/wt/$r" ] || continue
  [ -n "$(git -C "$STATE/wt/$r" status --porcelain)" ] || continue
  section "$r" | grep -q '^excluded:' && continue
  PASSING="$PASSING $r"
done
```

1. **Commit and push.** For each `r` in `$PASSING`:

   ```sh
   ( cd "$STATE/wt/$r" \
     && git add -A \
     && git commit -m "docs: regenerate per DOCUMENTATION.md ($RUN_ID)" \
     && git push -u origin "docs/regenerate-$RUN_ID" )
   ```

   Never `--force`. A rejected push means someone else pushed to that branch: stop and report it.

2. **PR body and PR** from the report's section for that repo:

   ```sh
   section "$r" > "$STATE/pr/$r.md"
   gh pr create -R "dark-incorporated/$r" --base main --head "docs/regenerate-$RUN_ID" \
     --title "docs: regenerate ($RUN_ID)" --body-file "$STATE/pr/$r.md"
   ```

3. The three infrastructure worktrees get the same treatment, with their own `-R` and the same
   `docs/regenerate-$RUN_ID` branch. `foundation_vs_slop` only when its worktree exists (a full run):

   ```sh
   for pair in "dark-incorporated/.github:.github" \
               "dark-incorporated/dark-incorporated.github.io:dark-incorporated.github.io"; do
     repo=${pair%%:*}; wt=${pair##*:}
     [ -n "$(git -C "$STATE/wt/$wt" status --porcelain)" ] || continue
     ( cd "$STATE/wt/$wt" \
       && git add -A \
       && git commit -m "docs: regenerate per DOCUMENTATION.md ($RUN_ID)" \
       && git push -u origin "docs/regenerate-$RUN_ID" )
     section "$wt" > "$STATE/pr/$wt.md"
     gh pr create -R "$repo" --base main --head "docs/regenerate-$RUN_ID" \
       --title "docs: regenerate ($RUN_ID)" --body-file "$STATE/pr/$wt.md"
   done

   if [ -d "$STATE/wt/foundation_vs_slop" ]; then
     ( cd "$STATE/wt/foundation_vs_slop" \
       && git add -A \
       && git commit -m "docs: regenerate per DOCUMENTATION.md ($RUN_ID)" \
       && git push -u origin "docs/regenerate-$RUN_ID" )
     section foundation_vs_slop > "$STATE/pr/foundation_vs_slop.md"
     gh pr create -R Ladvien/foundation_vs_slop --base main --head "docs/regenerate-$RUN_ID" \
       --title "docs: regenerate ($RUN_ID)" --body-file "$STATE/pr/foundation_vs_slop.md"
   fi
   ```

   `foundation_vs_slop` is a clone of `Ladvien/foundation_vs_slop`, so its pushes and its PR both name
   that owner; everything else in this run is `dark-incorporated`.

4. **Repo metadata**, once per run:

   ```sh
   gh repo edit dark-incorporated/.github \
     --description "Dark Incorporated: org profile, documentation guide and art"
   gh repo edit dark-incorporated/dark-incorporated.github.io \
     --description "The Dark Incorporated book: how the crates fit together"
   ```

   The organisation's own page, `https://github.com/dark-incorporated`, takes its description and website
   from the API. Its name (`Dark Inc.`) is the owner's and is left alone. The description is the profile
   README's first-sentence idea in under 160 characters:

   ```sh
   gh api -X PATCH orgs/dark-incorporated \
     -f description="An agent-first game editor and the Bevy crates around it: gothic industrial, neon cyberpunk, 80s pixel art." \
     -f blog="https://dark-incorporated.github.io/"
   ```

   The profile body itself (banner, intro, family table) is `profile/README.md` in `.github`, which ships
   in that repo's PR, so it appears on the org page only once the owner merges that PR. After the merge,
   check the live page: `gh api orgs/dark-incorporated --jq '[.name,.description,.blog]'` returns the
   values above, and a browser screenshot of `https://github.com/dark-incorporated` shows the new banner
   and the generated family table. The avatar and the pinned repositories are the owner's actions listed
   in `REPORT.md`.

5. **The one label rename** (`names.json` `labels`). For each `[old, new]` pair, and each repo where
   the OLD label still exists, rename it in place — the old value on the left is what we migrate from:

   ```sh
   jq -r '.labels[] | @tsv' "$GH/names.json" | while IFS=$'\t' read -r old new; do
     for r in $(jq -r '.[].repo' "$CRATES") .github dark-incorporated.github.io; do
       full="dark-incorporated/$r"
       gh label list -R "$full" --limit 200 --json name -q '.[].name' | grep -qxF "$old" \
         && gh label edit "$old" --name "$new" -R "$full"
     done
   done
   ```

   The pair comes from `names.json`, not from prose, so a pair added there later is picked up here
   without editing this command. Today's only pair is the old label `consumer:bevy_grimoire`, which
   becomes `consumer:bevy_dark_factory`; both are `names.json`'s `labels` entries.

6. **Homepage and topics** per crate, because today's still point at the old site and carry the old
   topic:

   ```sh
   for r in $SEL; do
     gh repo edit "dark-incorporated/$r" \
       --homepage "https://dark-incorporated.github.io/crates/$r/" \
       --remove-topic bevy-coven --add-topic dark-incorporated
   done
   ```

   `--remove-topic` on a repo that does not carry it is ignored by `gh`, so this is safe to repeat.

7. Print every PR URL, then print the `## Owner actions on the org page` section of `REPORT.md`
   (`section "Owner actions on the org page"`), then stop. **Never merge.**

---

## Mode `publish-book <run-id>`

The only mode that pushes `main`, and only after the crate PRs merged.

```sh
RUN_ID=$1
test -n "$RUN_ID" || { echo "usage: /regenerate-docs publish-book <run-id>"; exit 1; }
STATE=~/.local/state/dark-inc-docs/$RUN_ID
BOOKW=$STATE/wt/dark-incorporated.github.io
SEL=$(jq -r '.[].repo' "$CRATES")
```

1. **Refuse while any PR of the run is open or closed unmerged.** Check every crate the run touched,
   plus `.github`, the book, and `Ladvien/foundation_vs_slop` when its worktree exists:

   ```sh
   unmerged=""
   check_pr() {   # $1 = owner/repo
     state=$(gh pr view --repo "$1" --head "docs/regenerate-$RUN_ID" --json state -q .state 2>/dev/null || echo NONE)
     [ "$state" = "MERGED" ] || unmerged="$unmerged $1:$state"
   }
   for r in $SEL; do check_pr "dark-incorporated/$r"; done
   check_pr dark-incorporated/.github
   check_pr dark-incorporated/dark-incorporated.github.io
   [ -d "$STATE/wt/foundation_vs_slop" ] && check_pr Ladvien/foundation_vs_slop
   [ -z "$unmerged" ] || { echo "not merged:$unmerged"; exit 1; }
   ```

   A `NONE` means no PR with that head exists, which is as much a refusal as an open one.

2. **Catch the shared clones up, then re-sync from merged `main`:**

   ```sh
   for r in $SEL; do git -C "$DI/$r" pull --ff-only; done
   git -C "$GH"   pull --ff-only
   git -C "$BOOK" pull --ff-only
   ( cd "$BOOKW" && git fetch origin && git switch --detach origin/main )
   python3 "$BOOKW/tools/sync_crates.py" --workspace "$DI"
   python3 "$BOOKW/tools/glossary.py"
   mdbook build
   lychee --offline --root-dir "$PWD/book" book/
   ```

   The worktree switches to a detached `origin/main` so the run's own `docs/regenerate-<run-id>` branch
   and its commits are left exactly as they are; nothing is reset or discarded.

   `sync_crates.py` with no `--worktrees` pins each synced page to the merged `main` sha, which is the
   point of doing it here.

3. **Publish.** Commit in the book worktree and push a fast-forward:

   ```sh
   ( cd "$BOOKW" \
     && git add -A \
     && git commit -m "docs: sync the book to the merged crates ($RUN_ID)" \
     && git push origin HEAD:main )
   ```

   That push is a fast-forward. If it is refused, **stop and report the refusal** — do not force, do not
   rebase, do not retry with another refspec.

---

## One-time: rename CI runner registrations (`runners` mode)

**Runs once, by hand, when the org is renamed — not part of `run`.** After it, every runner unit on
`big` carries the new org name and the caches stay warm. Print each command's output into the report;
do not summarise.

1. **Wait until no runner is busy.** `repos.txt` still lists the OLD org, so read the repo name from it
   and ask the new org (repos have already moved):

   ```sh
   REPOS=~/home-cloud/gh-runners/repos.txt
   busy() {
     sed 's|^[^/]*/||; s/[[:space:]].*$//' "$REPOS" | sort -u | while read -r name; do
       [ -n "$name" ] || continue
       gh api "repos/dark-incorporated/$name/actions/runners" -q '.runners[]|select(.busy)|.name'
     done
   }
   for i in $(seq 1 12); do
     [ -z "$(busy)" ] && break
     sleep 300
   done
   [ -z "$(busy)" ] || { echo "still busy after 60 minutes"; busy; exit 1; }
   ```

   Twelve polls five minutes apart. Still busy after that: stop and name the repo and runner.

2. **Rewrite `repos.txt` in place.** OLD values on the left, new on the right (BSD `sed`, which is what
   macOS ships; on GNU use `sed -i` with the same expressions):

   ```sh
   sed -i '' \
     -e 's|^bevy-coven/bevy_grimoire |dark-incorporated/bevy_dark_factory |' \
     -e 's|^bevy-coven/|dark-incorporated/|' \
     ~/home-cloud/gh-runners/repos.txt
   ```

   The file has one uncommitted, unrelated line (`bevy-coven/bevy_siren 1`) from other work: it is
   renamed like the rest, and the file is **not committed**. Print `git -C ~/home-cloud diff
   gh-runners/repos.txt` into the report so the owner sees exactly what moved.

3. **Stop the old units on `big`:**

   ```sh
   ssh big 'systemctl --user disable --now $(systemctl --user list-units --plain --no-legend "gh-runner@bevy-coven__*" | cut -d" " -f1)'
   ```

4. **Move the caches so they stay warm.** On `big`, in `~/gh-runners/cache`, each
   `bevy-coven__<repo>` becomes `dark-incorporated__<repo>`, with `bevy_grimoire` becoming
   `bevy_dark_factory`. `mv` only when the target does not exist; otherwise leave both and report the
   pair as a collision (**never delete a cache**):

   ```sh
   ssh big 'cd ~/gh-runners/cache && for d in bevy-coven__*; do
     [ -d "$d" ] || continue
     repo=${d#bevy-coven__}; repo=${repo/bevy_grimoire/bevy_dark_factory}
     target="dark-incorporated__$repo"
     if [ -e "$target" ]; then echo "COLLISION $d -> $target (both kept)"; else mv "$d" "$target"; fi
   done'
   ```

5. **Reconcile every instance with the file:**

   ```sh
   ~/home-cloud/gh-runners/deploy.sh
   ```

6. **Verify.** Every repo shows at least one online runner within 10 minutes, and no old unit survives:

   ```sh
   sed 's|^[^/]*/||; s/[[:space:]].*$//' "$REPOS" | sort -u | while read -r name; do
     [ -n "$name" ] || continue
     echo "== $name"
     gh api "repos/dark-incorporated/$name/actions/runners" -q '.runners[]|[.name,.status]|@tsv'
   done
   ssh big 'systemctl --user list-units "gh-runner@bevy-coven__*"'   # lists nothing
   ssh big 'ls ~/gh-runners/cache'                                   # no bevy-coven__* left, except reported pairs
   ```

   A repo with no `online` line after 10 minutes is named, and the mode stops. The first crate PR's
   `build` job then logs `Compiling` only for its own package, which is how the warm cache proves
   itself.

---

## Appendix: what each mode leaves behind

| Mode | Worktrees | Commits | Pushes | Writes to `$STATE` |
|---|---|---|---|---|
| `check` | none | none | none | `json/` |
| `run` | one per repo + infra | none | none | everything |
| `publish` | reuses `run`'s | one per repo | one branch per repo | `pr/` |
| `publish-book` | reuses `run`'s | one in the book | `main` of the book | none |
| `runners` | none | none | none | none |

The owner signs off on `REPORT.md` before `publish`, and merges every PR before `publish-book`.
