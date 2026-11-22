# Bevy Coven

![A black raven with spread wings flying across a yellow full moon, airbrushed pink and orange clouds on a purple sky, over a black city skyline, in pixel art](media/banner.png)

Some parts of a game only grow as fast as people can author them: levels, set dressing, dialogue, the lives of villagers, interfaces, weather. Bevy Coven is a family of [Bevy](https://bevyengine.org/) crates built so that those parts grow with agents too.

> ⚠️ **Vibe Coded.** Written by AI agents working from a human's direction, covered by tests rather than a line-by-line human review. Read the code before you rely on it for something you care about.

## The coven, the grimoire, the cauldron and the familiar

- **The coven** is the family of crates. Each one is a Bevy plugin with its own settings, and works on its own: a sky, a forest, a crowd, a dialog box.
- **The grimoire** is the book of spells, and it is what a game loads: its kits, the grammar learned from your example, and the maps built from that grammar ([bevy_grimoire](crates/bevy_dark_factory/index.md)).
- **The Cauldron** is the editor where the grimoire is written: you and the familiar place pieces, and the learned grammar brews more.
- **The familiar** is the helper at your side: the agent that reads and writes the grimoire, through the Cauldron's MCP server.

Two more helpers belong to the same story: [bevy_fairy](crates/bevy_fairy/index.md), which lets an agent read and drive a running game, and golem, which drives Blender to make meshes.

## How the crates relate

- Every crate stands alone: add it with `cargo add` and its plugin with `app.add_plugins(...)`. See [Using a crate on its own](alone.md).
- The Cauldron hosts each crate as an optional cargo feature and edits that crate's own settings live, in your game's project. See [Using a crate in the Cauldron](with-cauldron.md).
- Some crates use each other. `bevy_society` speaks through `bevy_speech_bubbles`, steers its walkers with `bevy_orca` and leaves marks with `bevy_stigmergy`.

The [map of the coven](map.md) shows every crate, grouped by what it gives a game.
