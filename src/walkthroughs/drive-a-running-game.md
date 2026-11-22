# Drive a running game from an agent

By the end of this page an agent has read the state of a running Bevy game, taken a screenshot of it and spawned objects in it, using `bevy_fairy`.

## Preview

![A seven-second loop: the agent checks status, reads the spinner and captures the frame, then spawns three cubes through the game's own command](https://raw.githubusercontent.com/dark-incorporated/bevy_fairy/main/docs/media/hero.gif)

*The whole loop in seven seconds: `status`, a `brp` read beside the frame its `screenshot` call saved, then three `run` calls.*

## Demonstration

### 1. Run the demo game (3 minutes)

In a clone of [`bevy_fairy`](https://github.com/dark-incorporated/bevy_fairy):

```sh
cargo run --features plugin-screenshot --example demo_game
```

The game has a score, a mover and a spinner with a planted bug. It serves the Bevy Remote Protocol (BRP) on `127.0.0.1:15702`.

### 2. Check it answers (1 minute)

```sh
curl -s localhost:15702 -d '{"jsonrpc":"2.0","id":1,"method":"bevy_fairy/status"}'
```

The reply contains `"ready":true`.

### 3. Install the server and connect the agent (3 minutes)

```sh
cargo install bevy_fairy --no-default-features --features server
claude mcp add bevy-fairy -- bevy-fairy --stdio
```

Other agent clients are covered on the [clients page](https://github.com/dark-incorporated/bevy_fairy/blob/main/docs/guide/clients.md).

### 4. Ask the agent (2 minutes)

Ask: *"Call `status`, then list the game's resources with `brp`."* Then ask it to take a `screenshot`.

### 5. Add it to your own game (3 minutes)

```sh
cargo add bevy_fairy --no-default-features --features plugin
```

```rust,ignore
use bevy::prelude::*;
use bevy::remote::http::RemoteHttpPlugin;
use bevy_fairy::DebuggerPlugin;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins(DebuggerPlugin::default())
        .add_plugins(RemoteHttpPlugin::default())
        .run();
}
```

`DebuggerPlugin` adds Bevy's `RemotePlugin` itself, so do not add a second one.

## Review

- The agent speaks MCP to the `bevy-fairy` server, which speaks BRP to your game.
- It cannot see frame time, CPU or memory, because BRP does not report them, and the tools say so.
- The Dark Factory links this plugin, so the Night Shift can read and drive a running game the same way.
