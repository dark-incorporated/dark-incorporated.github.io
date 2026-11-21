<!-- synced from dark-incorporated/bevy_dark_factory@8a776ca; edit it there -->
# Getting started: make your first map

In about ten minutes you will make a map in this repo's own project, place a piece on it, undo the placement, save, and open the map again.

You need a Rust toolchain and a clone of this repo. Run every command from the repo root. On a Mac you can instead use the signed app from the [releases](https://github.com/dark-incorporated/bevy_dark_factory/releases) and open the project from its launcher.

![Placing a sofa on the bedroom map, then undoing it with Ctrl+Z (Cmd+Z on a Mac)](https://raw.githubusercontent.com/dark-incorporated/bevy_dark_factory/8a776caf494daa6109297d067eb61d6c53acd40f/docs/media/place-and-undo.gif)

## Start the editor

With no argument, `cargo run -p bevy_dark_factory` opens the **launcher** before any project: your recent projects as cards (a missing folder is listed as missing, not dropped) with a **Filter projects** box, **New project** (a name, a place and a template; a name that is already a folder is refused beside the field and Create stays off until it is free), **Open folder…** (the system's own folder chooser) and, when the changelog has grown since you last opened a project, what it added. On a first run, with nothing opened yet, the launcher is a welcome with an **Open the example** button (the Learn page has the same button). Choosing a project opens its **project page**, as step 1 below does by hand. **Copy command line** on a recent project puts the line that opens it on your clipboard. One press (or Enter) on a card opens it.

A project named on the command line with a map or a workspace (`cargo run -p bevy_dark_factory -- . bedroom`) skips the project page and opens on a **loading screen**: nothing for the first second, then the stage it is in with a spinner, and from ten seconds a bar that says `N of M` and the stage. **Cancel** goes back to the launcher and writes nothing. When it has loaded, any file of the project that does not read is listed on a card, one row each with the file, the field and why; **Open anyway** goes on into the editor and **Back** returns to the launcher. `BLUEPRINT_LOAD_STAGE_DELAY_MS=3000` pauses after each stage if you want to see the screen on a project that opens too fast to.

A project written before the YAML cutover holds `.ron` files and is refused at open, naming `bevy_dark_factory migrate <project folder>`, which converts it ([your game](your-game.md#moving-a-project-to-yaml)).

1. Run the editor on this project:

   ```
   cargo run -p bevy_dark_factory -- .
   ```

2. Wait for the window. It opens on the project page.

The page's sidebar has **Projects**, **Learn**, **What's new** and **Settings**, with the editor's version under them. The page itself has three sections: **Maps** (each map a card, and **+ New map**), **Kits** (each kit a card, and **+ New kit**) and **Agent guide** (the project's `.dark_factory/AGENTS.md`, which an agent reads first; **Create guide** writes one). The terminal is collapsed: the status band's **Terminal Cmd+J** label raises it.

A **kit** is a folder of pieces. A **piece** is one thing you can place on a map, such as a wall, a table, or a sofa. This repo's project binds two kits, `furniture` and `scp` (the folder `site` is a third kit that is not bound), and the first, `furniture`, is where new work lands.

## Make a map

A **map** is a file that holds your placements. It is saved as `<name>.map.yaml` in the project's maps folder.

1. Under **Maps**, press **+ New map**. A dialog titled **New map** opens.
2. Type `first_map` in **Name**. The name is turned into lowercase letters, digits and underscores, and a name a map already has is refused beside the field. The three size fields, **Width**, **Depth** and **Height** (metres), start at the default size, and **Uses pieces from** chooses which kits the map offers (every kit, or a named group of kits).
3. Press **Create**. The map is made and **opens in the editor**, in that one press.

**What you see:** the editor opens on the **Map workspace**. A workspace is one of the editor's jobs: Project, Map, World, Kit, Animation, Sound, Files, Game, Agent and Design. The strip of icons at the window's left edge has one for each, and `Cmd+1` to `Cmd+9` and `Cmd+0` (`Ctrl` elsewhere) go to them in that order.

**If the map is made but does not open:** the editor refused it, and the reason is on the status line. The map is still on the project page, so opening its card tries again.

**If it goes wrong:** a name that would leave nothing usable (no letters or digits) says so, and **Create** stays off until the name is usable and the sizes are more than zero.

## Look at the Kit workspace

1. Press `Cmd+4` (`Ctrl+4` on Windows and Linux). The editor switches to the Kit workspace.

**What you see:** the Kit workspace opens on the MESHES tab.

2. Press `Cmd+2` (`Ctrl+2`). You are back on the Map workspace, with the same map and the same view: a switch changes what is drawn and nothing else.

## Arm a piece and place it

Arming a piece means choosing the piece that your next click will place. A **placement** is one piece put on the map.

1. Make sure you are on the Map workspace. The PLACE palette lists the pieces of the kit.
2. Press Down. Each Down press arms the next piece in the PLACE list. Hold Shift to skip five pieces at a time.
3. Move the pointer over the floor. A translucent ghost of the armed piece follows the pointer.
4. Click on empty ground. The piece is placed where you clicked.
5. Place a second piece the same way, so the map has two placements.

**What you see:** each click adds a solid copy of the piece at the spot under the pointer. The ghost stays with the pointer until you arm something else.

**If it goes wrong:** if the ghost does not appear, press Down again. Walking the PLACE list is what arms a piece. Pressing Enter does not arm a single piece. Enter arms a composition, which is a group of pieces. It works only while the composition picker is open, which you open with `P`.

**The tour points at the control it names.** Help, then **Take the tour** runs the same first-map guide an agent can post, and each step that is about a control outlines it and stands an arrow beside it, pointing up at the control from below or down from above when there is no room below. The outline and arrow are click-through: the click the step asks for reaches the control under them. A step naming a control that is not on screen says so on the status line rather than pointing at nothing.

Press Home to frame the view. With a locked placement, Home frames that placement. Otherwise it frames the whole map. Framing does not change the map.

**Resize the panels.** The thin bar between the INSPECTOR on the left and the map is a divider. Drag it left or right and the inspector narrows or widens with it, its rows reflowing to the new width, while the map keeps the rest of the window. The wheel over the inspector scrolls it to the sections below the fold, such as ENVIRONMENT. `Cmd+B` (`Ctrl+B` elsewhere) slides the left panel shut and open, and a closed one peeks out over the map while the pointer rests on its edge.

**Your arrangement is kept.** A divider you drag, a tab you pick and a panel you move into another group are saved in your settings file (`settings.yaml`, in the application's data folder) as the shell's layout, one per workspace, and the editor opens on that arrangement next time. **View ▸ Reset layout** puts the open workspace's default back and takes that workspace's key out of the file, leaving the others alone. A project's own `editor.yaml` may state a layout too; the project's is the one read when a project is open.

## Undo and redo

1. Press Cmd+Z. The second placement disappears.
2. Press Cmd+Shift+Z to redo it. It comes back.
3. Press Cmd+Z again to leave the map with one placement.

**What you see:** each Cmd+Z removes the most recent change, one change at a time, whoever made it. Cmd+Shift+Z puts back the change you last undid.

## Save

1. Press Cmd+S.

**What you see:** a line in the status band reads `saved`, followed by the file path. The file is `maps/first_map.map.yaml` inside the project, which is `assets/blueprint/maps/first_map.map.yaml`.

**If it goes wrong:** if the map cannot be saved, the status band shows `NOT SAVED:` followed by the reason. The map stays open and nothing on disk changes. Fix the reason, then press Cmd+S again.

## When the editor refuses something

A refusal stands at the top of the viewport as a toast with the reason, and stays until you dismiss it: press its **Dismiss** button or `Esc`, or let the next refusal replace it. The same line is kept in the **Notifications** panel on `Cmd+E`, which lists every step and refusal of this session, newest first, with the time it happened; the newest step that can be taken back has an **Undo** button. When the refusal is about one thing (for example ``not sent back: `bed_double` is placed by `bedroom` ``), the toast has a **Show** button that takes you to it: a placement on the Map is targeted, and a piece in the library is selected on the Kit workspace's Meshes panel.

## Return to the project page and reopen

1. Press Cmd+O. The editor returns to the project page. (`Cmd+1` shows the same page as the Project workspace, beside the open map.)
2. Under **Maps**, the card `first_map` is there. Open it.

**What you see:** the editor opens `first_map` on the Map workspace. The piece you kept is still on the map. The piece you undid is not.

## Where next

- [Building maps](building-maps.md) covers turning, lifting, filling, generating and the rest of the map's jobs.
- [Agents](agents.md) connects an agent to the editor.
- [Keys](keys.md) lists every key, grouped by where you are in the editor.
- [README](https://github.com/dark-incorporated/bevy_dark_factory/blob/8a776caf494daa6109297d067eb61d6c53acd40f/docs/guide/README.md) describes the guide and what it covers.
