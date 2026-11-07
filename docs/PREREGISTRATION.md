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
  State on 2026-11-06 01:10: R3 seed 201 finished its 60 generations (job 38043): 11.5 s in the last generation
  with 42% of riders finishing, against 13.7 and 11.9 s in the last generations of R0's two seeds (58 and 57
  generations). That is 10% below R0's mean and 16% below the same CEM seed, inside prediction 2's 30% bound.
  Seed 202 is at generation 41 (10.7 s). One rewiring draw, one finished seed, hand-picked readout: a pilot, not
  the test of prediction 2.
  State on 2026-11-06 04:50: R3 seed 202 finished its 60 generations (job 37952): 11.1 s in the last generation
  with 52% of riders finishing, against 11.9 s (52%) for R0's seed 202. Over the two seeds R3 rides 11.3 s
  against R0's 12.8 s, 12% below (seed by seed 16% and 6% in the last generation; over each search's last five
  generations 15% below and 4% above), inside prediction 2's 30% bound. One rewiring draw,
  two CEM seeds, hand-picked readout: still a pilot. The R1 ride (job 38038) started on 2026-11-06 04:20.
  State on 2026-11-06 13:00: R1 finished its 60 generations (job 38038, CEM seed 201): 7.0 s in the last
  generation with 8% of riders finishing, against 13.7 and 11.9 s for R0's two seeds. That is 45% below R0's mean
  (12.8 s) and 4.5 seed-SDs below it (R0's two seeds: SD 1.29 s, from only two values); over each search's last five
  generations it is 7.6 s against 12.4 s, 3.4 SDs below (SD 1.41 s). It is also 38% below R3 (11.3 s). **This goes against prediction 1 as drafted.** The
  prediction is left as written; this line records that the pilot went against it, and point 7 of section 9a
  lists what to decide. The pilot is not the test of prediction 1: hand-picked readout, one rewiring draw, one
  CEM seed, one speed. Its deficit is in holding the lane (see the replays below), which the top-k readouts of
  prediction 1 do not do on R0 either (7.2 and 6.2 s; point 5 of section 9a). The R1 search also ended without
  using the readout's matched-filter lane signal (gain +0.01, against -0.12 to -0.19 in the four searches on R0
  and R3), and the lane filter and operating point built for R1 came out differently (fly-brain
  `docs/CURRENT_NUMBERS.md`), so the brain, its lane filter and this one search are not yet told apart. In this draw 8,584 of 166,700 neurons change sign (5.1%); none of the 44 driven VS and HS cells is
  among them, and 4.4% of the synapses onto the readout's neurons come from a neuron that changed sign (5.1%
  over the brain). R1's network runs at about 70% of R0's rate, averaged over all 48 brains for a
  whole generation of the search (ended rides included).
  Replays of each search's final mean decoder, 48 riders, one replay seed (fly-brain jobs 38092 to 38101): with
  the off-road rule 46 and 44 of 48 ride the full 15 s on R0, 22 and 28 on R3 and 10 on R1, and 86 of the 90
  rides that end early end at the road edge (4 in a fall); without the rule 235 of the 240 riders are upright at
  15 s (48 and 48, 48 and 44, 47), with 1 and 3, 18 and 10, and 35 of them more than 3.5 m from the center line.
  So these decoders balance on all three wirings, and the rungs differ in how well they hold the lane. Without
  the rule the riders that leave the road drift to one side, the same for R1 and both R3 decoders (all 35 on R1,
  17 of 18 and 10 of 10 on R3).
  Two more R1 pilots tell the draw from the search seed: draw 2 with CEM seed 201 (job 38107, started on
  2026-11-06 14:23) and draw 1 with CEM seed 202 (job 38108, started 20:10 when the R2 ride ended).
  State on 2026-11-06 20:30: R2 finished its 60 generations (job 38039, CEM seed 201, draw 1): 13.4 s in the
  last generation with 69% of riders finishing, against 13.7 and 11.9 s for R0's two seeds; 5% above R0's mean
  (12.8 s), 0.5 seed-SD above it (over each search's last five generations 13.0 against 12.4 s, also 0.5 SD).
  So with the hand-picked readout, on one draw and one seed, R2 is inside prediction 1 and R1 is not. R2's
  decoder uses the lane signal like R0's (gain -0.11 against -0.12 and -0.16) and its lane filter and operating
  point came out like R0's, where R1's did not.
  State on 2026-11-06 22:45: R1 on rewiring draw 2 finished its 60 generations (job 38107, CEM seed 201): 11.8 s
  in the last generation with 40% of riders finishing, 8% below R0's mean and 0.8 seed-SD below it (over each
  search's last five generations 11.5 against 12.4 s, 0.6 SD); 4% above R3's mean. So R1 is inside prediction 1
  on draw 2 and 4.5 SDs outside it on draw 1, with one CEM seed each. Draw 2's search used the lane signal (gain
  -0.14) and its network rate is as low as draw 1's (about 73% of R0's), so the rate is not what set draw 1
  apart.
  State on 2026-11-07 04:15: R1 on draw 1 with CEM seed 202 finished (job 38108): 12.3 s in the last generation
  with 56% finishing, 4% below R0's mean and 0.4 seed-SD below it (last five generations 11.8 against 12.4 s,
  0.4 SD); 3% above R0's seed 202 and 8% above R3. Same brain, same lane filter and operating point as the
  7.0 s search (byte-identical `probe.json` and `zbar_mu.npy`), lane-filter gain -0.135. So the two searches
  on draw 1 end 5.3 s apart, nearly three times R0's seed-to-seed gap: the 7.0 s pilot was a stalled search, not a
  property of the draw. Of the three R1 pilots (7.0 and 12.3 s on draw 1, 11.8 s on draw 2) two are inside
  prediction 1; their mean is 19% below R0. Replays of the seed-202 decoder (jobs 38122, 38123): with the rule
  14.7 s, 44 of 48 finish, 4 leave the road, none falls; without it all 48 upright, 1 beyond 3.5 m (median
  0.9 m): R0's result on the brain whose seed-201 decoder kept 10 of 48 on the road. So with this readout the
  lane result on R1 is as much the search's as the wiring's.
  State on 2026-11-07 13:00: R2 with CEM seed 202 finished (job 38125): 13.5 s, 75% finishing, 0.04 s from its
  seed 201; replay 43 of 48 finish, none falls. A third R0 seed (job 38124, seed 203), run like the rung pilots
  on CPU for 60 generations (the first two: GPU, 58 and 57), rides 10.9 s, 40% finishing, below both GPU seeds.
  Three-seed R0: mean 12.2 s, SD 1.42 s (last five generations: 11.95 and 1.23 s). Against it: R2 +10% and +11%
  (0.9 SD each), R3 -6% and -8% (0.5 and 0.7 SD), R1 +1% and -3% for the two unstalled searches (0.1 and
  0.3 SD) and -42% for the stalled one (3.6 SD). Every pilot but the stalled R1 search is within one seed-SD of
  R0; by rung mean R2 +10%, R3 -7%, R1 -15%. Replays of the seed-203 decoder (jobs 38130, 38131): with the rule 14.3 s, 38 of 48 finish, 10 leave the road,
  none falls; without it all 48 upright, 5 beyond 3.5 m (median 1.2 m), between the GPU seeds' decoders and R3's.
  Started 2026-11-07 13:00: pilot rides on a second rewiring draw of R3 (job 38134) and of R2 (job 38135), seed 201. Replays of R2's final mean decoder
  (jobs 38118 and 38119): with the off-road rule 14.7 s, 46 of 48 finish, 2 leave the road, none falls; without
  it all 48 upright and all within 3.5 m of the center line (median 0.9 m), like R0's two decoders. Replays of
  R1 draw 2's decoder (jobs 38120 and 38121): with the rule 13.5 s, 29 of 48 finish, 15 leave the road, 4 fall;
  without it 39 of 48 upright and 9 fall (more than any other replayed hand-picked decoder, 0 to 4), 7 of the 39 beyond
  3.5 m. So draw 2 holds the lane about like R3 and balances a little less reliably than the other hand-picked decoders.

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
   The screens finished on 2026-11-05 (R0 to R3). Curves: the project page.
   Top-8, finished 2026-11-06 04:20: the search reached the hands-off level (5.7 s) in generation 7 and stayed
   between 5.8 and 7.9 s, 7.2 s in generation 29 with 6% of riders finishing, where the hand-picked readout rode
   9.5 and 10.8 s. A replay of the search's final mean decoder (fly-brain job 38077, 48 riders): 9.0 s upright, 7
   ride all 15 s, 41 leave the road, none falls; the hands-off bike loses 3 of 16 to a fall and 13 to the road
   (the gate's final mean decoders, replayed later, ride 14.8 and 14.5 s with 46 and 44 of 48 finishing; at
   generation 29, like for like is 7.2 s against 9.5 and 10.8 s).
   So the top-8 readout balances and does not hold the lane, as feared. The hand-picked readout has more neurons
   (9 of its 42 types picked by the HS lane probe), a matched-filter lane signal and a different search setup
   (zbar operating point, uncentred roll features, 300 ms lane smoothing), and this run does not say which of
   these it needs; the top-32 search tests only whether more roll-rate-ranked neurons are enough.
   Bypass, finished 2026-11-06 08:35 (job 38037, the same search as top-8, reading the 10 sense populations):
   13.9 s in generation 29 with 77% of riders finishing, 13.2 s over generations 25 to 29, where top-8 rode 7.1 s
   and the hand-picked readout 9.9 and 10.6 s; the hand-picked searches ended on 13.7 and 11.9 s after 58 and 57
   generations. A replay of its final mean decoder (job 38081, 48 riders): all 48 ride the full 15 s and end
   0.5 m from the center line on average. So the bypass rides at about the level the better hand-picked search
   reached, and can serve as the ceiling section 5 takes it to be. The check on that: the driven
   neurons also receive synapses from the rest of the brain (486,000 in all), so the same search was repeated
   with every synapse off (job 38086, `ride-readout.sbatch ... bypass0`). It rides 13.9 s in generation 29 with
   81% finishing and is never more than 0.085 s from the bypass in any of the 30 generations, so the bypass
   does not need the wiring: with every synapse off it rides the same (one seed). The search set-up the bypass shares with top-8 holds the lane when the features
   carry it (the HS populations are given heading and lane offset directly). So what top-8 lacks is not the
   centring or the operating point of the search. Still open: which neurons it reads, and whether single
   neurons need the matched filter and the 300 ms lane smoothing (the bypass reads means over 5 to 247 neurons,
   top-8 eight single neurons). Top-32, finished 2026-11-06 12:12 (job 38078): 5.3 to 7.7 s from generation 4 on,
   6.2 s in generation 29 with no rider finishing. Its replayed final mean decoder (jobs 38104, 38105) loses 46
   of 48 to the road and none to a fall; without the off-road rule it keeps all 48 upright for 15 s with 44 more
   than 3.5 m from the center line. So in this one search more roll-rate-ranked neurons did not supply the lane. In R0's
   screen no descending neuron follows the lateral offset closely (largest |r| 0.29, against 0.65 for roll rate;
   the top 32 by roll rate reach 0.14), so a second ranking of the same screen by lane offset is not an obvious
   source of a lane signal; the hand-picked readout's lane neurons come from the HS probe, which each rung run
   already makes on its own brain. To decide:
   whether the per-brain readout gets a lane signal of its own (for example a second screen ranked by
   lane offset), or whether riding time is scored without the off-road rule. For that choice, replays of fixed
   decoders on 2026-11-06 (48 riders, seed 201, fly-brain jobs 38082 to 38084): without the off-road rule the
   top-8 mean decoder keeps all 48 riders upright for 15 s (34 end more than 3.5 m from the center line; the
   median over all 48 is 7.7 m), and the hands-off bike loses 46 of 48 to a fall (the 48 last 8.6 s on
   average); with the rule the hands-off bike rides 5.4 s (41 leave the road, 7 fall; the 5.7 s above is from
   the earlier replay with 16 riders and stays the hands-off floor of section 5). So without the rule the
   hands-off bike still falls, but the replayed top-8 mean decoder is already at the 15 s cap. No search has run
   without the rule, so the last-generation mean of section 5 is not measured without it (with the rule it was
   1.1 s below the replay for the bypass and 1.8 s for top-8); if it also ends near the cap, there is no room
   above top-8 unless rides get longer or gusts stronger. The replays of the hand-picked readout on R0, R3 and R1
   (section 9, jobs 38092 to 38101) bear on the same choice: without the rule the three wirings all end within
   0.4 s of the 15 s cap, and with it they ride 14.8 and 14.5 s, 12.3 and 12.7 s, and 10.1 s. On that evidence, with the hand-picked readout at 15 s and 5 N·m the off-road rule is what separates R0, R3
   and R1; a score without it would put all three at the cap. (R4 at 1.2 rides under 2 s and would be separated
   either way.) This is for a readout that has a lane signal. The top-k readouts have none on R0, so these
   replays do not show that the rule would separate the rungs with top-k. One replay seed per decoder, fixed
   decoders from searches that had the rule on. The random-k pilot (8 neurons, one draw, job
   38079) finished on 2026-11-06 14:23: 3.5 to 4.6 s from generation 3 on, 4.1 s in generation 29 with no rider
   finishing, below the hands-off floor. Its replayed final mean decoder (jobs 38111, 38112) is close to blank
   and rides about like the hands-off bike: 5.5 s with 38 of 48 leaving the road and 10 falling (hands-off: 5.4 s,
   41 and 7); without the off-road rule all 48 fall (7.8 s; hands-off: 46 fall, 8.6 s). So top-k separates from random-k on balance (top-8 and top-32 keep all 48 replayed
   riders upright), and neither holds the lane. Numbers: fly-brain `docs/CURRENT_NUMBERS.md`, "Readout pilot on the real wiring" and
   "Replays with and without the off-road rule".
