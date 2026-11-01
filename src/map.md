# The map of the coven

Every crate in the family, grouped by what it gives a game. Each picture plays from the crate's own repository.

## The grimoire and the Cauldron

### [bevy_grimoire](crates/bevy_grimoire.md)

The grimoire is what a game loads: a library of pieces and a map. The Cauldron is the editor that writes it: it learns a world's grammar from your example and builds more, with the Familiar beside you.

![An agent turns the abbey 90 degrees and removes its table through MCP calls; the inspector names each change as the agent's, and two presses of Cmd+Z take them back](https://raw.githubusercontent.com/bevy-coven/bevy_grimoire/main/docs/media/agent-drives.gif)

## World

### [bevy_elements](crates/bevy_elements.md)

Sky, weather, wind, clouds, terrain and water, simulated in compute shaders.

![The ten weather presets forced in turn, the clock running from 10.00 h on 20 April 2026](https://github.com/bevy-coven/bevy_elements/raw/HEAD/docs/media/tour_hero.gif)

### [bevy_flora](crates/bevy_flora.md)

Procedural stylized trees and shrubs that grow over time.

![A maple growing from a bare trunk into a full crown while the camera circles it](https://github.com/bevy-coven/bevy_flora/raw/HEAD/docs/media/growth.gif)

### [isomesh](crates/isomesh.md)

`isomesh` and `bevy_isomesh`: signed distance fields in, meshes out, with caves and carving.

![Eight examples at once: a field smooth-unioned into a mushroom, caves and arches, letters thinner than a voxel, one cell meshed two ways, Surface Nets against Marching Cubes, terrain being carved, a ball crossing chunk seams, and a slab blown apart](https://raw.githubusercontent.com/bevy-coven/isomesh/main/docs/media/kitchen-sink.gif)

### [bevy_lights](crates/bevy_lights.md)

Flickering fires and a budgeted pool of real lights over thousands of virtual ones.

![Four braziers with real lights of their own and 48 torch-bearers sharing an 8-light pool, their flames leaning back as they walk](https://github.com/bevy-coven/bevy_lights/raw/HEAD/docs/media/showcase.gif)

### [bevy_light_grid](crates/bevy_light_grid.md)

An illuminance grid that creature AI can read and follow.

![A flashlight wedge sweeps a dark room; pale creatures flee the beam while amber ones move into it](https://raw.githubusercontent.com/bevy-coven/bevy_light_grid/main/docs/beam.gif)

## Life

### [bevy_society](crates/bevy_society.md)

Villagers with needs, moods, memories, relationships, rumours and factions.

![A rumor spreads through a village: green tie lines thicken between villagers, one red rivalry line appears, and a magenta ring marks who knows the rumor](https://github.com/bevy-coven/bevy_society/raw/HEAD/docs/media/village.gif)

### [bevy_stigmergy](crates/bevy_stigmergy.md)

Fading marks on a grid that crowds coordinate through, like ant trails.

![Ninety foragers find the gap in a wall: a bright amber trail forms between nest and food while older trails fade](https://raw.githubusercontent.com/bevy-coven/bevy_stigmergy/main/docs/foraging.gif)

### [bevy_orca](crates/bevy_orca.md)

Walkers that steer around each other without colliding.

![Twenty coloured discs swap sides of a circle through a rotating vortex, without colliding](https://raw.githubusercontent.com/bevy-coven/bevy_orca/main/docs/circle_swap.gif)

### [bevy_speech_bubbles](crates/bevy_speech_bubbles.md)

Speech balloons, barks, conversation graphs and a dialog box.

![Five coloured figures in a ring while the camera orbits; speech and thought balloons appear above them and fade](https://raw.githubusercontent.com/bevy-coven/bevy_speech_bubbles/main/docs/chatter.gif)

## Interface

### [bevy_gooey](crates/bevy_gooey.md)

Menus, HUD meters, dialogs and tooltips with keyboard and gamepad navigation.

![Walking a menu with the keyboard: focus moves down the panel onto Options, the health meter drains, then the Load game list scrolls to follow focus and a toast appears](https://github.com/bevy-coven/bevy_gooey/raw/HEAD/docs/media/gallery.gif)

## Spectacle

### [bevy_carnage](crates/bevy_carnage.md)

Wounds that bleed and bodies that break, deterministic to the bit.

![A textured blocked-out body takes a blow, a burn, a slash and shots to the chest; the wounds bleed and pool, and the body comes apart](https://raw.githubusercontent.com/bevy-coven/bevy_carnage/main/docs/preset.gif)

## Agents and tooling

### [bevy_fairy](crates/bevy_fairy.md)

Lets a coding agent read and drive a running Bevy game.

![A scripted tour: each tool call beside the frame the same call captured](https://github.com/bevy-coven/bevy_fairy/raw/HEAD/docs/media/hero.gif)
