<!-- synced from dark-incorporated/bevy_gooey@6135378; edit it there -->
# Upgrading

`bevy_gooey` is below 1.0, so a minor release (`0.52` to `0.53`) may break a host that touches the crate's types directly, and each break is listed under **Breaking** in [`CHANGELOG.md`](https://github.com/dark-incorporated/bevy_gooey/blob/613537885824a772991d9f1b49786f3d5ab7bc35/CHANGELOG.md) with the version that made it. This page says what a host has to change, for the breaks since the last release (0.52.1), which are on `main` today. A host that only spawns the widget functions (`button`, `panel`, `toast`, ...) and observes their events changes nothing: the breaks below are for a host that matches on a type exhaustively, builds one with a struct literal, or schedules or calls a gooey system itself.

`Extent`, `Space`, `Sides` and the other box-model types are new since 0.52.1, so no release of them has broken a host yet; from here on `Extent` and `Space` are not `#[non_exhaustive]` either, and `Space` has no `Eq` (it holds a float), so a match on them adds an arm when a variant arrives.

To check a bump quickly, build with `cargo check --all-targets`: every item below is a compile error, not a change of behaviour, except where it says otherwise.

## You match on `Role`

`Role` is not `#[non_exhaustive]`, so a variant added to it breaks an exhaustive `match`. Add the arms, or a `_ =>` if the match was only ever about the roles you spawn.

- `Role` gained the variants `GlyphButton`, `EdgeTab`, `Band`, `FillText`, `CountText` (G-82), `ButtonRow`, `FillColumn`, `FillRegion`, `Placed`, `AspectImage` (G-84), `Spacer`, `Sized`, `ListRow` (G-85), `Backdrop` (G-87), `ScrollRegion`, `ScrollView` (G-88), `ScrollViewport` (G-90), the `Markdown…` roles (the Markdown view) and the `Code…` roles (the code editor).

## You build `SideTab` or `GooeyFonts` by hand

- `SideTab` has a new public field `icon: Option<IconSource>` and no longer implements `Eq` (an image handle is `PartialEq` only). `SideTab::new`, `label` and `badge` are unaffected; a struct literal needs `icon: None` or `..Default::default()`, and a type that derives `Eq` over a `SideTab` drops the derive.
- `GooeyFonts` has a new field `mono`, the code editor's monospace face. A literal needs `mono` or `..default()`.

## You schedule or call a gooey system yourself

Gooey's plugins add every system in `GooeySystems`, so a host that only adds `GooeyPlugins` is not affected. A host that adds a system by hand, or calls it as a plain function, sees the new parameters.

- `page_lists` takes two more query parameters (G-89), because a `scroll_region` is paged by it too. Calling it as a plain function needs them; scheduling it by hand does not.
- `update_notification_centers` takes a different query (G-92). Nothing to change unless you ordered a system against its parameters.

## You read or write the toast log

All of these are G-92, the journal on `notification_center()`:

- `ToastKind` has a new variant `Note` (`toast_note(..)`, a muted mark and no `! ` in the journal's row). A `match` on `ToastKind` with no wildcard needs an arm.
- `ToastLog::push` returns the entry's id (a `u64` that is never reused). A call that ignored the unit result still compiles; keep the id to add actions to the row or to pass to `.logged_as(id)`.
- `ToastLog::entries()` yields `&ToastLogRecord`, which derefs to `&ToastLogEntry`, so field reads and a function taking `&ToastLogEntry` are unchanged. `ToastLogEntry` gained no field, so a struct literal of it still compiles.
- `NotificationRow` is no longer a unit struct: it carries the id of the entry it draws (`entry()`, `None` for the "No notifications yet" line). Spawn nothing but gooey's rows.
- A toast you spawn **and** push to the log yourself used to be listed twice; spawn it `.unlogged()`, or `.logged_as(id)` with the id `push` returned. See [toasts](toasts.md#actions-sticky-errors-repeats-and-the-log).

## Behaviour that changed without a compile error

- `SideTab::badge` draws nothing for an empty text or for a count of zero, in a plain `side_tabs` too.
- `GooeySkin::problems()` also checks every syntax colour of the code editor at the text-contrast bar, so a skin you wrote may report a new problem.
- A bare `Dock(layout)` on a node of your own now gets its body and shows its panels (before, `update_docks` returned early and built none). Your `Node` and your `DropTarget` are left as written.
- A `split` pane is no longer marked `Hovered` while the split is open: a host that treats "any `Hovered` node under the pointer" as "the pointer is on the interface" no longer finds the map's pane.
- `split_clamp` (so every split drag) no longer panics when the two panes' minimums fill the whole extent (G-91); `pin_to_edge` and the slider and number steps are total too. [Split panes](splits.md) has the rule.
- Bevy's `bevy_clipboard` feature is on, for the code editor's copy and paste. It adds no dependency to a game that already uses Bevy's defaults.

## Older releases

Each earlier break is in the [CHANGELOG](https://github.com/dark-incorporated/bevy_gooey/blob/613537885824a772991d9f1b49786f3d5ab7bc35/CHANGELOG.md), under the release that made it: search the file for `Breaking`.
