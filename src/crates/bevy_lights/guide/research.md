<!-- synced from dark-incorporated/bevy_lights@c057c2e; edit it there -->
# The craft and the science

Every default in this crate is researched and cited, or marked a design default. Each note is committed
before the code it justifies, and carries the headings the repository requires: `## Sources`,
`## Craft principle`, `## How shipping games do it`, `## Model adopted`, `## Parameters`,
`## Validation targets`, `## Deviations`, `## Pending index`.

| note | what it settles | key sources |
|---|---|---|
| [`docs/research/fire-light.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/fire-light.md) | the flicker's rate and amplitude, the kindle's flare | Sanctuary decisions 0127/0148; Team Fortress 2's illustrative ramp (SIGGRAPH 2007 *Advances*); the fire-physics literature this crate is still missing |
| [`docs/research/light-pool.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/light-pool.md) | the pool's budget, reach, sort and phases | Olsson, Billeter & Assarsson 2012 (clustered shading); Ghost of Tsushima (SIGGRAPH 2021 *Advances*); *Stochastic tile-based lighting* (SIGGRAPH 2025 *Advances*); RTR4's many-light chapter |
| [`docs/research/flame.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/flame.md) | the flame's shape, noise, ramp and packing | Nguyen, *GPU Gems* ch. 6 §6.1; RTR4 §6.3; Sanctuary decision 0228 |
| [`docs/research/flame-flicker.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/flame-flicker.md) | why a drawn flame breathes with the light it motivates, and how the two share one function | Xia & Zhang 2018; SIGGRAPH 2011 *Advances*' fire talk; Doğaner on motivated sources |
| [`docs/research/flicker-depth.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/flicker-depth.md) | how far a fire dips, who chooses, and a measured ceiling for the default | Mandin & Most (IAFSS 6) on flame fluctuation; Gergely et al. 2020; Doğaner |
| [`docs/research/fuel-bed.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/fuel-bed.md) | why a bed is a temperature field and not a constant `emissive` | Pirk et al. 2017 (wood combustion); Xia & Zhang 2018; *PBR* 3rd ed. ch. 12 on blackbody emitters; Prince 2004 on clipped highlights |
| [`docs/research/corpus.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/corpus.md) | what the home-still library holds for cinematography, photography, CG lighting, game-lighting craft, many-light rendering, fire physics and perception — and what it does not | the live corpus |

The full index — including the notes behind the flame's silhouette, its catch, its read from overhead,
the pool's hand-offs, a fire's colour, smoke, tongues, the fuel bed, a whole fire as one component and a
fire that moves — is [`docs/research/README.md`](https://github.com/dark-incorporated/bevy_lights/blob/c057c2e6fe135098664e358c92d6df1e7b18ae29/docs/research/README.md).
