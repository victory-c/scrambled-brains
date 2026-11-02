# Scrambled Brains: preregistration (draft, 2026-11-02)

**Status: draft.** This becomes the preregistration when it is tagged in this repository before the first
closed-loop run on a scrambled rung. Everything run before the tag is listed under "Already run" and is not
confirmatory. Changes after the tag go in a dated "Deviations" section at the end, never by editing the text above it.

## 1. Question

On a closed-loop task that the body cannot solve by itself, how much of the measured wiring does a fixed-weight
spiking model of the whole fly central nervous system need before a learned decoder of a given size stops learning
the task? Secondary: do the same perturbations break the model's decoder-free predictions and its decodability?

## 2. System

- Connectome: male CNS v1.0 (Janelia FlyEM, Cambridge, Google; CC BY 4.0), 166,700 neurons, 25,582,938
  connections, 124,177,616 synapses (fly-brain `brain/connectome.py`).
- Neuron model: Shiu et al. 2024 leaky integrate-and-fire, one free parameter `w_syn` = 0.275 mV times a global
  scale. Scale 1.0 is Shiu's; the male CNS is calibrated at 0.47 (fly-brain `runs/calibrate_wsyn.py`). The
  simulator matches Brian2 spike for spike (`tests/test_brian2.py`).
- Body: a road bicycle (Whipple model, verified against Meijaard et al. 2007; self-stable 4.70-7.74 m/s with a
  70 kg rider), senses VS/HS optic flow, halteres, Johnston's organ and front-leg proprioceptors, 789 driven
  sensory neurons (fly-brain `bike/`).
- Task: ride 15 s at a held speed below the self-stable range with 5 N·m side gusts; a fall or leaving the road
  (|y| > 3.5 m) ends the run. Pedal power is fixed to hold the speed; the brake is off.

## 3. The wiring ladder (fly-brain `brain/variants.py`, seed = the rewiring draw)

| Rung | Definition | Keeps |
|---|---|---|
| R0 | real wiring | everything |
| R1 | 6% of neurons relabelled to another transmitter, drawn by frequency; sign flips only where the class (chloride vs. other) changes | wiring; 94% per-neuron transmitter accuracy after Eckstein et al. 2024 |
| R2 | each synapse count times a lognormal factor, median 1, sigma = ln 1.25 | wiring, signs, degrees |
| R3 | each target redrawn within the same (cell type, side) | the (type, side) synapse matrix; out-degree, output synapses, signs |
| R3.5 | targets permuted among connections of equal sign and synapse count | in-degree, incoming synapse total, excitatory/inhibitory input mix, plus everything the sender keeps |
| R4 | all targets permuted | in-degree, out-degree, output synapses, signs |
| R5 | targets drawn uniformly | out-degree, output synapses, signs |

Model-side rung (to be added before the tag): +/-10% in synaptic scale and in the membrane and synaptic time
constants, to put wiring error next to neuron-model error of the same size.

## 4. Transmission pre-test (gate for Track A)

fly-brain `runs/pretest.py`: bike held upright at 4.5 m/s, every sense at cruise rate, +30 Hz on the left VS (or
haltere) inputs in half the brains and on the right in the other half, 300 ms warm-up then 1 s, 8 brains per cell
(30 for the confirmatory run). A rung **passes** at a synapse scale s if (a) the number of descending and motor
neurons with |z| > 3 between left and right brains exceeds the largest value over the 18 balanced relabellings
(the null), for both VS and haltere drive, and (b) the network rate outside the driven neurons is within 2x of
R0's at scale 0.47 (21,500 spikes/s; so 10,750-43,000). Scales tried, in order: 0.47, 0.6, 0.8, 1.0, 1.5, 2.0. A
rung that fails at every scale is reported as "no transmission" and gets one confirmatory Track A seed, no more.

## 5. Track A: closed-loop riding

- Speeds: 4.0 and 4.5 m/s. Criterion: mean riding time over 48 riders in the last generation, and the fraction
  riding the full 15 s; the hands-off floor is 3.5 s (4.0 m/s) and 5.7 s (4.5 m/s).
