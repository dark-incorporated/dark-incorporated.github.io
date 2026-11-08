# bevy_orca

Walkers that steer around each other without colliding. ORCA (optimal reciprocal collision avoidance) gives each agent the velocity closest to the one it wanted that no neighbour can object to, assuming every neighbour reasons the same way and each takes half the dodge. It is a plain library on `bevy_math`'s `Vec2`, with no ECS, plugin or schedule: you call a function and get a velocity back.

![Twenty coloured discs swap sides of a circle through a rotating vortex, without colliding](https://raw.githubusercontent.com/dark-incorporated/bevy_orca/main/docs/circle_swap.gif)

## Add it

```sh
cargo add bevy_orca
```

The [README](https://github.com/dark-incorporated/bevy_orca#quick-start) has a single-agent quick start that is compiled on every `cargo test`.

## What it gives you

- `new_velocity` for one agent, with a documented, finite answer for every unusable input and never a velocity over `max_speed` ([one agent](https://github.com/dark-incorporated/bevy_orca/blob/main/docs/guide/one-agent.md)).
- `Crowd` for many: a neighbour grid, a deterministic tie-break, a sideways `nudge`, and no allocation once warm ([a whole crowd](https://github.com/dark-incorporated/bevy_orca/blob/main/docs/guide/crowd.md)).
- Right of way through `priority`, and `Crowd::begin` / `CrowdStep::solve_range` to split a step over your own thread pool with bit-identical results.
- `ObstaclesBuilder` for buildings, walls, polygons and tile maps, as RVO2's obstacle lines ([static obstacles](https://github.com/dark-incorporated/bevy_orca/blob/main/docs/guide/obstacles.md)).
- `serde` and `reflect` features on `Agent`, `CrowdMember` and `CrowdParams`.

<a id="use-it-in-blueprint"></a>
## Use it in the Dark Factory

The Dark Factory takes this crate behind its `bevy_orca` feature for the **crowd preview** (issue #107): it walks N people from one area of a map to another, each stepping with `bevy_orca`'s `Crowd` against its neighbours and against the cells the map's pieces make solid, and lays their trails and congestion into a `bevy_stigmergy` field. The editor draws the result over the map with how many arrived and where congestion peaks, and saves nothing to the map. The settings it passes are the crate's own `CrowdParams`, which are `Serialize`/`Deserialize` behind the `serde` feature.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_orca) · [docs.rs](https://docs.rs/bevy_orca) · [crates.io](https://crates.io/crates/bevy_orca) · [CHANGELOG](https://github.com/dark-incorporated/bevy_orca/blob/main/CHANGELOG.md)
