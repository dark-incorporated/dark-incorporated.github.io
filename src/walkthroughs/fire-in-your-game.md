# Add fire to your game

By the end of this page a fresh `cargo new` game has a lit campfire with a flickering light, using `bevy_lights` on its own.

## Preview

![Four braziers with real lights of their own and 48 torch-bearers sharing an 8-light pool, their flames leaning back as they walk](https://raw.githubusercontent.com/dark-incorporated/bevy_lights/main/docs/media/showcase.gif)

*The crate's courtyard example: this page builds one fire of that scene.*

## Demonstration

### 1. Make a game (2 minutes)

```sh
cargo new fire_game && cd fire_game
cargo add bevy
cargo add bevy_lights
```

### 2. Add the plugins and one fire (3 minutes)

Replace `src/main.rs` with:

```rust,ignore
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

`Fire::lit(kind, lux, over)` is a whole fire in one component: the kind's flame, the light the pool hands it, sparks, smoke, tongues and a bed of coals. `MyFocus` marks the entity the pool ranks lights around, usually the camera or the player.

### 3. Run it (1 minute)

```sh
cargo run --release
```

### 4. Try another kind of fire (2 minutes)

Change `FireKind::Campfire` to another kind. The crate's own `fires` example shows six, from a candle to a bonfire:

```sh
LIGHTS_KIND=bonfire cargo run --release --example fires
```

Run that from a clone of [`bevy_lights`](https://github.com/dark-incorporated/bevy_lights).

## Review

- `bevy_lights` works alone: add the crate, add its plugins, spawn a `Fire`.
- A pool of real lights is shared over many fires, so a scene with a thousand torches still shades only a budgeted number.
- The Dark Factory can place the same `Fire` component on a map; see [Using a crate with the Dark Factory](../with-cauldron.md).

Next: [drive a running game from an agent](drive-a-running-game.md).
