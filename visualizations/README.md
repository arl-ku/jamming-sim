# Visualizations of a CALiPPSO jammed packing

Interactive 3D views of a monodisperse hard-sphere packing produced by CALiPPSO
(`d=3`, `N=512`, seed `123`), driven from a random gas at `φ=0.30` to a jammed,
isostatic state at `φ≈0.6305`. Both HTML files are fully self-contained (data is
embedded; no external dependencies) — open them directly in a browser.

| File | What it shows |
|------|---------------|
| `packing_viewer.html`   | The final jammed configuration. Drag to rotate, scroll to zoom; colour spheres by contact number `z`, depth, or plain. Rattlers (z=0) are faded. |
| `packing_animation.html`| The **jamming process**, iteration by iteration: spheres inflate and rearrange from φ=0.30 to φ=0.63. Play/scrub controls, live φ readout. Uses minimal-image interpolation so periodic wraps don't streak across the cell. |

## How the data is produced

From the repository root:

```julia
julia --project=. export_packing.jl      # -> packing_d3_N512.csv    (final config + coordination)
julia --project=. export_trajectory.jl   # -> packing_trajectory.json (every iteration; *.json is gitignored)
```

`export_trajectory.jl` relies on the optional `traj_sink` keyword added to
`produce_jammed_configuration!` (in `src/CALiPPSO.jl`): pass a `Vector` and each
iteration pushes `(R, d×N matrix of raw coordinates)` into it. Default `nothing`
= no recording, no overhead, no behaviour change for existing callers.

## Rebuilding the HTML

The viewers embed the exported data. To regenerate after re-running the exports:

```bash
python gen_viewer.py   # reads ../packing_d3_N512.csv     -> packing_viewer.html
python gen_anim.py     # reads ../packing_trajectory.json -> packing_animation.html
```