- Search: cross-entropy method from a blank decoder, 48 riders x 15 s per generation, elite 25%, sigma0 as in
  the balance gate, 5 h cap per run (about 60 generations). Identical CEM seeds for every rung.
- Readout (fly-brain `runs/ride.py --readout`): each brain gets its own passenger screen
  (`runs/screen.py --brain`); the decoder reads the k descending neurons that screen ranks highest by roll-rate
  correlation, k = 8 and k = 32 (`topk`); `randk` draws k at random from the same pool, 3 draws; `bypass` reads
  the 10 sense populations directly (ceiling). No hand-picked neuron list is used on any rung.
- Design: every rung that passes the pre-test x k in {8, 32} x 3 rewiring draws x 5 CEM seeds x 2 speeds, plus
  R0, bypass and random-k. Rungs that fail the pre-test: 1 confirmatory seed at k = 32.
- Primary outcome per rung: last-generation mean riding time, median over seeds, with a paired bootstrap 95%
  CI (10,000 resamples, paired by CEM seed) against R0. Secondary: finish fraction; generations to reach half
  of R0's final riding time ("never" at the cap).
- Held-out tests on the final decoders (not used in the search): unseen gust seeds, speed +/-0.5 m/s, silencing
  that brain's own top-screened neurons.

## 6. Track B: decoder-free predictions

Shiu et al. 2024's feeding and grooming predictions (fly-brain `brain/stimuli.py`, dashboard experiments) and
about 5 in-class flybench tasks, each with stimulus, readout, expected sign and source listed in a CSV before the
tag. Scored per rung as the fraction of predictions with the expected sign, mean over 100 draws for R1 and R2
and over 3 draws for the shuffles, at that rung's calibrated scale and at 0.47.

## 7. Track C: decodability

Ridge regression from recorded spike counts (100 ms bins, as in the replay exports) to roll rate. N90: the
number of neurons needed to reach 90% of the R² that all descending neurons give together, for neurons added in
screen order and in random order, at a brain descending-neuron site and at a nerve-cord wing-motor site. Also:
the same from simulated jGCaMP8 dF/F at 30 and 10 Hz; and R² against a probe's miss distance (0-50 µm) for
probe radii 10, 25 and 50 µm.

## 8. Predictions

1. R1 and R2 ride within one seed-SD of R0 at both k.
2. R3 loses under 30% of R0's riding time; the transition lies between R3 and R3.5.
3. R4, recalibrated to its own passing scale, rides no better than the bypass minus the brain's lag; in
   practice, no better than random-k on R0.
4. R5 fails the pre-test at every scale.
5. If R4 at its own calibration rides as well as R0 at k = 32, closed-loop riding is not a valid acceptance
   test, and Track B becomes the headline result.

## 9. Already run (not confirmatory)

- Balance gate on R0: jobs 37491-37494 (2026-10-17/18), 4.0 and 4.5 m/s, seeds 201 and 202, hand-picked
  readout list (`--readout base`), reaching 9.6-11.8 s and 11.9-13.7 s.
- Pre-test pilot on R0, R4, R5 at scales 0.47-1.5 (2026-10-29, 8 brains, one draw): R4 and R5 near silent at
  0.47; R4 reaches 46-63% of R0's activity and 14-17 lateralised outputs at 1.5.
- Pre-test on R1, R2, R3, R3.5 at 0.47 (2026-11-02, CPU, 8 brains, draw 1; `site/data.json`): network
  spikes/s and lateralised outputs VS / haltere: R1 13,700, 15 / 16 (VS null max 24); R2 25,300, 23 / 28;
  R3 15,900, 25 / 20; R3.5 890, 0 / 0. R3.5 is as silent as R4 and R5; R3 transmits. This was seen before the
  tag, so prediction 2 is not a blind prediction for the pre-test; it remains one for riding.

## 10. Deviations

(none yet)
