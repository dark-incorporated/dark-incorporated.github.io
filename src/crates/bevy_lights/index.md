# bevy_lights

Practical lights for Bevy 0.20: the fires a scene's props actually carry. A world can hold thousands of
torches and afford a dozen real lights, so this crate ranks the candidates by the light they put on you,
hands the budget out without a pop, modulates each light the way a fire's light moves, and draws the
flame that motivates it — with sparks, smoke, tongues for a wide fire and a bed of coals that goes on
glowing after the fire is put out.

![Four braziers with real lights of their own and 48 torch-bearers sharing an 8-light pool, their flames leaning back as they walk](https://github.com/bevy-coven/bevy_lights/raw/HEAD/docs/media/showcase.gif)

## Add it

```sh
cargo add bevy_lights
```

```rust,no_run
use bevy::prelude::*;
use bevy_lights::*;

#[derive(Component)]
struct MyFocus;

fn main() {
    App::new()
        .add_plugins(DefaultPlugins)
        .add_plugins((FlickerPlugin, LightPoolPlugin::<MyFocus>::default(), FlamePlugin, FirePlugin))
        .add_systems(Startup, |mut commands: Commands| {
            let fire = Fire::lit(FireKind::Campfire, 250.0, 0.35);
            commands.spawn((fire, Transform::from_xyz(4.0, 0.0, 2.0)));
            commands.spawn((MyFocus, Transform::default()));
        })
        .run();
}
```

`Fire::lit(kind, lux, over)` is a whole fire in one component: the kind's flame, the light the pool hands
it, its sparks, smoke, tongues and bed of coals. Or run it first: `cargo run --release --example courtyard`.

## What it gives you

- **Fires that flicker, flare and go out** ([fires](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/fires.md)): `Flicker` dips a light below its base at the rate its fuel bed sets, `Kindle` flares it up over 0.6 s, `Snuff` puts it out over 1.2 s with the linked flame.
- **A budget of real lights for a town of thousands** ([the light pool](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/light-pool.md)): ranked by the light each candidate puts on you, held with hysteresis, cross-faded on a hand-off, with a shadow budget of its own and one template that reaches every light live.
- **The flame drawn where the fire is** ([shader flames](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/flames.md)): one additive billboard per fire, breathing on its light's clock, in a hue of its own, shedding sparks, smoking, leaning in a wind and streaming behind a torch you carry — and going out when a wall hides its source.
- **Coals that outlive the flame** ([the fuel bed](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/fuel-bed.md)): a temperature field that breathes with the flicker, warms as the fire catches and cools over a minute once it is put out.
- **A cinematographer's numbers** ([the lighting look](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/lighting-look.md)): `fire_lumens`, `fill_for`, `blackbody_colour` and `white_balanced` turn "1000 lx at 4 m" and "1900 K" into a sized, coloured light.
- **Every curve outside the engine** ([engine-free maths](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/model.md)): the same maths as plain `f32` functions with no `bevy` in them, for a host that drives its own lights.
- **What a host touches, and what it saves** ([host API](https://github.com/bevy-coven/bevy_lights/blob/main/docs/guide/host-api.md)): the components and resources a game spawns, marks and reads, and the `serde` feature that makes a placed fire one line of a scene file.

![The six fire kinds, each one Fire component, with its flame, the pool its light throws on the ground, and its own sparks, smoke, tongues and coals](https://github.com/bevy-coven/bevy_lights/raw/HEAD/docs/media/fires.png)

<a id="use-it-in-grimoire"></a>
## Use it in the Cauldron

The Cauldron, the Coven's level editor, takes `bevy_lights` as an optional cargo feature (`bevy_lights`) and a
project lists it in its `family.ron`. Two things it does with the crate today:

- **A placement's fire is the crate's own settings type.** `family_set` writes a field of the fire's
  `Flicker` — `base`, `phase`, `depth`, `diameter` — in `<project>/family/bevy_lights.ron`, and the placed
  prop reads back as the crate's `Flicker`, so the editor has no schema of its own for it.
  `placement_set_family` puts that value on one placement, or takes it off.
- **Two read-only operations answer "which of my torches are real, and how lit is this tile?"** — `light_pool`
  runs the crate's own `LightPoolPlugin` over the map's fixtures and reads its `PoolBudget` for where the
  viewer stands, and `light_map` bakes a `bevy_light_grid` illuminance field from the same fixtures.

There is no panel for the fire kinds yet. One would edit `Fire { kind, lumens, phase, color, embers, smoke,
tongues, bed }` — the whole fire as one serde value — and read `Fire::problems()` beside the fields, which
is what every settings type in the crate returns: a list of `Problem { field, kind }` naming what cannot
work, before the value reaches a light.

## Links

- [Repository](https://github.com/bevy-coven/bevy_lights)
- [docs.rs](https://docs.rs/bevy_lights)
- [crates.io](https://crates.io/crates/bevy_lights)
- [CHANGELOG](https://github.com/bevy-coven/bevy_lights/blob/main/CHANGELOG.md)
- [Capture recipes](https://github.com/bevy-coven/bevy_lights/blob/main/docs/DEMOS.md) · [every image in `docs/media/`](https://github.com/bevy-coven/bevy_lights/blob/main/docs/media/README.md)
