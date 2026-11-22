<!-- synced from dark-incorporated/bevy_gooey@6135378; edit it there -->
# Toasts

A toast is one spawn from any system, with no layout and nothing to set up:

```rust
fn save(mut commands: Commands) {
    commands.spawn(toast("Game saved"));
}

fn pickup_failed(mut commands: Commands) {
    commands.spawn(toast_alert("Inventory full"));
}
```

- The first toast creates the one `ToastStack` (a full-window, pointer-transparent column above a `dialog`'s scrim and below a tooltip) and every toast becomes its child in the frame it is spawned. Despawn the entity to take a toast back sooner.
- A toast stands as long as its message takes to read: `(base_seconds + characters ÷ chars_per_second) × duration_scale`, 2.5 s for "Game saved" at the defaults, then fades out and despawns. It runs on real time, so a paused game's menu still ages it. It fades in as the room it holds opens and fades out as that room closes, so the toasts round it glide to make way and close up and none of them jumps.
- A toast slides in as it fades in: it starts 48 px (`TOAST_SLIDE_PX`) toward the window edge its stack is anchored to, below for a bottom anchor and above for a top one, and settles on the skin's `motion.snappy` spring (`MotionTarget`, started by `begin_entrances`). Under reduced motion it only fades, and with no motion it lands. A toast already standing is never moved by one that arrives.
- Offer `ToastSettings::duration_scale` in your settings screen: Xbox Accessibility Guideline 116 asks that a player can stretch the time notifications stay up to at least ten times the default (any value above zero works). `fade_seconds: 0` removes the fade and the opening of room for a player who wants no motion. `max_visible` (3) sends the oldest into its fade when a fourth arrives, and `anchor` picks one of six places (bottom centre by default); the newest stands nearest the edge. `inset` keeps the stack off the window's edges, logical px on each side: `ToastInset::top(34.0)` with `ToastAnchor::TopCenter` stands the toasts under a 34 px menu bar (with the stack's own padding below it), and `ToastInset::bottom(..)` keeps them above a status band; rewrite it when the bar's height changes.
- A toast takes no input and no focus: every node of it is `Pickable::IGNORE`, it is no tab stop, and a press, a key or a D-pad direction goes to what is under it. (A toast you give a button, below, has that button and nothing else that does.) The mark down its left edge is the accent for `toast` and `danger` for `toast_alert`; the words carry the kind too. `GooeySkin::problems()` checks both marks against the toast's surface at 3:1.
- **A toast is a live region**, so a screen reader announces it without taking focus (WCAG 2.2 SC 4.1.3): a `toast_alert` is `Live::Assertive` and interrupts, a plain `toast` is `Live::Polite` and waits its turn. The politeness follows the same `ToastKind` the mark's colour does, so the two channels never disagree.

## Actions, sticky errors, repeats and the log

```rust
fn deleted(mut commands: Commands) {
    commands.spawn(toast("Item deleted").action("Undo", "undo"));
}

fn failed(mut commands: Commands) {
    commands.spawn(toast_alert("Could not write the save").action("Show", "show").sticky());
}

fn heard(action: On<ToastAction>) {
    match action.id.as_str() {
        "undo" => { /* put the item back */ }
        "show" => { /* open the folder */ }
        _ => {}
    }
}
```

