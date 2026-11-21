# Presence

Presence for Bevy: the crates a VR game needs to put a player in a room with a character who listens, answers, looks at them and moves its mouth.

## Add it

```sh
cargo add bevy_presence --git https://github.com/dark-incorporated/bevy_presence
```

The repository is a workspace of crates that are each useful alone: the player's rig and hands (`bevy_xr_rig`), locomotion (`bevy_xr_locomotion`), interaction (`bevy_xr_interact`), a UI on a quad in the world (`bevy_world_panel`), chat, speech in and out, lip sync, gaze and a companion that takes turns (`bevy_companion`). `bevy_presence` itself is `PresencePlugins` and the glue between them.

## What it gives you

- A player with tracked head and hands, controller input as plain values, haptics, recentring and a boundary guard.
- A character who listens, answers, looks at the player and moves its mouth.
- Engine-free crates for the parts that need no engine, so they can be tested without a headset.

## Use it in the Dark Factory

Presence is under construction and has no panel in the Dark Factory yet. Which crates the Dark Factory hosts, and how it edits a crate's settings, is on [Using a crate with the Dark Factory](../../with-cauldron.md).


## Guide

This crate has no guide pages yet. `docs/CONTRACTS.md` in its repository says what each crate promises.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_presence) · [CONTRACTS.md](https://github.com/dark-incorporated/bevy_presence/blob/main/docs/CONTRACTS.md)
