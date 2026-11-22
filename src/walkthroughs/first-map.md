# Build your first map

By the end of this page you have made a map in the Dark Factory, placed pieces on it with your own hands, then watched the Night Shift (an agent) place and undo pieces through the same operations, and taken the keyboard back.

## Preview

![An agent turns the abbey 90 degrees and removes its table through MCP calls; the inspector names each change as the agent's, and two presses of Cmd+Z take them back](https://raw.githubusercontent.com/dark-incorporated/bevy_dark_factory/main/docs/media/agent-drives.gif)

*What you build towards: the agent's changes are named as the agent's, and your undo takes them back.*

You need a Rust toolchain and a clone of [`bevy_dark_factory`](https://github.com/dark-incorporated/bevy_dark_factory). Run every command from the repository root.

## Demonstration

### 1. Open the editor (2 minutes)

```sh
cargo run -p bevy_dark_factory -- .
```

The editor opens on the project page, with **Maps** and **Kits** sections. A **kit** is a folder of pieces; a **piece** is one thing you can place, such as a wall or a sofa.

![Placing a sofa on the bedroom map, then undoing it](https://raw.githubusercontent.com/dark-incorporated/bevy_dark_factory/main/docs/media/place-and-undo.gif)

### 2. Make a map (1 minute)

Press **+ New map**, type `first_map` as the name, then press **Create**. The map opens on the Map workspace.

### 3. Place a piece and undo it (3 minutes)

Press Down until a piece in the PLACE list is armed, move the pointer over the floor and click. Place a second piece the same way. Press `Cmd+Z` (`Ctrl+Z` on Windows and Linux) to take the last placement back.

### 4. Let the Night Shift drive (3 minutes)

Connect an agent to the running editor and ask it to move a piece. Every step, including the config for your agent's client, is in the [Agents guide](https://github.com/dark-incorporated/bevy_dark_factory/blob/main/docs/guide/agents.md). The short form:

```sh
cargo build -p dark_factory_mcp
```

Point your agent's MCP configuration at `target/debug/dark_factory_mcp --project <your project folder>`, then ask it to call `blueprint_state`. It answers with the open map and the undo depth.

### 5. Take the keyboard back (1 minute)

Place a piece yourself while the agent is connected. The inspector names which changes were yours and which were the agent's, and one undo history covers both.

![The agent hands the editor back to the person](https://raw.githubusercontent.com/dark-incorporated/bevy_dark_factory/main/docs/media/agent-hands-back.gif)

## Review

- A map is a file, `first_map.map.yaml`, holding your placements.
- You and the Night Shift use the same named operations, so there is one undo history for both.
- If the agent says no editor answered, the editor is not running, or the two sides use different `BEVY_BRP_PORT` values.

Next: [add fire to your game](fire-in-your-game.md) with one crate, no editor needed.
