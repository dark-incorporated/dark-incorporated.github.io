# bevy_light_grid

An illuminance grid that creature AI can read. It answers "how bright is it here, and which way is brighter" per cell, on the CPU, so a creature can flee into shadow or climb toward a lamp. Your GPU lighting already knows how bright each pixel is, but that answer lives in a framebuffer gameplay cannot read; this crate computes it in a form gameplay can sample and differentiate.

![A flashlight wedge sweeps a dark room; pale creatures flee the beam while amber ones move into it](https://raw.githubusercontent.com/bevy-coven/bevy_light_grid/main/docs/beam.gif)

## Add it

Not on crates.io yet:

```toml
[dependencies]
bevy_light_grid = { git = "https://github.com/bevy-coven/bevy_light_grid" }
```

The [README](https://github.com/bevy-coven/bevy_light_grid#quick-start) has a quick start that is compiled on every `cargo test`. The crate takes `bevy_math` and `bevy_ecs` and nothing that draws.

## What it gives you

- `LightGrid` with `bake` (static lamps, rerun when one changes) and `compose` (moving `FlashlightCone`s on the cached bake, every tick), both shadowed by your own line-of-sight closure ([the field](https://github.com/bevy-coven/bevy_light_grid/blob/main/docs/guide/the-field.md)).
- `sample_cell` and `gradient_cell`, and `light_push_at` for a steering push up or down the gradient.
- `Photophobic`, `Photophilic` and `Phototropic` markers, and `phototropic_scale` for growth toward light.

<a id="use-it-in-grimoire"></a>
## Use it in the Cauldron

The Cauldron takes this crate behind its `bevy_light_grid` feature for the **light map** (issue #103), a read-only operation and overlay. Every placement that carries a `bevy_lights` `Flicker` is a fixture, a placement whose descriptor is a wall blocks line of sight, and the values drawn over the map are the crate's own `LightGrid::sample_cell`, so what the author reads is what a light-shy creature in the game reads.

## Links

- [Repository](https://github.com/bevy-coven/bevy_light_grid) · [Guide](https://github.com/bevy-coven/bevy_light_grid/blob/main/docs/guide/README.md)
