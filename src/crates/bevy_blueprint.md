# Blueprint and the Dark Factory (`bevy_blueprint`)

The blueprint is what a game loads (`bevy_blueprint` and `blueprint_model`). **The Dark Factory is Dark Inc.'s editor**, where you build it: a world editor for Bevy games where you build levels with an AI agent, the Night Shift, working beside you. The Night Shift changes a map only through the same named operations you use, its changes join your one undo history, and you show it what you mean by snipping a rectangle of the editor with a note.

![An agent turns the abbey 90 degrees and removes its table through MCP calls; the inspector names each change as the agent's, and two presses of Cmd+Z take them back](https://raw.githubusercontent.com/dark-incorporated/bevy_dark_factory/main/docs/media/agent-drives.gif)

## The demo

<video controls preload="none" poster="../media/bevy_blueprint-demo.png" src="../media/bevy_blueprint-demo.mp4" width="100%"></video>

64 seconds on a walled map: the agent frames two wall pieces, turns `wall_02_2` to 90 degrees and removes `wall_02_3`; the person's Cmd+Z reports `put back wall_02_3`. It ends with a snip: the person drags a box over the walled cluster, writes a note, and the receipt names the PNG it saved.

## Add it

The editor is a program you run from a clone, on your game's project:

```sh
git clone https://github.com/dark-incorporated/bevy_dark_factory
cd bevy_blueprint
cargo run -p bevy_dark_factory -- /path/to/your/game
```

Your game links only the libraries: `cargo add blueprint_model bevy_blueprint`. `blueprint_model` is engine-free and holds the grammar and the solvers; `bevy_blueprint` puts a library and a map into a Bevy world (`BlueprintPlugin`), and `BlueprintLivePlugin` reloads them while the game runs, so an edit shows up about a second later. A project from before the rename keeps its data in `assets/emerge`; the editor moves it to `assets/blueprint` the first time it opens the project.

## What it gives you

- Maps built from kits: place, fill, turn, remove and undo ([building maps](https://github.com/dark-incorporated/bevy_dark_factory/blob/main/docs/guide/building-maps.md)).
- Layouts learned from a corner you laid out and continued with wave function collapse, drawn before you keep them.
- Kits and labels, with a vision model's proposals marked unchecked until you confirm them ([kits and labels](https://github.com/dark-incorporated/bevy_dark_factory/blob/main/docs/guide/kits-and-labels.md)).
- The MCP server, `dark_factory_mcp`, whose tools (`factory_state`, `factory_apply_operation`, captures, snips) let the Night Shift read and drive the open editor ([MCP tools](https://github.com/dark-incorporated/bevy_dark_factory/blob/main/docs/mcp-tools.md)).
- Panels for the rest of Dark Inc., each editing that crate's own settings ([using a crate in the Dark Factory](../with-dark-factory.md)).

<a id="use-it-in-blueprint"></a>
## Use it in the Dark Factory

This is the Dark Factory. Every other crate's page says what the Dark Factory does with it.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_dark_factory) · [The guide](https://github.com/dark-incorporated/bevy_dark_factory/blob/main/docs/guide/README.md) · [docs.rs (core)](https://docs.rs/blueprint_model) · [crates.io](https://crates.io/crates/bevy_blueprint) · [CHANGELOG](https://github.com/dark-incorporated/bevy_dark_factory/blob/main/CHANGELOG.md)
