# bevy_carnage

Runtime gore for Bevy characters, deterministic to the bit. Add a plugin, dress a loaded character with one component, and send a `GoreHit` per injury: a wound peels through skin, fat and muscle to bone, bleeds along the pose of an animated body, pools on the floor and dries, and a body that takes enough comes apart into watertight-capped chunks. A violence setting the player controls is honoured, and every canvas is owned by the CPU, so a whole fight can be hashed and replayed.

![A textured blocked-out body takes a blow, a burn, a slash and shots to the chest; the wounds bleed and pool, and the body comes apart](https://raw.githubusercontent.com/bevy-coven/bevy_carnage/main/docs/preset.gif)

## Add it

```sh
cargo add bevy_carnage
```

The [README](https://github.com/bevy-coven/bevy_carnage#quick-start) has an 18-line quick start that is compiled on every `cargo test`; the [full quick start](https://github.com/bevy-coven/bevy_carnage/blob/main/docs/guide/quick-start.md) covers the flesh material, skinned characters, cost, the violence tiers and baking a fracture by hand. Putting it on a real glTF character has a [checklist](https://github.com/bevy-coven/bevy_carnage/blob/main/docs/preset.md).

## What it gives you

- The preset: `GorePlugin`, `Gore` and `GoreScene` to dress surfaces, `GoreHit` for impacts, blows, burns and slashes, and `GorePolicy` for the player's violence setting.
- The fracture: bake once with `FractureSubject`, then query a hierarchy and a bond graph per blow, with two meshes per fragment and convex colliders ([the API](https://github.com/bevy-coven/bevy_carnage/blob/main/docs/guide/api.md)).
- Seven kernels as modules: `bloodstain`, `wetmap`, `viscera`, `cross_section`, `flaymap`, `laceration` and `fracture_modes` ([the family](https://github.com/bevy-coven/bevy_carnage/blob/main/docs/guide/family.md)).
- A recorded [gallery](https://github.com/bevy-coven/bevy_carnage/blob/main/docs/gallery.md) of every demo.

## Use it in Grimoire

Grimoire takes this crate behind its `bevy_carnage` feature for **destructible props** (issue #108). `destructible_set` marks a piece destructible and fractures it once with the crate's own `fracture_mesh` over its mesh and a box proxy of its bounds, caching the chunks in the project (`destructible/<piece>.bake.ron`, keyed by the mesh's bytes and the cut settings, so it never bakes twice). `destructible_hit` previews a hit on the cached chunks and reports which break loose and whether each is a closed solid, by the crate's own audit. The violence dials are the crate's own `GorePolicy`, saved as `family/bevy_carnage.ron` through `family_set`; the editor itself ships no gore.

## Links

- [Repository](https://github.com/bevy-coven/bevy_carnage) · [docs.rs](https://docs.rs/bevy_carnage) · [crates.io](https://crates.io/crates/bevy_carnage) · [CHANGELOG](https://github.com/bevy-coven/bevy_carnage/blob/main/CHANGELOG.md)
