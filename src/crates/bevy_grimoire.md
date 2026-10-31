# Grimoire (`bevy_grimoire`)

The coven's editor, and its book of spells: a world editor for Bevy games where you build levels with an AI agent, the Familiar, working beside you. The Familiar changes a map only through the same named operations you use, its changes join your one undo history, and you show it what you mean by snipping a rectangle of the editor with a note.

![An agent turns the abbey 90 degrees and removes its table through MCP calls; the inspector names each change as the agent's, and two presses of Cmd+Z take them back](https://raw.githubusercontent.com/bevy-coven/bevy_grimoire/main/docs/media/agent-drives.gif)

## The demo

<video controls preload="none" poster="../media/bevy_grimoire-demo.png" src="../media/bevy_grimoire-demo.mp4" width="100%"></video>

64 seconds on a walled map: the agent frames two wall pieces, turns `wall_02_2` to 90 degrees and removes `wall_02_3`; the person's Cmd+Z reports `put back wall_02_3`. It ends with a snip: the person drags a box over the walled cluster, writes a note, and the receipt names the PNG it saved.

## Add it

The editor is a program you run from a clone, on your game's project:

```sh
git clone https://github.com/bevy-coven/bevy_grimoire
cd bevy_grimoire
cargo run -p bevy_grimoire_mapper -- /path/to/your/game
```

Your game links only the libraries: `cargo add bevy_grimoire_core bevy_grimoire`. `bevy_grimoire_core` is engine-free and holds the grammar and the solvers; `bevy_grimoire` puts a library and a map into a Bevy world (`GrimoirePlugin`), and `GrimoireLivePlugin` reloads them while the game runs, so an edit shows up about a second later. A project from before the rename keeps its data in `assets/emerge`; the editor moves it to `assets/grimoire` the first time it opens the project.

## What it gives you

- Maps built from kits: place, fill, turn, remove and undo ([building maps](https://github.com/bevy-coven/bevy_grimoire/blob/main/docs/guide/building-maps.md)).
- Layouts learned from a corner you laid out and continued with wave function collapse, drawn before you keep them.
- Kits and labels, with a vision model's proposals marked unchecked until you confirm them ([kits and labels](https://github.com/bevy-coven/bevy_grimoire/blob/main/docs/guide/kits-and-labels.md)).
- The MCP server, `bevy_grimoire_mcp`, whose tools (`grimoire_state`, `grimoire_apply_operation`, captures, snips) let the Familiar read and drive the open editor ([MCP tools](https://github.com/bevy-coven/bevy_grimoire/blob/main/docs/mcp-tools.md)).
- Panels for the rest of the coven, each editing that crate's own settings ([using a crate with Grimoire](../with-grimoire.md)).

## Use it in Grimoire

This is Grimoire. Every other crate's page says what Grimoire does with it.

## Links

- [Repository](https://github.com/bevy-coven/bevy_grimoire) · [The guide](https://github.com/bevy-coven/bevy_grimoire/blob/main/docs/guide/README.md) · [docs.rs (core)](https://docs.rs/bevy_grimoire_core) · [crates.io](https://crates.io/crates/bevy_grimoire) · [CHANGELOG](https://github.com/bevy-coven/bevy_grimoire/blob/main/CHANGELOG.md)
