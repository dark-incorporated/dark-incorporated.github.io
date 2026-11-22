# bevy_gooey

Game interfaces made easy for Bevy 0.20: a skin, ready-made game widgets and keyboard and gamepad
navigation, built on Bevy's own headless widgets (`bevy_ui_widgets`) and input focus
(`bevy_input_focus`). A menu is a few nested calls, every widget looks like one family, and a pad or a
keyboard reaches everything a mouse does — with the WCAG 2.2 contrast and target-size checks the crate
runs on your own skin.

![Walking a menu with the keyboard: focus moves down the panel onto Options, the health meter drains, then the Load game list scrolls to follow focus and a toast appears](https://github.com/bevy-coven/bevy_gooey/raw/HEAD/docs/media/gallery.gif)

## Add it

```sh
cargo add bevy_gooey
```

```rust
use bevy::prelude::*;
use bevy_gooey::*;

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, GooeyPlugins))
        .add_systems(Startup, setup)
        .run();
}

fn setup(mut commands: Commands) {
    commands.spawn(Camera2d);
    commands.spawn((
        screen(),
        children![(
            panel(),
            children![
                heading("Paused"),
                (
                    menu(),
                    children![
                        (button("Resume"), observe(|_: On<Activate>| info!("resume"))),
                        button("Quit"),
                    ]
                ),
            ]
        )],
    ));
}
```

Or run the gallery first: `cargo run --example gallery`.

## What it gives you

- **A skin as data** ([skins](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/gooey.md)):
  `GooeySkin` holds every colour and size, with the `dark` and `parchment` presets and `problems()`,
  which checks WCAG 2.2 contrast and target size. Change it and everything restyles that frame. Fonts
  live in `GooeyFonts`, never in the skin.
- **Every widget a game screen needs** ([the widget set](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/gooey.md)):
  `screen`, `panel`, `menu`, `heading`, `label`, `button`, `meter` (a HUD bar), `toggle`, `choice`,
  `slider`, `list`, `toast`, `toast_alert`, `Tooltip` and the modal `dialog` — each a free function
  returning a bundle, so they compose in `children![]` and with `observe`.
- **Settings controls that are the widget** ([controls](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/controls.md)):
  a `toggle`, `choice` and `slider` each root on Bevy's own `Checkbox`, `Button` and `Slider`, so the
  entity you spawn carries the value, takes `observe` and says each change once in `ValueChange`.
- **A list that scrolls and follows focus** ([lists](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/list.md)):
  `list(4.5, children![..])` shows four rows and a half, cuts the fifth so the player sees there is
  more, and keeps the next row in sight as the arrows walk down it.
- **Navigation with no mode to enter** ([focus](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/focus.md)):
  arrows and the D-pad move focus to the nearest widget, Enter, Space and South activate, Tab cycles,
  an open dialog holds focus, and the focus ring appears the moment a key is pressed.
- **Toasts that read at the player's pace** ([toasts](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/toast.md)):
  `commands.spawn(toast("Game saved"))` and it stacks, times itself to its own length and ages on real
  time, so a paused game's menu still lets it go.
- **One interface at every resolution** ([scale](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/scale.md)):
  `GooeyScalePlugin` keeps the skin's sizes the same share of the screen, and every border is a whole
  number of device pixels at any scale.
- **A pointer that passes through a HUD** ([over a game world](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/research/pointer.md)):
  the empty part of a `screen` is `Pickable::IGNORE`, so a click on the world under a HUD still
  reaches the world.

<a id="use-it-in-grimoire"></a>
## Use it in the Cauldron

The Cauldron, the Coven's level editor, takes `bevy_gooey` as an optional cargo feature (`bevy_gooey`) and
a project lists it in its `family.ron`. It adds the crate's `GooeyStylePlugin` (not `GooeyNavPlugin`:
the editor owns the arrow keys) and reads a project's skin from `<project>/family/bevy_gooey.ron`, which
is the crate's own `GooeySkin` type written as RON — the same file a game ships:

```ron
(accent: Srgba((red: 0.2, green: 0.6, blue: 0.9, alpha: 1.0)), text_scale: 1.25)
```

`GooeySkin` is `#[serde(default)]`, so a partial file is the default skin with only that field changed.
Editing the file live swaps the running `GooeySkin` resource and the crate's own `apply_skin` restyles
every widget that frame; a file that is not a skin is a problem on the status line and the last good
skin stays; a skin that breaks the crate's own rules is applied and each broken rule
(`GooeySkin::problems()`) is a problem. Removing the file puts the default skin back.

There is no panel for the skin yet. One would edit `GooeySkin`'s fields — the colours (`background`,
`surface`, `surface_raised`, `text`, `text_muted`, `accent`, `accent_text`, `danger`, `focus_ring`,
`outline`, `scrim`), the sizes (`text_size`, `heading_size`, `gap`, `padding`, `radius`, `border`,
`meter_height`, `min_target`) and the player's `text_scale` — with `problems()` listed beside them, and
it would read `UiScaleSettings { reference_short_side, scale }` and `ToastSettings { anchor,
max_visible, base_seconds, chars_per_second, duration_scale, fade_seconds }` the same way: each is
serde data, so each is one line of the project's `family/` folder.

## Links

- [Repository](https://github.com/bevy-coven/bevy_gooey)
- [docs.rs](https://docs.rs/bevy_gooey)
- [crates.io](https://crates.io/crates/bevy_gooey)
- [CHANGELOG](https://github.com/bevy-coven/bevy_gooey/blob/main/CHANGELOG.md)
- [Every image in `docs/media/`](https://github.com/bevy-coven/bevy_gooey/blob/main/docs/media/README.md)
