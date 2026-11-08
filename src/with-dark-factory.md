# Using a crate in the Dark Factory

[The Dark Factory](crates/bevy_blueprint.md) is Dark Inc.'s editor, where the blueprint a game loads is written. It runs as its own program on your game's project, so the editor never becomes part of your game's build:

```sh
cargo run -p bevy_dark_factory -- <game-root> <map> --kit <kit>
```

With `--live`, every change is written through to disk as you make it, for a game that watches its own project.

## Each crate is an optional feature of the editor

The Dark Factory takes each crate in the family as an optional cargo feature, pinned to a git revision on that crate's `main`. Turning a feature on gives the editor that crate's panels: a sky and weather panel for `bevy_elements`, a forest panel for `bevy_flora`, villagers for `bevy_society`, and so on.

## Configure, don't fork

The editor never defines a second schema for a crate's settings. A crate's own serde types are the data: the Dark Factory saves them in your game's project, and edits them live. So the file the editor writes is the same file your game loads with the crate on its own, and a game can drop the editor at any time.

## The two-way street

When the editor needs something from a crate, the change is made in that crate's repository, with its own tests, and requested there as an issue labelled `consumer` and `consumer:bevy_dark_factory`. The editor takes it by moving its pin once the issue is closed as fixed. A game asks the editor for what it needs the same way, with `consumer` and `consumer:<game>` on the editor's repository.

## The Night Shift

The Dark Factory's MCP server (`dark_factory_mcp`) lets an agent, the Night Shift, read the editor's state with `factory_state` and change a map with `factory_apply_operation`. Each crate's page says what its panel lets you, or the Night Shift, change.