![The notifications example: Delete item spawns the toast "Item deleted" with an Undo button and a journal row with an Undo of its own, Save game pressed three times shows one "Game saved x3" while the journal lists all three, Break something shows a sticky red toast wrapped over four lines with Show and Dismiss buttons, and Tab walks the ring down the journal to the Undo on "Item deleted" where Enter makes the game hear "undo (entry 1)"](https://raw.githubusercontent.com/dark-incorporated/bevy_gooey/main/docs/media/notifications.gif)

- **`.action(label, id)`** adds a button (a button's look, fading with its toast). Pressing it (Enter, Space, South or a click) sends **one `ToastAction { toast, id }`** (an `EntityEvent` on the toast, observable globally) and dismisses the toast: it fades out at once, so a second press does nothing. The button is a tab stop, so the keys and the pad reach it, but it never takes focus by itself: a game's focus does not jump. A toast with a button stands at least `ToastSettings::action_seconds` (6, times `duration_scale`) so it can be reached; offer the same command somewhere that does not time out, as WCAG 2.2.1 asks of anything that is only reachable from a timed message. Prefer one button.
- **`.sticky()`** (on `toast` or `toast_alert`) stands until the player dismisses it, with a **Dismiss** button that sends no `ToastAction`. It is not counted against `max_visible`, so a newer toast never pushes it out.
- **A toast's buttons keep their size.** A long message wraps (the body stops at 24 text sizes) but a button never gives up its padded label to it: each is a full button wide, half a gap of margin each side (so two stand a gap apart and the last is inside the frame), and centred on the toast's height beside a message of several lines. A toast without a button is laid out as before.
- **Repeats merge.** A toast identical (kind, words, buttons) to one that arrived less than `ToastSettings::merge_seconds` (2; 0 turns it off) ago folds into it: it reads "Game saved x3" (ASCII `x`: the host supplies the font), stands again from the start of its hold, and **the entity you spawned is despawned** (the one standing is the one that stays; `Toast::count()` says how many).
- **`ToastLog`** is a resource that keeps the last 200 lines (`ToastLog::CAPACITY`) as `ToastLogRecord`s: every toast spawned, merged or not, and every line you `push(ToastLogEntry { seconds, kind, text })` yourself (seconds on `Time<Real>`). It is plain data: read it, save it, `clear()` it. **Each entry has an `id()`** that `push` returns: it only goes up, survives the log being capped and is never given twice. `get(id)`, `get_mut(id)` and `remove(id)` find, change and take an entry; a record derefs to its `ToastLogEntry` (`record.text`) and carries a `count()` (`set_count(3)`: the row reads `text  (x3)`, in place) and its `actions()` (`add_action("Undo", "undo")`). A time that is not a number is 0, a count of 0, an empty label or id and a repeated action are ignored.
- **`ToastKind::Note`** (`toast_note(text)`) is a third kind for a quiet receipt: a muted mark, and no `! ` in its row.
- **A toast that is also a journal line.** A toast logs itself, so a refusal you push to the log yourself would be listed twice: spawn the toast `.unlogged()` (it adds nothing to the log), or `.logged_as(id)` with the id `push` returned (it adds nothing and `Toast::entry()` names that entry: the toast and the journal's row are one row).
- **`notification_center()`** is a scrolling list of the log, newest first, a row for each entry as `m:ss  words` (an alert's words start with `! `: the mark is not only a colour) or "No notifications yet". A row is a button, so the keys and the pad scroll it like any list; put it in a panel or a dialog of your own. `examples/notifications.rs` shows all of it.
- **A row can carry buttons and says which entry it is.** `NotificationRow::entry()` is the id of the entry the row draws (`None` on the "No notifications yet" line). Each of an entry's `actions()` is a button at the row's end (a tab stop, a button's look); pressing it sends **one global `NotificationAction { entry, id }`**, and a press on the row's words sends nothing, so a click on a line of history never undoes it. A row whose entry did not change is **the same entity** after the log changes (focus and hover stay); one whose entry changed (a count, an action) is rebuilt, one whose entry is gone is despawned. A centre hidden with `Shown(false)` has no tab stops.

```rust,ignore
fn moved(mut log: ResMut<ToastLog>) {
    let id = log.push(ToastLogEntry { seconds: 3.0, kind: ToastKind::Note, text: "Moved the bed".into() });
    if let Some(entry) = log.get_mut(id) {
        entry.add_action("Undo", "undo");
    }
}

fn on_row_action(action: On<NotificationAction>) {
    if action.id == "undo" {
        // undo the change that entry `action.entry` records
    }
}
```

Research: [`docs/research/toast-actions.md`](https://github.com/dark-incorporated/bevy_gooey/blob/613537885824a772991d9f1b49786f3d5ab7bc35/docs/research/toast-actions.md).
