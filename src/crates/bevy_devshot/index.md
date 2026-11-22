# Devshot

A frame on demand: touch a sentinel file and the next frame writes a PNG, straight from the GPU.

## Add it

```sh
cargo add bevy_devshot --git https://github.com/dark-incorporated/bevy_devshot
```

```rust,ignore
#[cfg(debug_assertions)]
app.add_plugins(bevy_devshot::DevShotPlugin);
```

## What it gives you

- A screenshot from anything that can touch a file: a person over SSH, a Makefile, CI, a capture script, or an agent driving your game.
- One `Path::exists` poll per frame and nothing else, so it costs next to nothing while idle.
- A single example, `cargo run -p bevy_devshot --example capture`, that opens a spinning cube and writes `screenshot.png` after `touch screenshot.request`.

## Use it in the Dark Factory

Which crates the Dark Factory hosts, and how it edits a crate's settings, is on [Using a crate with the Dark Factory](../../with-cauldron.md). This crate has no settings to edit; use it on its own: [Using a crate on its own](../../alone.md).


## Guide

This crate has no guide pages yet; its [README](https://github.com/dark-incorporated/bevy_devshot#readme) is the whole API.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_devshot) · [CHANGELOG](https://github.com/dark-incorporated/bevy_devshot/blob/main/CHANGELOG.md)
