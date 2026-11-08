# bevy_society

Living societies for Bevy: villagers who remember, gossip, take sides, fall out and make up. Big Five personalities, moods on a pleasure/arousal/dominance axis, an OCC emotion set, needs that decay and memories that fade; utility-AI daily lives over tagged places and other people; directed ties with a Dunbar-style cap; opinions, rumors, reputation and factions; Rhai scripts, dialogue through `bevy_speech_bubbles`; and a save that restores the society the reload would have produced.

![A rumor spreads through a village: green tie lines thicken between villagers, one red rivalry line appears, and a magenta ring marks who knows the rumor](https://github.com/dark-incorporated/bevy_society/raw/HEAD/docs/media/village.gif)

*`cargo run --release --example capture -- --scene village`: one afternoon in a village of twenty-four people. The plate reads `Day 4 · 14:01  Friendships 30 · Rivalries 1` on the first frame and `Day 4 · 20:01  Friendships 27 · Rivalries 1` with `“Bram stole bread” — known by 2/24` on the last.*

## Add it

```sh
cargo add bevy_society
```

```rust
use bevy::prelude::*;
use bevy_society::{
    Autonomous, Home, Person, Place, PlaceTags, SocietyClock, SocietyDefs, SocietyPlugins,
    SocietySettings,
};

let defs = SocietyDefs::starter().expect("the starter pack is valid");
// A headless app has no frame clock, so `Time<Fixed>` never advances on its own. Without this the
// society takes zero ticks however many updates you run.
let step = std::time::Duration::from_secs_f64(1.0 / 64.0);

let mut app = App::new();
app.add_plugins((MinimalPlugins, TransformPlugin))
    .insert_resource(bevy::time::TimeUpdateStrategy::ManualDuration(step))
    .insert_resource(SocietySettings::default())
    .insert_resource(defs);
// `DialoguePlugin` needs a speech-bubbles plugin over a camera, which this snippet has not.
let plugins = SocietyPlugins.build();
#[cfg(feature = "dialogue")]
let plugins = plugins.disable::<bevy_society::DialoguePlugin>();
app.add_plugins(plugins);

let well = app
    .world_mut()
    .spawn((Name::new("well"), Place { capacity: 6 }, PlaceTags(vec!["gathering".into()]), Transform::default()))
    .id();
for name in ["Bram", "Alys", "Corin"] {
    app.world_mut()
        .spawn((Person, Autonomous, Name::new(name), Home(well), Transform::default()));
}

for _ in 0..600 {
    app.update();
}
// The society advanced: this line is what proves the fixed step was pinned.
assert!(app.world().resource::<SocietyClock>().tick > 0);
```

With the default `dialogue` feature, `DialoguePlugin` panics in `finish` without `bevy_speech_bubbles::SpeechBubblesPlugin::<YourCamera>` over a camera; add that first, or `.disable::<DialoguePlugin>()` as above.

## What it gives you

- **People with a mind.** Big Five personalities, PAD mood, OCC emotions, decaying needs, fading memories, and a `Chronotype` so a lark and an owl keep their own hours in one village. [features](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/features.md#people-with-a-mind)
- **A day they choose.** Utility-AI scoring over tagged places and other people, with travel, arrival, durations, per-tier ranks and an urgency that wins the tier while a need is low. [features](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/features.md#daily-life-and-trades)
- **Relationships.** Directed ties with affinity, trust, respect and familiarity, a Dunbar-style cap, friend and rival labels with hysteresis, and rebuff memory so someone turned down stops asking. [features](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/features.md#relationships)
- **Opinions, rumors, reputation and factions.** Bounded-confidence influence, Daley–Kendall gossip, witnesses who judge deeds and hold grudges, in-group affinity and conferred standing. [features](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/features.md#opinions-rumors-reputation-and-factions)
- **Scripts.** Rhai triggers over a per-tick snapshot, bound to an area, a faction or named people, with a `ctx` reader and an `fx` writer that cannot see its own writes. [scripting](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/scripting.md)
- **An economy and a save file.** Goods as quantities with a per-head price, sharing and swapping between people, and `capture`/`restore` of the whole society. [features](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/features.md#a-basic-economy) · [persistence](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/persistence.md)
- **An editor's handles.** `fast_forward`, `preview_forward` (run a day, report what moved, put it back), `test_trigger`, `check_script`, `place_dependents` and `persons_in_rect`. [editor](https://github.com/dark-incorporated/bevy_society/blob/main/docs/guide/editor.md)

<a id="use-it-in-blueprint"></a>
## Use it in the Dark Factory

The Dark Factory takes `bevy_society` as an optional cargo feature, named `bevy_society` in `Cargo.toml` and in a project's `family.ron`. When the project lists it, the editor:

- **writes the crate's own settings** through `family_set`, which rewrites one dot-pathed field of the RON file the crate's serde types parse — the editor holds no schema for them, so it keeps the rest of the file as the author left it;
- **refuses a definitions file the crate would reject**: a saved society definition goes through `bevy_society::SocietyDefs::from_ron` first, so a file the loader would not compile is never written;
- **authors people on a map** through `person_set` (`<emerge_dir>/people/<map>.ron`), with a name, a position, a faction the project's definitions declare, a home, a workplace and starting ties;
- **runs a map's people forward** through `people_run`, which spawns them in `bevy_society`'s own headless app and reports where each went and which ties moved — the crate's systems decide, the editor adds no behaviour.

A settings panel for this crate would edit `SocietySettings` (seed, `tick_secs`, `seconds_per_day`, `start_hour`, `start_weekday`, the clock source, locomotion, the society plane and the perception, contact and interaction radii), the tie capacities (`max_ties`, `close_ties`), the memory and knowledge capacities, and the rates on `Tuning` — every one of which is `Serialize` through the crate's settings types. `SocietyDefs` itself is authored as a `DefsFile` in RON, and `DefsFile::to_ron` exists so an editor can save what it edited.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_society)
- [docs.rs](https://docs.rs/bevy_society)
- [crates.io](https://crates.io/crates/bevy_society)
- [CHANGELOG](https://github.com/dark-incorporated/bevy_society/blob/main/CHANGELOG.md)
