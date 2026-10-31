# bevy_flora

`bevy_flora` is the coven's trees: parametric, stylized procedural trees for Bevy 0.20 that grow over time. A tree is a `TreeParams` value with a seed in it — one of 20 presets or every field tuned by hand — and the same value makes the same tree on every run, at every age. Twenty thousand of them draw from a pool of a few seed variants in under 4 ms a frame, and they can be notched, felled, bucked, burnt, shaken and picked like game objects rather than looked at like scenery.

![A maple growing from a bare trunk into a full crown while the camera circles it](https://github.com/bevy-coven/bevy_flora/raw/HEAD/docs/media/growth.gif)

## Add it

```sh
cargo add bevy_flora
```

Add the plugin and spawn a tree. `Growing` advances its age every frame until it is mature; leave it off and set `TreeAge` yourself.

```rust,no_run
use bevy::prelude::*;
use bevy_flora::{FloraPlugin, Growing, ProceduralTree, TreeAge, TreePreset};

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, FloraPlugin))
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands) {
    let mut params = TreePreset::Maple.params();
    params.seed = 7;
    commands.spawn((ProceduralTree(params), TreeAge(0.0), Growing::default()));
    commands.spawn((DirectionalLight::default(), Transform::from_xyz(10.0, 20.0, 10.0).looking_at(Vec3::ZERO, Vec3::Y)));
    commands.spawn((Camera3d::default(), Transform::from_xyz(0.0, 5.0, 20.0).looking_at(Vec3::new(0.0, 4.0, 0.0), Vec3::Y)));
}
```

`cargo run --release --example showcase` is the same thing with the controls wired up; the README's quick start and its doctests are the version CI compiles.

## What it gives you

- **A tree over any age.** `TreeAge` and `Growing` on the CPU, or `GpuGrowth` for two hundred oaks at 0.81 ms a frame — [growing](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/growing.md).
- **A forest.** `TreePool` and `PooledTree` with three levels of detail and baked impostors, `BackgroundPools` to build them off the frame, `PoolColors` for more than one look, `Scatter` for where the trees stand, `FloraGround` for the terrain, `FloraUnits` for a world that is not in metres — [forests](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/forests.md).
- **A look.** Bundled CC0 bark scans and real leaf outlines, veins grown by space colonisation, `Natural`, `Painterly` and `Toon` styles, and low-poly `CrownStyle::Hull` conifers — [bark, leaves and looks](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/appearance.md).
- **A year.** `FloraSeason` for autumn colour, leaf fall, snow and blossom, fruit through summer, and `FloraWetness` for rain — [seasons](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/seasons.md).
- **Things that happen to trees.** `TreeShakes`, `DropLeaves`, `TreeFruit`, `TreeNotch` and `FellTree`, `BuckTree`, `FloraFire` and `FoliagePusher` — [interaction](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/interaction.md).
- **Answers for the game.** `TreeShape` for colliders, `FloraIndex` (nearest tree, trees within a radius, the trunk a ray meets), `TreeCondition` for sick and dying trees, and what a save holds — [gameplay](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/gameplay.md).
- **Cameras.** `SeeThroughTrees` to keep the player visible, and orthographic cameras whose levels of detail follow the zoom — [cameras](https://github.com/bevy-coven/bevy_flora/blob/main/docs/guide/camera.md).

## Use it in Grimoire

Grimoire takes this crate as the optional cargo feature `bevy_flora` (pinned to a git revision of `main`, with the crate's `ron` feature on). With the feature off, the two operations are still registered and refuse, naming the feature, so the editor's surface does not change with the build.

Two operations, both writing files the game loads with the crate on its own:

- **`tree_edit`** writes `<grimoire_dir>/trees/<name>.tree.ron`, which is `TreeParams` in the format `TreeParamsLoader` reads. `preset` starts the file from one of the 20 presets (by name, through `TreePreset::from_name`); `set` changes fields by dotted path into `TreeParams` — `trunk.radius`, `branches.density`, `foliage.scan`, `crown`, `trunk_style`, `style`, `wind`, `bark` — and a path the crate does not know is refused with the crate's own message, so a typo is never written. The settings are the crate's serde types; the editor defines no second schema for them. A tree that shares the file regrows after an edit with nothing to recompile, which is `ProceduralTreeAsset` and the `file_watcher`.
- **`forest_scatter`** writes `<grimoire_dir>/forest/<map>.ron`: one `Tree` per trunk — an id, a species (a preset name or a `.tree.ron` path), its `(x, z)`, its ground height, its scale, its seed and its pool variant — masked to the stroke the author drew. The editor plants it with the crate's own `Scatter` (its Poisson-disc spacing, groves and species weights, its seed) and stands each trunk on the map's terrain with `FloraGround`.

In the viewport the trees are always the crate's: a scattered trunk is a `PooledTree` of its species' `TreePool`, built with `BackgroundPools`; a tree placed by hand is a `ProceduralTree` at its own `TreeAge` and seed, so the same seed grows the same tree in the editor and in the game. The preview's `FloraSeason` follows `bevy_elements`' `WorldClock`, so the month set in the environment panel turns the forest from blossom to leaf to autumn to snow.

Not yet a panel: `FloraFire`, `TreeCondition` and `SeeThroughTrees` have no editor surface — a fire's grid (`FloraFire::cells`) and a tree's condition would each be a file beside the forest's, restored with `FloraFire::with_cells` and `restore` and with `insert(TreeCondition::Sick)`.

## Links

- [The repository](https://github.com/bevy-coven/bevy_flora)
- [API docs on docs.rs](https://docs.rs/bevy_flora)
- [crates.io](https://crates.io/crates/bevy_flora)
- [The guide](https://github.com/bevy-coven/bevy_flora/tree/main/docs/guide) and [the gallery](https://github.com/bevy-coven/bevy_flora/blob/main/docs/gallery.md)
- [CHANGELOG](https://github.com/bevy-coven/bevy_flora/blob/main/CHANGELOG.md)
