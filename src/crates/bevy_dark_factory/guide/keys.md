<!-- synced from dark-incorporated/bevy_dark_factory@8a776ca; edit it there -->
# Keys

This page lists the keys the editor answers to, grouped by where they work. It is taken from the binding table in `crates/bevy_dark_factory/src/keys.rs`. Hold `K` in the editor to see the same keys in an overlay.

## How to read this page

Cmd means the Command key on a Mac. Shift and Alt keep their names. Alt is Option on a Mac. A row with two chords, such as `Cmd+Z` and `Cmd+Shift+Z`, is two bindings that do opposite jobs.

The editor has ten **workspaces**, one job each: **Project** (the project's maps, kits and agent guide), **Map** (builds a level out of pieces), **World** (the world under the level: terrain, water, forest, lights), **Kit** (makes the reusable content: meshes, tiles and compositions), **Animation** (the rig bench), **Sound** (cues and music scores), **Files** (the project's files and an editor for them), **Game** (the running game, beside its own window), **Agent** (what the agent is doing and what waits on you) and **Design** (the game's style). Switching workspaces changes what is drawn and nothing else: the project, the open map and the selection stay where they are.

Some tables below say a panel of a workspace: the Meshes, Tiles and Compose panels are the Kit workspace's, and the Anim panel is the Animation workspace's rig bench.

A piece is one placed item on a map. A composition is a named group of pieces that you place as one. A kit is the set of meshes, tiles, and compositions you make once and reuse.

The "Works when" column names the state the editor must be in:

- **Any time** means the key works in every state of that tab.
- **Nothing in hand** means no piece is held.
- **While a piece is in hand** means you have picked a piece up and not yet dropped it.
- **While a derivation waits** means the editor has proposed a result and is waiting for a yes or no.
- **While browsing tiles** means the Tiles panel is live, and the arrow keys walk the tiles.
- **While a composition is being picked** means the composition picker has the keys that walk it.

A key marked "in filter boxes" still walks its list while a filter box has focus. Every other key pauses while you type in a name, an id, or a filter box. Typing the letter `S` in a name does not save the map, because saving is `Cmd+S`.

## Every key is a command

Each key on this page is also a command with an id that does not change, such as `file.save`, `edit.undo` or `tiles.align_forward`. The part before the dot is the category a menu groups it under. A menu, the command palette and an agent name a command by its id, so renaming a key never breaks them. `crates/bevy_dark_factory/src/commands.rs` lists every id and its title, and a test fails when two commands share an id, a title, or a shortcut on a tab where both work.

Help ▸ Keyboard shortcuts lists every command of the registry with the chord it answers to now, so a command added tomorrow is on it without anyone writing it, and a command you rebound shows the new chord. The same screen is where you rebind: press a chord on a row, and a chord another command already has is refused by name.

An agent runs a command by its id with `blueprint_run_command`, and it presses the same shortcut, so a command that is not available now (a key that needs a piece in hand, or a text field holding the keys) is refused with the reason a menu would show.

## The command palette

`Cmd+Shift+P` (`Ctrl+Shift+P` elsewhere) or `Cmd+K` (`Ctrl+K`) opens a box over every command. Type a few letters ("undo", or "opn prj" for "File: Open Project") and the list narrows; the commands you ran last come first. `Up` and `Down` move the lit row, `Enter` or a click runs it, and `Esc`, a click outside, or the same chord again closes it. Each row shows its shortcut at the end, and a command that cannot run now stays in the list with the reason where the shortcut would be ("Not on this tab", "Only while holding a piece"), judged in the tab you were on when you opened it. A command from the palette runs as its shortcut would: the same undo step, the same line in the history, the same refusals.

`Cmd+P` (`Ctrl+P`) opens the same box over **everything the project names**: maps, pieces, placed pieces, compositions, rigs and their clips, cues, scripts, files, data files and notes. Type a name and press `Enter`, and the editor opens the workspace and the thing in it. Start the text with `>` to search commands instead.

The palette does not open while a text field has the keys, because `Cmd+K` there is the field's.

## Everywhere

These keys work in every workspace.

| Key | Works when | Does |
| --- | --- | --- |
| `Cmd+1` to `Cmd+9`, `Cmd+0` | Any time | Go to a workspace: 1 Project, 2 Map, 3 World, 4 Kit, 5 Animation, 6 Sound, 7 Files, 8 Game, 9 Agent, 0 Design. The order is fixed, so a number is always the same workspace. The Kit panels (Meshes, Tiles, Compose) have no key: click their chips on the strip. |
| `Cmd+Delete` | Any time | Define this piece. On a Mac, the Delete key sends Backspace. |
| `K` (held) | Any time | Show every key and what it does. Release to hide it. |
| `Cmd+S` | Any time | Save. |
| `Cmd+\` | Any time | Snip an area. |
| `Cmd+O` | Any time | Go back to the project page (it asks first when the map has unsaved changes). |
| `Cmd+=` / `Cmd+-` | Any time | Step the whole interface's size — buttons, spacing and type together — up or down the ladder 100%, 110%, 125%, 150%, 175%, 200%. The Settings screen's **Interface size** row (`Cmd+,`) shows and sets the same value, so a chord and a slider are two hands on one number. `Cmd+=` is also `Cmd++` on a keyboard where `+` needs Shift. |
| `Shift+Cmd+0` | Any time | Put the interface size back to 100% (`Shift+Ctrl+0` elsewhere). `Cmd+0` is the Design workspace, so the reset takes Shift. |
| `Cmd+,` | Any time | Open the settings screen, or close it: every setting with its default, a search, and Reset. It is also the launcher's Settings button; its Project configuration button lists the family crates the project uses and the packs the kit leaves out (a switch each), and its Keymap button rebinds a command (a chord another command has is refused). A rebound command answers to its new chord at once; this page lists the chords it ships with. |
| `Cmd+E` | Any time | Show the **Notifications** panel: every step and refusal of this session, newest first, each with the time it happened. The newest step that can be taken back has an **Undo** button, which works while the agent's writes are paused. `Esc` closes it and `Cmd+C` copies the list. |
| `Shift+Cmd+E` | Any time | Show or hide the **Console**: every `info`, `warn` and `error` this process has said, newest first, with a pill per level carrying its line count (press one to hide that level), and a line's whole text and frame number one click away in the details pane. A line that names a piece (`warn!(piece = "wall@0", …)`) offers a chip that selects that piece. It is the log file's second window, not the Notifications panel's: `Cmd+E` is what went wrong and what an agent did, this is what the process said. The ring holds 400 lines and says how many fell off. `Shift+Ctrl+E` elsewhere. |
| `Shift+Cmd+D` | Any time | Show or hide the **Frame profile**: the last frame's time, the heaviest system it ran and how much of the frame that was, over 120 frames of history. Opening it starts recording; closing it stops, so the cost with the panel away is one atomic load per measured system. `blueprint/state.frame.frame_ms` reports the same number the panel draws. `Shift+Ctrl+D` elsewhere. |
| `Cmd+J` | Any time | Cycle the terminal through its three positions, in the owner's order: maximised, then collapsed, then a quarter of the window at the bottom, and round again (`Ctrl+J` elsewhere). It starts collapsed; the status band's **Terminal Cmd+J** label does the same, and its tooltip says what the next press will do. |
| `Shift+Cmd+J` | Any time | Make the terminal cover the whole window below the menu bar from whichever of the three positions it is in (`Shift+Ctrl+J` elsewhere; View ▸ Maximise terminal). From full, it gives back the height. |
| `Cmd+P` | Any time | Go to anything: one finder over everything the project names. `>` first searches commands. |
| `Cmd+[` / `Cmd+]` | Any time | Back and forward across workspaces and camera positions, up to 100 places (the mouse's back and forward buttons do the same). |
| `Cmd+W` | Any time | Close the active document tab (`Ctrl+W` elsewhere). `Shift+Cmd+T` opens the one you closed last. |
| `Cmd+C` | Any time | Copy this tab's text. |
| `Cmd+F` | Any time | Filter the list. |
| `Esc` | Any time | Back out of the current state. |
| `W`, `A`, `S`, `D` | Any time | Pan forward, left, back, and right. |
| `Q`, `E` | Any time | Turn the view left and right. |

## Map

These keys work in the Map workspace.

| Key | Works when | Does |
| --- | --- | --- |
| `Cmd+Z` | Any time | Undo. |
| `Cmd+Shift+Z` | Any time | Redo. |
| `H` | Any time | Target the stack. |
| `Up` / `Down` | Nothing in hand | Walk the palette. Hold Shift to move five at a time. Works in filter boxes. |
| `P` | Nothing in hand | Take the arrow keys to the compositions. |
| `Shift+Up` / `Shift+Down` | While a composition is being picked | Walk the compositions. |
| `Enter` | While a composition is being picked | Arm this composition for the map. |
| `R` | Any time | Turn left, 15° a press: the armed piece if one is armed, otherwise the placed piece under the pointer. |
| `T` | Any time | Turn right, 15° a press: the armed piece if one is armed, otherwise the placed piece under the pointer. |
| `Y` | Any time | Tip about x, a quarter turn: the armed piece if one is armed, otherwise the piece under the pointer. |
| `U` | Any time | Tip about z, a quarter turn: the armed piece if one is armed, otherwise the piece under the pointer. |
| `V` | Any time | Straighten the piece. |
| `J` | Any time | Change the grid rung: tile, fine, then finer. |
| `[` / `]` | Any time | Lower / lift this piece. |
| `X` | Any time | Enter removal mode. |
| `Shift` and drag | Any time | Select every piece the box covers, primary first, in one act — no operation and no undo step, because a selection is where you are looking. `Shift` and a click adds one piece beside the primary, as before. |
| `Home` | Any time | Frame the view: the locked placement when there is one, otherwise the whole map. |
| `B` | Any time | Move. |
| `Shift+B` | Any time | Clone. |
| `Shift+Cmd+B` | Any time | Run. |
| `Cmd+B` | Any time | Show or hide the left panel (`Ctrl+B` elsewhere; View, Show left panel). |
| `Shift+Cmd+M` | Any time | Zen mode: hide everything but the viewport, and bring it back (`Shift+Ctrl+M` elsewhere; View, Zen mode). |
| `Shift+Cmd+X` | Any time | Show the problems list: the Map inspector's PROBLEMS, scrolled on screen from any workspace (`Shift+Ctrl+X` elsewhere; View, Show problems). |
| `M` | Any time | Keep the selected set as a composition. |
| `N` | Any time | Rename the map. |
| `O` | Any time | Pin or unpin. |
| `F` | Nothing in hand | Fill with the brush. |
| `G` | Nothing in hand | Fill with the learned source. |
| `Shift+G` | Nothing in hand | Fill with the declared source. |
| `Cmd+G` | Nothing in hand | Fill with the composed source. |
| `Enter` | While a derivation waits | Keep this layout. |
| `Esc` | While a derivation waits | Throw the layout away. |

## Meshes

These keys work on the Meshes panel of the Kit workspace.

| Key | Works when | Does |
| --- | --- | --- |
| `Up` / `Down` | Any time | Walk the lists. Hold Shift to move five at a time. Works in filter boxes. |
| `Left` | Any time | Move focus to the candidates. Works in filter boxes. |
| `Right` | Any time | Move focus to the library. Works in filter boxes. |
| `I` | Any time | Type an id. |
| `M` | Any time | Mount. |
| `Enter` | Nothing in hand | Add or update this tile. |
| `Space` | No piece in hand | Open or close the pack. |
| `Enter` | While a derivation waits | Keep the derived edges. |
| `Esc` | While a derivation waits | Throw the derived edges away. |
| `R` | Any time | Rescan. |
| `Shift+R` | Any time | Exclude the pack. |
| `Delete` | Any time | Send this back to NOT IMPORTED. |
| `Cmd+Z` | Any time | Undo this tab's last change. |
| `Cmd+Shift+Z` | Any time | Redo this tab's last change. |
| `T` | Any time | Move the cell cursor forward. |
| `F` | Any time | Move the cell cursor left. |
| `G` | Any time | Move the cell cursor back. |
| `H` | Any time | Move the cell cursor right. |
| `Shift+T` | Any time | Add a vocabulary token. |
| `[` / `]` | Any time | Previous / next layer. |
| `Z` | Any time | Mark this cell solid. |
| `X` | Any time | Mark this cell as an edge. |
| `V` | Any time | Clear this cell. |
| `B` | Any time | Rescan the solid. |
| `N`, `O`, `P` | Any time | Turn the mesh about x, about y, and about z. |
| `L` | Any time | Suggest labels. |
| `Shift+L` | Any time | Suggest labels for all. |
| `Shift+Y` | Any time | Abandon all suggestions. |
| `/` | Any time | Filter the tags. |

## Tiles

These keys work on the Tiles panel of the Kit workspace.

| Key | Works when | Does |
| --- | --- | --- |
| `Up` / `Down` | While browsing tiles | Walk the tiles. Hold Shift to move five at a time. Works in filter boxes. |
| `Right` | While browsing tiles | Go to the meshes. |
| `Left` | Nothing in hand | Go back to the tiles. |
| `Enter` | While browsing tiles | Open this tile. |
| `Up` / `Down` | Nothing in hand | Walk the library. Hold Shift to move five at a time. Works in filter boxes. |
| `Up` / `Down` | While a piece is in hand | Move the piece forward and back. |
| `Left` / `Right` | While a piece is in hand | Move the piece left and right. |
| `,` / `.` | While a piece is in hand | Step to the previous / next member. |
| `Shift` + arrow | While a piece is in hand | Flush the piece to that side. |
| `Space` | Not browsing tiles | Take the piece. `Esc` puts it back. |
| `[` / `]` | Not browsing tiles | Move the layer down / up. |
| `J` | Not browsing tiles | Make the grid deeper by thirds, wrapping around. |
| `Enter` | Nothing in hand | Drop the piece. |
| `Shift+Enter` | Nothing in hand | Drop the piece into a slot. |
| `R` | Not browsing tiles | Turn this piece. |
| `Delete` | Not browsing tiles | Remove this piece from the tile. |
| `Shift+Delete` | Not browsing tiles | Empty the tile. |
| `N` | Any time | Name a new tile. |
| `C` | Any time | Close the tile. |
| `Cmd+Z` | Not browsing tiles | Undo this tab's last change. |
| `Cmd+Shift+Z` | Not browsing tiles | Redo this tab's last change. |

## Anim

These keys work on the Animation workspace's rig bench (the Anim panel).

| Key | Works when | Does |
| --- | --- | --- |
| `Up` / `Down` | Any time | Walk the rigs. Hold Shift to move five at a time. Works in filter boxes. |
| `Enter` | Any time | Adopt the measured values into the rig file. |
| `Cmd+Z` | Any time | Undo the last write. |
| `Cmd+Shift+Z` | Any time | Redo the last write. |
| `Left` / `Right` | Any time | Scrub the phase. Hold Shift to scrub finely. |
| `Space` | Any time | Play or scrub. |
| `C` | Any time | Check all rigs. |
| `G` | Any time | Toggle the ghost: measured over declared. |
| `V` | Any time | Change the view: figure, feet, side, or ground. |

## Compose

These keys work on the Compose panel of the Kit workspace.

| Key | Works when | Does |
| --- | --- | --- |
| `Up` / `Down` | Any time | Walk the focused list. Hold Shift to move five at a time. |
| `Enter` | Any time | Arm this composition for the map. |
| `I` | Any time | Rename this composition. |
| `Left` / `Right` | Any time | Choose which list the arrow keys walk. |
| `O` / `P` | Any time | Previous / next composition. |

## The terminal

A real shell is docked across the bottom of every screen, already in your project's folder: `cargo`, `git` and your agent run there. It starts collapsed. `Cmd+J` (`Ctrl+J` elsewhere) cycles it round maximised, collapsed and a quarter at the bottom, and `Shift+Cmd+J` makes it fill the window below the menu bar from any of the three; the status band's **Terminal Cmd+J** label raises it too, and a raise is kept across a relaunch. Click it to put the keyboard in the shell, and click anywhere else to give the keys back to the screen. A shell that ends (`exit`, `Ctrl+D`) closes its tab, and `+` in the bar opens another.

- **The shell holds its keys.** While it has the keyboard, typing a `d` does not move the camera and an arrow does not move the screen's focus. Command chords stay the editor's, except the few that mean a line-editing action on a Mac: `Cmd+Backspace` clears the line the shell is reading back to its start, `Cmd+Left` and `Cmd+Right` go to its start and end (the control codes `^U`, `^A` and `^E`), and `Cmd+K` clears the terminal and leaves the prompt at the top (`Ctrl+K` still belongs to the shell). `Esc` closes a dialog over a terminal that holds the keys.
- **Find in the scrollback.** `Cmd+F` (`Ctrl+F` elsewhere) opens a find box: every match is lit, `Enter` walks to older ones and `Shift+Enter` to newer, the box counts them, and `Esc` hands the keys back to the shell.
- **Scrolling and the mouse.** The wheel scrolls the terminal's output while the pointer is over it, and over the menu bar, the status band or any panel it leaves the map alone; the map zooms only when the pointer is over the map itself. Typing while you are scrolled back brings you to the prompt. Full-screen programs get their keys and mouse the way they ask: the wheel scrolls `less`, `man` and `git log`, a click reaches a program that asks for the mouse (`htop` sorts by the column you click), and `Shift`+drag still selects.
- **Links.** `Cmd+click` (`Ctrl+click` elsewhere) on an `http://` or `https://` address in the output opens it in your browser, even over a program that asked for the mouse.
- **What it draws.** Colours, inverse text and coloured backgrounds the way a program asks; a drag shows what it selects; icons a prompt or tool prints (starship, powerline, `eza --icons`) as icons, one cell wide, in FiraMono Nerd Font Mono. The caret is a block over its cell, takes the shape a program asks for (vim's block and bar), and is an outline while the keys are elsewhere. Its default text, ground and sixteen ANSI colours follow the theme the frame it changes.
- **What the shell is told.** `TERM_PROGRAM=DarkFactory` and the version, `DARK_FACTORY_PROJECT` (the open project's folder), and a UTF-8 locale when it would have none.
- **Settings.** Text size, cursor style, blinking and how many lines of scrollback are kept are on the Settings screen's Terminal tab (`Cmd+,`) and reach a running terminal at once; the program a tab runs and its arguments are `terminal_shell` and `terminal_shell_args`, and the agent is `terminal_agent` ([data files](data-files.md#editoryaml-and-settingsyaml), [agents](agents.md#start-an-agent-in-dark_factorys-terminal)).

## Text fields and menus

While a name, an id, or a filter box has focus, the editor reads your keys as text. Every shortcut above pauses, except the list keys marked "Works in filter boxes".
