# bevy_stigmergy

Fading marks on a grid that a crowd coordinates through, like ant trails. Agents deposit into shared channels that evaporate and diffuse between floor cells, never through a wall, and read them back by value or by gradient, so a crowd converges on a trail, scatters from a threat or rallies toward a moving target without any agent planning a route. The field is computed once per tick and shared by every agent.

![Ninety foragers find the gap in a wall: a bright amber trail forms between nest and food while older trails fade](https://raw.githubusercontent.com/bevy-coven/bevy_stigmergy/main/docs/foraging.gif)

## Add it

```sh
cargo add bevy_stigmergy
```

The [README](https://github.com/bevy-coven/bevy_stigmergy#quick-start) has a quick start that is compiled on every `cargo test`. The crate depends only on `bevy_math`; it owns no resources, registers no systems and has no schedule, so it ticks wherever your game's loop says.

## What it gives you

- `StigGrid<N>`: `N` scalar channels with `deposit`, `evaporate_diffuse`, `sample_cell`, `gradient_cell` and `hotspot_cell` ([the field](https://github.com/bevy-coven/bevy_stigmergy/blob/main/docs/guide/model.md)).
- `RallyGrid`: a vector per cell, for recruiting toward a target that moves.
- `CellFrame`: an optional world-to-cell mapping for an axis-aligned grid.
- `evaporate_diffuse_with`: the same tick split into chunks for your own thread pool, bit-identical to the inline one ([ticking](https://github.com/bevy-coven/bevy_stigmergy/blob/main/docs/guide/ticking.md)).
- `serde` and `reflect` features on the settings types.

## Use it in Grimoire

Grimoire takes this crate behind its `bevy_stigmergy` feature, for the **crowd preview** (issue #107): it walks N people from one area of a map to another with `bevy_orca`'s avoidance, and each lays a trail and a congestion mark into a `StigGrid` laid over the map with a `CellFrame`. The result is a measurement, not an edit: the two fields drawn as an overlay, how many walkers arrived, and where congestion peaks, so you can see where a gap between buildings jams before a game ships it. The settings it uses are the crate's own `ChannelDef`s, which are `Serialize`/`Deserialize` behind the `serde` feature.

## Links

- [Repository](https://github.com/bevy-coven/bevy_stigmergy) · [docs.rs](https://docs.rs/bevy_stigmergy) · [crates.io](https://crates.io/crates/bevy_stigmergy) · [CHANGELOG](https://github.com/bevy-coven/bevy_stigmergy/blob/main/CHANGELOG.md)
