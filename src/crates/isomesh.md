# isomesh

Signed distance field in, triangles out. An SDF (signed distance field) is a function that returns how far a point is from a surface, negative inside; `isomesh` turns one into a mesh with any of seven extractors, so a voxel world can have caves, arches and overhangs that a heightfield cannot store, and a CAD tool can have `f64` precision from the same crate. Three crates live in the repository: `isomesh` (the engine-free core, `no_std`, one dependency), `bevy_isomesh` (the Bevy plugin and every example) and `isomesh-gpu`.

![Eight examples at once: a field smooth-unioned into a mushroom, caves and arches, letters thinner than a voxel, one cell meshed two ways, Surface Nets against Marching Cubes, terrain being carved, a ball crossing chunk seams, and a slab blown apart](https://raw.githubusercontent.com/bevy-coven/isomesh/main/docs/media/kitchen-sink.gif)

## Add it

```sh
cargo add isomesh        # the core, no engine
cargo add bevy_isomesh   # the Bevy plugin
```

The [README](https://github.com/bevy-coven/isomesh#quick-start) has a quick start compiled on every `cargo test`. Eleven of the demos run in a browser at [bevy-coven.github.io/isomesh](https://bevy-coven.github.io/isomesh/).

## What it gives you

- Seven extractors: Marching Cubes (with MC33's tunnels), Surface Nets, Dual Contouring, Manifold Dual Contouring, Marching Tetrahedra, greedy quads, and subgrid Marching Tetrahedra, which sees features thinner than a voxel ([algorithms](https://github.com/bevy-coven/isomesh/blob/main/docs/demos/algorithms.md)).
- Chunks that tile with no cracks at their seams, streaming, LOD with Transvoxel seams, and meshing off the main thread under a frame budget ([what it can do](https://github.com/bevy-coven/isomesh/blob/main/docs/guide/showcase.md)).
- Validity and accuracy checks as public API: Euler characteristic, manifoldness, orientation, self-intersections, determinism, Hausdorff distance ([what gets checked](https://github.com/bevy-coven/isomesh/blob/main/docs/guide/checks.md)).
- GPU extraction in `isomesh-gpu`, 37 times faster than the CPU at 129³ when the field is evaluated in the shader.

## Use it in Grimoire

Grimoire takes `isomesh` for **carved volumes** (issue #101): a volume's edit list is the data, and the editor samples it over the ground one chunk at a time, each chunk sharing its boundary plane with its neighbour so the mesh has no cracks, and meshes it with `isomesh`. That is how caves, overhangs and tunnels a heightfield cannot hold get onto a map, and how `bevy_elements`' terrain gets them too.

## Links

- [Repository](https://github.com/bevy-coven/isomesh) · [The guide](https://github.com/bevy-coven/isomesh/blob/main/docs/guide/README.md) · [docs.rs](https://docs.rs/isomesh) · [docs.rs (bevy_isomesh)](https://docs.rs/bevy_isomesh) · [crates.io](https://crates.io/crates/isomesh) · [CHANGELOG](https://github.com/bevy-coven/isomesh/blob/main/CHANGELOG.md)
