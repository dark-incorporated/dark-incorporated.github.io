# bevy_fairy

`bevy_fairy` lets a coding agent look inside a running Bevy 0.20 game, drive it, and ask the person playing it for help — without touching the desktop. It is one crate with two halves: a **Bevy plugin** the game links, which registers `bevy_fairy/*` methods on the [Bevy Remote Protocol](https://docs.rs/bevy_remote) (BRP, Bevy's own JSON-RPC interface on port 15702), and an **MCP server**, `bevy-fairy`, that gives an agent tools to read the game's state, run the game's own commands, capture a PNG from the game's own pixels and inject input into Bevy's own messages. Nothing here captures the screen or synthesises an OS event: a capture from the window focused had 7,188 distinct colours on the game this was built for, and one flat colour with another app in front.

![A scripted tour: each tool call beside the frame the same call captured](https://github.com/dark-incorporated/bevy_fairy/raw/HEAD/docs/media/hero.gif)

## Add it

```sh
cargo add bevy_fairy --no-default-features --features plugin
```

```rust,no_run
use bevy::prelude::*;
use bevy::remote::http::RemoteHttpPlugin;
use bevy_fairy::DebuggerPlugin;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        // Owns the BRP RemotePlugin. Never add a second one next to it.
        .add_plugins(DebuggerPlugin::default())
        .add_plugins(RemoteHttpPlugin::default())
        .run();
}
```

Then `cargo install bevy_fairy --no-default-features --features server` and register `bevy-fairy --stdio` with the agent. The README's Quick Start is the same two steps with the checks between them.

## What it gives you

- **Read state, change it, undo it.** `brp` calls any BRP method the game serves; `observe` answers a phrase query with component values and diffs it against the last read; `experiment` spawns, modifies and deletes entities and steps back through its own history — [the tools](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/tools.md), [changing the game](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/claims.md).
- **Watch one value over time.** `watch` reports which fields moved and which stopped, each sample stamped with the game frame; `burst` returns a run of frames as one labelled contact sheet; `bevy_fairy/ring` records frames inside the game and freezes on a trigger — [the tools](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/tools.md).
- **Run the game's own actions, and replay them.** `commands` lists what the game registered with typed params and a worked example; `run` calls one; `scene save` writes the run to a file `BEVY_FAIRY_SCENE` replays at startup — [commands](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/commands.md), [scenes](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/scene.md).
- **See the screen.** `screenshot` captures from an offscreen render target or from the window, with a crop and a zoom, and says which frame it was asked on and which it was delivered on — [capture](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/capture.md).
- **Press keys, type, click and drag.** `bevy_fairy/input` writes into Bevy's own input messages, so `ButtonInput`, text fields and `bevy_ui` picking all see it; a press, a cursor move and a release elsewhere is a drag — [input](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/input.md).
- **Ask a person.** `guide` posts a script the game draws one step at a time, and each step moves on when a checkpoint the game registered passes — [the guide overlay](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/guide.md).
- **Six worked sessions.** A value that stops changing, an entity in the wrong place, a capture with state beside it, a player's keystroke, a regression test that is a command, a reproduction walked through a person — [workflows](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/workflows.md).

<a id="use-it-in-blueprint"></a>
## Use it in the Dark Factory

The Dark Factory takes this crate as an optional dependency, `bevy_debugger_bevy` (the package is `bevy_fairy`), pinned to a git revision of `main` with `default-features = false, features = ["plugin", "plugin-guide", "plugin-screenshot"]`: the guide overlay, capture, and the injected cursor, and none of the server. With the feature off, `cargo tree -i bevy_debugger_bevy` finds no package and neither does `bevy_remote`.

There is no settings panel for it, because there is nothing to author: the plugin has no file format of its own and no serde configuration. What it does in the editor is drive the editor.

- **`DebuggerPlugin::default()`** is added in `harness.rs`, so the editor's own window answers `bevy_fairy/status`, `commands`, `input`, `screenshot`, `capture`, `guide` and `quit` at 127.0.0.1:15702. That is how an agent looks at the Dark Factory the way it looks at a game; it is on by default because the editor is not a build that ships to a player.
- **`DebugCaptureTarget`** is inserted in `surface.rs` with the image the editor's camera renders to, so a `screenshot` of the Dark Factory is the editor's own interface — panes, tabs and all — captured offscreen, with the window behind another app or on another Space.
- **`DebugCommandsAppExt::add_debug_command`** in `ops_brp.rs` registers the editor's own verbs, so an agent finds them with `commands` and runs them with `run` with typed params and an example, rather than driving the UI blind.
- **`Checkpoints` and `Guide`** in `guided.rs` and `chooser.rs` are what a guided run uses: each step names a condition the editor itself evaluates, so a script the agent posts advances when the author actually got there. `GuidePlacement` is `insert_resource`d at `top: 58.0` so the card sits below the title line rather than over the tab bar it describes.
- **`cursor_position(&window, &DebugCursor)`** in `view.rs` is the one line an editor that reads the pointer itself has to write: the plugin injects a cursor instead of moving the real mouse, so a host reads through the plugin's function rather than `Window::cursor_position`.

A setting that would fit a panel, and does not exist yet: a `GuidePlacement` and a "debugger on/off" toggle in the editor's own settings file, so the port and the card's position survive a restart.

## Links

- [The repository](https://github.com/dark-incorporated/bevy_fairy)
- [API docs on docs.rs](https://docs.rs/bevy_fairy)
- [crates.io](https://crates.io/crates/bevy_fairy)
- [The guide](https://github.com/dark-incorporated/bevy_fairy/tree/main/docs/guide) and [the generated tool reference](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/mcp-tools.md)
- [CHANGELOG](https://github.com/dark-incorporated/bevy_fairy/blob/main/CHANGELOG.md)
