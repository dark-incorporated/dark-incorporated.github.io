# Bevy Coven

![A black raven with spread wings flying across a yellow full moon, airbrushed pink and orange clouds on a purple sky, over a black city skyline, in pixel art](media/banner.png)

Some parts of a game only grow as fast as people can author them: levels, set dressing, dialogue, the lives of villagers, interfaces, weather. Bevy Coven is a family of [Bevy](https://bevyengine.org/) crates built so that those parts grow with agents too.

> ⚠️ **Vibe Coded.** Written by AI agents working from a human's direction, covered by tests rather than a line-by-line human review. Read the code before you rely on it for something you care about.

## The coven, the grimoire and the familiar

- **The coven** is the family of crates. Each one is a Bevy plugin with its own settings, and works on its own: a sky, a forest, a crowd, a dialog box.
- **The grimoire** is the book of spells: [Grimoire](crates/bevy_grimoire.md), the editor. It holds a game's kits, the grammar it learns from your example, and the maps it builds from that grammar.
- **The familiar** is the helper at your side: the agent that reads and writes the grimoire, through the editor's MCP server.

Two more helpers belong to the same story: [bevy_fairy](crates/bevy_fairy.md), which lets an agent read and drive a running game, and golem, which drives Blender to make meshes.

## How the crates relate

- Every crate stands alone: add it with `cargo add` and its plugin with `app.add_plugins(...)`. See [Using a crate on its own](alone.md).
- Grimoire hosts each crate as an optional cargo feature and edits that crate's own settings live, in your game's project. See [Using a crate with Grimoire](with-grimoire.md).
- Some crates use each other. `bevy_society` speaks through `bevy_speech_bubbles`, steers its walkers with `bevy_orca` and leaves marks with `bevy_stigmergy`.

The [map of the coven](map.md) shows every crate, grouped by what it gives a game.
