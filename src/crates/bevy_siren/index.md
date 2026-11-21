# Siren

Sound for Bevy 0.20 that decides *what* plays and *how loud*: cues with variants, buses that duck, a voice budget that refuses politely, music that changes on the bar, and a log of what played and why.

## Add it

```sh
cargo add bevy_siren
```

```rust,ignore
app.add_plugins((DefaultPlugins, bevy_siren::SirenPlugin));
```

## What it gives you

- A cue table as data: a cue has variants, and the picker never plays the same one twice in a row.
- Buses that duck: dialogue lowers the music without a line of mixing code.
- A voice budget that refuses a sound it has no room for, and says so.
- Music that changes on the bar, and a `SirenLog` that records what played and why.

## Use it in the Dark Factory

Which crates the Dark Factory hosts, and how it edits a crate's settings, is on [Using a crate with the Dark Factory](../../with-cauldron.md). Until this crate has a panel there, use it on its own: [Using a crate on its own](../../alone.md).


## Guide

The guide pages in the sidebar are synced from the crate's `docs/guide/` folder.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_siren) · [docs.rs](https://docs.rs/bevy_siren) · [crates.io](https://crates.io/crates/bevy_siren) · [CHANGELOG](https://github.com/dark-incorporated/bevy_siren/blob/main/CHANGELOG.md)
