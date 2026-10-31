# Using a crate with Grimoire

[Grimoire](crates/bevy_grimoire.md) is the coven's editor. It runs as its own program on your game's project, so the editor never becomes part of your game's build:

```sh
cargo run -p bevy_grimoire_mapper -- <game-root> <map> --kit <kit>
```

With `--live`, every change is written through to disk as you make it, for a game that watches its own project.

## Each crate is an optional feature of the editor

Grimoire takes each crate in the family as an optional cargo feature, pinned to a git revision on that crate's `main`. Turning a feature on gives the editor that crate's panels: a sky and weather panel for `bevy_elements`, a forest panel for `bevy_flora`, villagers for `bevy_society`, and so on.

## Configure, don't fork

The editor never defines a second schema for a crate's settings. A crate's own serde types are the data: Grimoire saves them in your game's project, and edits them live. So the file the editor writes is the same file your game loads with the crate on its own, and a game can drop the editor at any time.

## The two-way street

When the editor needs something from a crate, the change is made in that crate's repository, with its own tests, and requested there as an issue labelled `consumer` and `consumer:bevy_grimoire`. The editor takes it by moving its pin once the issue is closed as fixed. A game asks the editor for what it needs the same way, with `consumer` and `consumer:<game>` on the editor's repository.

## The Familiar

Grimoire's MCP server (`bevy_grimoire_mcp`) lets an agent, the Familiar, read the editor's state with `grimoire_state` and change a map with `grimoire_apply_operation`. Each crate's page says what its panel lets you, or the Familiar, change.
