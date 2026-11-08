# bevy_speech_bubbles

A dialog kit for Bevy: world-space speech and thought balloons that float over their speakers, a conversation graph with a runtime, paced barks, and a skinnable screen dialog box. Balloons are quads in the scene rather than a UI layer, so they hold a world position, can be hidden behind a wall, and turn to face the camera.

![Five coloured figures in a ring while the camera orbits; speech and thought balloons appear above them and fade](https://raw.githubusercontent.com/dark-incorporated/bevy_speech_bubbles/main/docs/chatter.gif)

## Add it

```sh
cargo add bevy_speech_bubbles
```

The [README](https://github.com/dark-incorporated/bevy_speech_bubbles#quick-start) has a quick start that is compiled on every `cargo test`. Your game names the camera balloons face with a marker component, and loads its own font.

## What it gives you

- Balloons (`build_bubble`, `track_bubbles`, `BalloonSkin`, `BalloonScale`), including pixel-perfect ones ([balloons](https://github.com/dark-incorporated/bevy_speech_bubbles/blob/main/docs/guide/balloons.md)).
- A `DialogueScript` of `Line` and `Choice` nodes, loaded from RON or any serde format, strict about unknown keys, and checked by `validate_script` ([conversations](https://github.com/dark-incorporated/bevy_speech_bubbles/blob/main/docs/guide/conversations.md)).
- A runtime driven by `StartConversation`, `ChoicePicked` and `ConversationEnded`, with `DialogueNodeEntered` for effects, and two presenters: balloons or the dialog box.
- `Bark`s with `BarkSettings` pacing, and a 9-sliced `DialogSkin` with portrait, name tag and typewriter.

<a id="use-it-in-blueprint"></a>
## Use it in the Dark Factory

The Dark Factory takes this crate behind its `bevy_speech_bubbles` feature and keeps a project's dialogue as the crate's own `DialogueScript` in `family/bevy_speech_bubbles.ron`, with barks as `Vec<Bark>`. `family_set` writes them and runs `validate_script` before anything is saved, so a dangling `next` or a missing start node is refused with nothing written. `dialogue_preview` walks one path through a conversation, taking the options you name at each choice, and answers with the lines said, where the walk stopped and which nodes no path reaches, without changing a file. People placed with `bevy_society` speak these lines.

## Links

- [Repository](https://github.com/dark-incorporated/bevy_speech_bubbles) · [docs.rs](https://docs.rs/bevy_speech_bubbles) · [crates.io](https://crates.io/crates/bevy_speech_bubbles) · [CHANGELOG](https://github.com/dark-incorporated/bevy_speech_bubbles/blob/main/CHANGELOG.md)
