# Using a crate on its own

Every crate in the coven is a Bevy plugin plus its settings, and none of them needs the Cauldron.

1. Add it:

   ```sh
   cargo add bevy_elements
   ```

   A crate that is not on crates.io yet (`bevy_light_grid`) is a git dependency:

   ```toml
   bevy_light_grid = { git = "https://github.com/bevy-coven/bevy_light_grid" }
   ```

2. Add its plugin to your app:

   ```rust,ignore
   use bevy::prelude::*;

   fn main() {
       App::new()
           .add_plugins((DefaultPlugins, bevy_elements::ElementsPlugins))
           .run();
   }
   ```

   Each crate's page in this book, and its README, gives its own plugin name and a quick start that compiles.

3. Tune it. A crate's settings are plain Rust types that implement `serde`'s `Serialize` and `Deserialize`, so you can build them in code, or load them from a RON or JSON file in your project.

Each crate's README has a `cargo run --example` line that opens the scene in its hero GIF; that is the fastest way to see what it does before you add it.
