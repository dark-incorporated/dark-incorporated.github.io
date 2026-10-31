# bevy_elements

Living environments for Bevy 0.20: a sun and moon on real ephemerides, the bright-star sky, a seeded climate that schedules hourly weather, a GPU wind field, volumetric clouds, rain and snow, lightning and thunder, fog, heightfield terrain with erosion and flooding, ground cover, rocks, dust, paths and trails — all in compute shaders. Everything runs behind one `Environment` system parameter, so gameplay asks the simulation what the ground, the water, the light and the weather are doing instead of guessing at it.

![The ten weather presets forced in turn, the clock running from 10.00 h on 20 April 2026](https://github.com/bevy-coven/bevy_elements/raw/HEAD/docs/media/tour_hero.gif)

## Add it

```sh
cargo add bevy_elements
```

```rust,no_run
use bevy::prelude::*;
use bevy_elements::*;

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, ElementsPlugins))
        .insert_resource(WorldClock::new(CivilDate::new(2026, 6, 21)).at_hour(7.0))
        .insert_resource(Climate::temperate())
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands) {
    // The environment follows and renders for the `ElementsCamera`.
    commands.spawn((
        Camera3d::default(),
        ElementsCamera::default(),
        Transform::from_xyz(0.0, 160.0, 0.0).looking_at(Vec3::new(100.0, 100.0, 0.0), Vec3::Y),
    ));
    // 2 km of rolling hills, centred on the origin.
    commands.spawn(Terrain::procedural(ProceduralTerrain::hills(42)));
}
```

Or run it first: `cargo run --release --example quickstart`.

## What it gives you

- **A living sky over any scene** — sun, moon and 8 404 stars from real ephemerides, with exposure that keeps night dark: [sky, weather and light](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/sky-weather.md).
- **A seeded climate that schedules the weather** — `Clear` through `Blizzard`, hourly, with seasons and a snow season a game sets by date: [climate, seasons and weather](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/sky-weather.md#climate-seasons-and-weather).
- **Rain, snow, fog and lightning that read from every camera** — including orthographic and isometric views, through `PrecipitationLook::readable()`: [precipitation](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/sky-weather.md#precipitation).
- **A terrain you generate, sculpt and save** — procedural presets, a height map or flat ground, brushes on the live heightfield, snapshots to save and restore: [terrain](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/terrain.md).
- **Ground that wears** — drifting snow and melt, wetness and puddles, blown sand, trodden paths, pressed footprints: [ground cover](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/terrain.md#ground-cover).
- **Water that answers** — shallow-water hydrology with erosion, lakes and rivers, wakes from anything moving through: [rivers, lakes and waves](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/water.md).
- **A simulation gameplay can query** — ground height and normal, water depth and velocity, snow depth, cloud shadow, the lumens a night lamp needs: [gameplay queries](https://github.com/bevy-coven/bevy_elements/blob/main/docs/guide/queries.md).

## Use it in Grimoire

Grimoire takes bevy_elements as the optional cargo feature `bevy_elements` (the volume snow feature builds on it as `volume_snow`), and its **map environment** panel edits this crate's own serde types, written to `<project>/family/bevy_elements.ron` so the editor's preview and the game read the same values:

- `WorldClock`, `GeoLocation` and `Climate` — the date, the clock, where the observer stands and the climate the scheduler draws from.
- `WeatherPreset` as `forced_weather` — `Some(Rain)` forces one preset and `None` releases the weather back to the climate's own schedule, so a map can be authored under a storm and played under whatever the season brings.
- `SnowSettings`, `WetnessSettings`, `RockSettings` and `DustSettings` — how the snow settles, drifts and melts; how the ground wets and puddles; how many rocks lie on the ground; how the sand moves.
- `SurfaceCover` as `volume_cover` — a fixed snow and wetness a carved `bevy_isomesh` volume wears whatever the weather is, which is what a preview of a snow-capped cliff needs.

The editor also builds a map's heightfield from `ProceduralTerrain`'s presets (`hills`, `mountains`, `dunes`, `plains`) and puts `bevy_elements`' `SnowyField` over a carved volume. Nothing outside those types is reachable from the editor yet: `EnvironmentSetup` and `SurfaceSetup` — the whole sky-and-ground setup as one saved, validated value that applies live — are the natural next panel, and the terrain's `TerrainSetup`, `SculptTerrain` and `RestoreTerrain` would give it sculpting and undo.

## Links

- [Repository](https://github.com/bevy-coven/bevy_elements)
- [docs.rs](https://docs.rs/bevy_elements)
- [crates.io](https://crates.io/crates/bevy_elements)
- [CHANGELOG](https://github.com/bevy-coven/bevy_elements/blob/main/CHANGELOG.md)