6. Prediction 3's first bound. On the real wiring the bypass pilot rides 13.9 s in generation 29 (job 38037),
   about where the better hand-picked search ended (13.7 s after 58 generations) and 6.7 s above R0's own top-8
   readout (7.2 s). "No better than the bypass" therefore holds for the real wiring too and cannot separate R4
   from R0. Proposed: test prediction 3 by its second clause only (no better than random-k on R0). The
   random-8 pilot (job 38079, one draw of the 8, one CEM seed) is in: 4.1 s in generation 29, below the
   hands-off bike (5.4 to 5.7 s); its replayed final mean decoder rides 5.5 s, like the hands-off bike
   (point 5). So the bound is either random-k's last generation (4.1 s here) or the hands-off level, and an R4
   that rode 5 s would be above one and below the other; which one has to be fixed before the tag. The R4
   pilot at 1.2 rode 1.7 s in generation 24, where it was paused, below both. It used the hand-picked readout,
   which prediction 3 does not cover, so it is not the test of this clause. Still to decide.
7. Prediction 1 (R1 and R2 ride within one seed-SD of R0 at both k): one of the three R1 pilots went against
   it; the other two (0.4 and 0.8 seed-SD below R0) and both R2 pilots (0.5 seed-SD above) were inside it
   (section 9; against the three-seed R0 mean of 12.2 s with SD 1.42 s the same holds: R1 0.1 SD above and 0.3 SD below,
   R2 0.9 SD above, the stalled search 3.6 SD below). The first draw-1 pilot rode 5.8 s and 4.5 seed-SDs below R0, with the hand-picked readout, one
   CEM seed and one speed; a second CEM seed on the same draw, with the same lane filter, rode 12.3 s, so that
   pilot was a stalled search. The pilot is not the prediction's test, and in the replay its deficit is in the lane, not in balance:
   without the off-road rule 47 of 48 riders are upright at 15 s, 35 of them more than 3.5 m from the center
   line. The top-k readouts the prediction is written for have no lane signal (point 5). On R0 itself they ride
   7.2 s (k = 8) and 6.2 s (k = 32) after 30 generations, about where the R1 pilot ended (7.0 s after 60). So
   the pilot says little about how R1 compares with R0 at top-k. Either keep the prediction and report how
   it comes out in the confirmatory runs, or restate it before the tag. All three R1 pilots are in hand. Also to
   settle: "one seed-SD" is 1.4 s from the three R0 seeds run so far (1.3 s from the first two; the third, on
   CPU, rode 10.9 s), while the two R1 searches on draw 1 differ by 5.3 s, so with 5 CEM seeds one stalled search can move a rung's mean by about 1 s, most of a seed-SD, on its own; the
   prediction's test might be better stated on the median over seeds, or on the best generation of each search
   (to decide before the tag). The stalled R1 search rode worse than R3; the other two R1 pilots rode 4% and 8%
   better than R3.

## 10. Deviations

(none yet)
