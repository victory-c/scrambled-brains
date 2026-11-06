# Scrambled Brains: preregistration (draft, 2026-11-02)

**Status: draft.** This becomes the preregistration when it is tagged in this repository before the first Track A
run (section 5: per-brain readouts) on a scrambled rung. Everything run before the tag is listed under "Already run"
and is not confirmatory. That includes pilot rides on scrambled rungs with the balance gate's hand-picked readout,
which began on 2026-11-05 on rewiring draw 1: because of them the riding predictions in section 8 are informed by
pilot data, not blind. The confirmatory runs use per-brain readouts and include rewiring draws the pilots never saw.
Changes after the tag go in a dated "Deviations" section at the end, never by editing the text above it.

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
neurons with |z| > 3 between left and right brains exceeds the largest value over the balanced relabellings
(the null: all 18 with 8 brains; 1,000 drawn at random from the 19.3 million with 30 brains, `--null-splits`),
for both VS and haltere drive, and (b) the network rate outside the driven neurons is within 2x of
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
- Confirmatory pre-test on R1 at 0.47 (2026-11-03, CPU, 30 brains, draw 1, 1,000 random balanced relabellings):
  13,000 / 14,300 network spikes/s; 35 / 31 lateralised outputs against null maxima of 4 / 13 (95th percentile 1).
  R1 passes the gate. So, before the tag, R1, R2 and R3 pass at 0.47 and R3.5, R4 and R5 fail at 0.47.
- Pre-test with 30 brains over the whole scale ladder (2026-11-05, CPU; table in fly-brain
  `docs/CURRENT_NUMBERS.md`, data in `site/data.json`). R0, R1, R2 and R3 pass at 0.47 (31 to 50 lateralised
  outputs, null maxima 4 to 13). R3.5 fails at every ladder scale: 2,800 spikes/s at 0.47, 117,000 at 0.6. R4
  passes at none of the ladder scales run with 30 brains (0.6 to 1.5): at 1.5 it has 21 / 35 lateralised outputs
  but 9,275 spikes/s on the VS probe (the window starts at 10,750); at 2.0 only the VS probe was run and it ran
  away (8 million spikes/s, 8 outputs against a null maximum of 14). R5 passes at 2.0 (12,000 / 11,200
  spikes/s; 7 / 8 outputs against a null maximum of 4 / 4) and fails below. **The R5 pass contradicts prediction 4
  as drafted.** The prediction is left as written; this line records that the pilot went against it.
- Fine scans between ladder steps (same date, exploratory, not on the ladder): R3.5 at 0.50 is inside the rate
  window (15,300 / 16,300, three quarters of the real rate) and has no signal (1 / 1 outputs, null maxima
  162 / 158); at 0.53 and 0.56 the rate is 48,000 and 83,000 and it still does not beat the null on both probes.
  R4 at 1.2: 3,000 / 3,500 spikes/s, 11 / 14 outputs (null maximum 1); at 1.6: 234,000 / 2.1 million, no signal
  on the VS probe.
- R4 in closed loop (same date): replaying the reference decoder, R4's rate over the first 0.6 s of riding is
  12,700 spikes/s per brain at scale 1.0, 39,400 at 1.2, 79,600 at 1.3, 327,000 at 1.4 and 1.2 million at 1.5;
  the real wiring is at 23,400 on the same window. Upright, the same R4 brains fire 1,200 to 9,000 and the real
  wiring 10,000 to 12,800. The upright pre-test therefore does not tell whether a rung is stable while riding.
  In the first generations of the pilot search R4 at 1.2 averages about three times the real wiring's rate
  (173,000 to 212,000 against 59,500 to 68,800), since most bikes have already fallen.
- Pilot rides, balance gate unchanged (hand-picked readout, 4.5 m/s, CEM seed 201, rewiring draw 1), on CPU
  because the GPU node has no working CUDA: R3 at 0.47 (fly-brain jobs 37938, 37946) and R4 at 1.2 (job 37945),
  started 2026-11-05 and continued across 24 h jobs. Curves: the project page.
  State on 2026-11-05 14:50: R3 seed 201 rides 7.0 s after generation 10 (R0's two seeds: 9.0 and 10.1 s) and
  passed the hands-off bike (5.7 s) in generation 8; a second CEM seed (202; jobs 37948, 37952, 37953) rides
  5.9 s after generation 5 (R0: 6.8 and 4.9 s). R4 at 1.2 stayed at 1.3 to 1.8 s through generation 24, below the
  hands-off bike, and was paused there. So far this agrees with prediction 2 and says nothing yet about its 30%
  bound; R4 was run with the hand-picked readout, which prediction 3 does not cover.

## 9a. Open points before the tag

These came out of the runs above and need a decision before this document is tagged.

1. The model-side rung (section 3) and the Track B prediction CSV (section 6) are not written yet.
2. Scale ladder: R3.5 and R4 go from too quiet to runaway inside one ladder step (0.47 to 0.6, and 1.5 to 1.6).
   Proposed: when a rung brackets the rate window between two ladder scales, bisect up to three times.
3. Where the scale is set: the rate criterion is measured upright, and the first 0.6 s of riding doubles the real
   wiring's rate but multiplies R4's by 10 to 22. Proposed: add a closed-loop check to section 4 (rate over the
   first 0.6 s of the reference replay within 2x of R0's 23,400, and the rate averaged over generation 0 of the
   search reported next to R0's), and set a rung's scale there. The replay's whole-run average is not usable for
   this: it depends on when the last rider falls.
4. Prediction 4 (R5 fails at every scale) is contradicted by the pilot at 2.0. Either keep it and report it as
   failed, or restate it (for example: R5's lateralised outputs stay under a quarter of R0's at every scale).
5. Track A readout: the top-k neurons are ranked by roll-rate correlation only, and the per-brain readout has no
   lane signal, so a rider can balance and still leave the road. This has to be piloted on R0 (top-k, random-k,
   bypass) before the design is fixed. Queued on CPU on 2026-11-05 as pilots on the real wiring only: per-brain
   screens (fly-brain job 38035), top-8 (38036) and bypass (38037), 30 generations each at 4.5 m/s, seed 201.

## 10. Deviations

(none yet)
