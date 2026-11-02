# Scrambled Brains

**How accurate must a connectome be before a brain emulation keeps its behaviour?**
A DeepBrain at Berkeley project, fall 2026.

We run the whole male fruit-fly central nervous system (166,700 neurons, male CNS v1.0) as a spiking network and
let it learn to ride a bicycle below the speed at which the bike balances itself. Then we corrupt its wiring step
by step, from realistic mapping errors to random wiring, and measure where the behaviour breaks.

This repository is the study: the project page, the wiring-ladder results, the preregistration and the final
figure. The simulator, the bicycle and the ladder generators live in
[victory-c/fly-brain](https://github.com/victory-c/fly-brain) (`brain/variants.py`, `runs/pretest.py`,
`ride-rung.sbatch`), which this project uses as its engine.

## The wiring ladder

| Rung | What survives of the real wiring |
|---|---|
| R0 | everything |
| R1 | everything, but 6% of neurons carry the wrong transmitter (Eckstein et al. 2024 error rate) |
| R2 | everything, with each synapse count jittered by a lognormal +/-25% |
| R3 | which cell types talk to which, on each side |
| R3.5 | each neuron's number of inputs, input strength and excitatory/inhibitory mix |
| R4 | each neuron's number of inputs and outputs |
| R5 | nothing: random targets |

Every rung is scored three ways: closed-loop riding with a learned decoder (Track A), decoder-free published
predictions (Track B), and how many recorded neurons a decoder needs (Track C).

## Layout

- `site/` the project page, served as is by Vercel (`vercel.json`); `site/data.json` holds the numbers the page
  draws, exported from fly-brain's `results/`.
- `docs/` preregistration and reports (to come).

## Licence

Code MIT (see `LICENSE`). Numbers and figures CC BY 4.0. The connectome is the male CNS v1.0 (HHMI Janelia FlyEM,
Cambridge Connectomics Group, Google; CC BY 4.0); the neuron model follows Shiu et al., Nature 2024. Not affiliated
with Janelia, Eon Systems or the Foresight Institute.
