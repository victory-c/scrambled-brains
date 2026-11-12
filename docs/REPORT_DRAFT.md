# Scrambled Brains: interim technical report (draft, 2026-11-12)

> Draft for the 4 December report (milestone M3). Confirmatory runs are still in progress; numbers marked [pending] will be filled as rides finish. Source of every number: `fly-brain/docs/CURRENT_NUMBERS.md` and the result files it names.

## Abstract

This is an interim draft, dated 2026-11-12. The confirmatory runs are still in progress and no preregistered prediction has been tested yet.

We ask how much of the measured wiring a fixed-weight spiking model of the whole fly central nervous system needs before a decoder stops learning a closed-loop task. The model is the Shiu et al. leaky integrate-and-fire model on the male CNS v1.0 connectome, which has 166,700 neurons. The task is to ride a simulated bicycle for 15 s below its self-stable speed, with side gusts. We degrade the wiring along a ladder of seven rungs. R0 is the real wiring and R5 has uniformly random targets. Three tracks test each rung:

- **Track A:** closed-loop riding.
- **Track B:** decoder-free predictions of published behaviours.
- **Track C:** how well roll rate can be decoded from recorded neurons.

The plan was fixed by the tag `prereg-v1` on 2026-11-09.

So far, 14 of the 100 primary rides are done, all with CEM seed 211:

- **4.5 m/s, R0:** 12.79 s in the last generation (job 38263).
- **4.5 m/s, R1 to R3:** draws 3 to 5 ride between 10.47 and 14.65 s.
- **4.0 m/s:** R0 and three R1 draws have finished.

Outside the primary design, R3.5, R4 and R5 each get one ride (draw 1, CEM seed 211, 4.5 m/s, at their closed-loop scale). All three are done, on the CPU: 2.71, 2.96 and 4.34 s (jobs 38371 to 38373). That is below the 5.7 s that the bike rides with no steering.

The Track B confirmatory scores are finished: R1 scores 0.682, R2 0.993, R3 1.000, and every rung from R3.5 up scores 0.000 to 0.056.

[pending: medians over five CEM seeds, bootstrap intervals and the tests of predictions 1 to 3 and 5, about four weeks of queue]

## 1. Introduction

### 1.1 The question

Connectome-based models of the fly brain are built on measured wiring. That wiring contains errors. Synapse counts are noisy. Transmitter identity is predicted, not measured, for most neurons. It is not known how many such errors a whole-brain model can absorb before it stops working as a brain.

The preregistered question (`docs/PREREGISTRATION.md`, section 1) is this. On a closed-loop task that the body cannot solve by itself, how much of the measured wiring does a fixed-weight spiking model of the whole fly CNS need before a decoder stops learning the task? The decoder is learned on a fixed list of descending and motor cell types. A secondary version uses neurons screened on that brain.

There is also a secondary question. Do the same perturbations break the model's decoder-free predictions, and its decodability?

### 1.2 System and ladder in brief

The model is the Shiu et al. 2024 leaky integrate-and-fire model on the male CNS v1.0 connectome (166,700 neurons), driven by a simulated road bicycle through 789 sensory neurons (section 2.1). The task matters because the bike cannot do it on its own: with no steering it rides 3.5 s at 4.0 m/s and 5.7 s at 4.5 m/s (16 riders). On the real wiring, the balance-gate pilots before the tag learned to ride 9.6 to 11.8 s at 4.0 m/s and 11.9 to 13.7 s at 4.5 m/s (jobs 37491 to 37494).

The wiring ladder (section 2.2) goes from R0 (real wiring) through R1 (transmitter errors at the measured rate), R2 (synapse-count jitter) and R3 (targets redrawn within cell type and side) to R3.5, R4 and R5, which keep only degree and sign statistics. R1 and R2 model errors of the size the measured data may contain. The preregistered expectation is a transition between R3 and R3.5 (prediction 2). Because rescrambled brains fire far less at the same synaptic scale, each rung is gated by a transmission pre-test, and R3.5, R4 and R5 ride at their own closed-loop scale (section 2.3).

### 1.4 Why three tracks

Track A alone cannot settle the question, for two reasons.

**The primary readout favours R0.** It is a hand-picked list of 42 cell types (35 descending, 7 motor; 112 neurons on R0), plus one lane signal. The list was chosen on the real wiring, and the same names are read on every rung, whatever those neurons now receive. A rung that loses riding time is therefore not evidence by itself that the rung has no usable signal anywhere (preregistration section 5). A secondary readout, screened on each brain, is there for that question.

**A learned decoder might compensate for bad wiring.** Prediction 5 covers this case. Suppose R4, at its own scale, rides as well as R0 with the primary readout. Then closed-loop riding is not a valid acceptance test, and Track B becomes the headline result.

The three tracks therefore ask different things of the same brains:

- **Track A, closed-loop riding (section 5).** Can a decoder learn to ride on this brain? The search uses the cross-entropy method from a blank decoder: 48 riders × 15 s per generation, 60 generations, CEM seeds 211 to 215. It runs at 4.0 and 4.5 m/s. The outcome is the last-generation mean riding time, taken as a median over a rung's runs.
- **Track B, decoder-free predictions (section 6).** Does the brain still reproduce known behaviours with no learned decoder? There are six scored rows from published work and two controls (`docs/track_b_predictions.csv`):
  - Four feeding rows read MN9: the sugar response, bitter suppression, Ir94e suppression, and dose-response.
  - Two escape rows drive LPLC2 + LC4 and read the giant fiber DNp01 in one row, and DNp02 and DNp11 in the other.

  A row passes on a brain if its difference has the expected sign and is at least half as large as on the real wiring at scale 0.47.
- **Track C, decodability (section 7).** How many recorded neurons are needed to decode roll rate? Ridge regression maps spike counts in 100 ms bins to roll rate. N90 is the number of neurons needed to reach 90% of the R² that all the neurons of a site give together. There are two sites: brain descending neurons and nerve-cord wing-motor neurons. Neurons are added in screen order or in random order.

### 1.5 Status of this draft

The plan was tagged `prereg-v1` on 2026-11-09, before the first confirmatory Track A ride. Everything run before the tag is a pilot and is reported as one (preregistration section 9).

Pilot rides on draws 1 and 2 began on 2026-11-05. The riding predictions are therefore informed by pilot data, not blind. The confirmatory runs use rewiring draws 3 to 5 for R1 to R3 and CEM seeds 211 to 215, which no pilot used. R3.5, R4 and R5 ride draw 1, which the pilots used. So predictions 3 and 5, and the R3.5 clause of prediction 2, are not tested on a new draw.

One pilot already went against a prediction. Prediction 4, that R5 fails the pre-test at every scale, was contradicted before the tag: R5 passed weakly at 2.0. The pass gave 7 and 8 lateralised outputs against a null maximum of 4. The prediction was left as written. No deviations have been recorded since the tag (preregistration section 10).

As of 2026-11-12, these parts are done:

- **Confirmatory pre-test** on draws 3 to 5 (job 38261). Eight draws pass. R2 draw 3 fails on the null only and is ridden anyway, as preregistered.
- **Primary rides at 4.5 m/s** for CEM seed 211 only: R0 and the nine R1 to R3 draws (jobs 38263 to 38272).
- **Primary rides at 4.0 m/s** for seed 211 on R0 and R1 draws 3 to 5 (jobs 38710, 38714, 38728, 38735).
- **The single rides of R3.5, R4 and R5** (jobs 38371 to 38373, CPU).
- **The Track B confirmatory runs** (jobs 38414 to 38429).

Track C has only a pilot (job 38185, R0 to R3).

The rest of the queue runs one job at a time, as a relay, with about four weeks left (CURRENT_NUMBERS.md, "The queue as one chain").

[pending: CEM seeds 212 to 215 on every primary rung, both speeds; the 4.0 m/s rides of R2 and R3; the secondary design (top-32, random-32, bypass, model-side variants); prediction 3's replays; confirmatory Track C]

## 2. Methods

This section restates the confirmatory plan fixed by the git tag `prereg-v1` (2026-11-09), sections 2 to 8 of `docs/PREREGISTRATION.md`. Run details and job ids come from the fly-brain ledger `docs/CURRENT_NUMBERS.md`. Anything run before the tag is a pilot and is labelled as one. The preregistration's deviations section (section 10) reads "(none yet)".

### 2.1 System

**Connectome.** We use male CNS v1.0 (Janelia FlyEM, Cambridge, Google; CC BY 4.0). It has 166,700 neurons, 25,582,938 connections and 124,177,616 synapses (fly-brain `brain/connectome.py`).

**Neuron model.** We use the Shiu et al. 2024 leaky integrate-and-fire model. It has one free parameter, `w_syn` = 0.275 mV, multiplied by a global synapse scale. Scale 1.0 is Shiu's value. The male CNS is calibrated at 0.47, giving `w_syn` 0.129 mV (`runs/calibrate_wsyn.py`, `results/calibrate_wsyn.json`, job 36539). Our simulator matches Brian2 spike for spike: 2,101 spikes over 100 ms in a 500-neuron network (`tests/test_brian2.py`). That test last passed on 2026-10-29 on the login VM.

**Body.** The body is a road bicycle (Whipple model). Its matrices match Meijaard et al. 2007 to within 1e-8. With a 70 kg rider the bike is self-stable from 4.70 to 7.74 m/s. The brain receives VS/HS optic flow, halteres, Johnston's organ and front-leg proprioceptors through 789 driven sensory neurons (fly-brain `bike/`).

**Task.**
- The fly rides for 15 s at a held speed below the self-stable range.
- Side gusts of 5 N·m push the bike.
- A run ends at a fall or when the bike leaves the road (|y| > 3.5 m).
- Pedal power is fixed to hold the speed: 23.1 W at 4.0 m/s and 29.6 W at 4.5 m/s, as in the balance gate (jobs 37491 to 37494). The brake is off.
- "Riding time" is the time until a fall or leaving the road (`upright_mean` in `cem.json` "history").

**Hands-off floor.** This is a replay with no steering, 16 riders × 15 s, seed 201, run on the login VM's CPU (no job id):
- 4.0 m/s: 3.5 s (`results/gate/v4.0_s201/handsoff_trace.json`).
- 4.5 m/s: 5.7 s (`results/gate/v4.5_s201/handsoff_trace.json`).

### 2.2 The wiring ladder

Every rung is generated by fly-brain `brain/variants.py`. The seed is the rewiring draw.

| Rung | What it changes | What it keeps |
|---|---|---|
| R0 | nothing (real wiring) | everything |
| R1 | relabels 6% of neurons to another transmitter, drawn by frequency; the sign flips only where the class (chloride vs. other) changes | wiring; 94% per-neuron transmitter accuracy, after Eckstein et al. 2024 |
| R2 | multiplies each synapse count by a lognormal factor, median 1, sigma = ln 1.25 | wiring, signs, degrees |
| R3 | redraws each target within the same (cell type, side) | the (type, side) synapse matrix; out-degree, output synapses, signs |
| R3.5 | permutes targets among connections of equal sign and synapse count | in-degree, incoming synapse total, excitatory/inhibitory input mix, and everything the sender keeps |
| R4 | permutes all targets | in-degree, out-degree, output synapses, signs |
| R5 | draws targets uniformly | out-degree, output synapses, signs |

Draw 1 of each rung was generated on 2026-11-02 (ledger, "The wiring ladder"):
- **R1:** 9,907 neurons relabelled (5.9%) and 8,584 changed sign (5.1%). The inhibitory share of synapses goes from 38.4% to 40.2%.
- **R2:** 127,344,656 synapses (+2.6%).
- **R3:** keeps 39.4% of the original connections.
- **R3.5:** keeps 0.6%.
- **R4:** keeps 0.58%.
- **R5:** keeps 0.27%.

**Model-side rung.** This rung moves R0's neuron model instead of its wiring. Each of six variants changes one parameter by ±10%: the synaptic scale, the membrane time constant or the synaptic time constant. It puts wiring error next to neuron-model error of the same size.

### 2.3 Transmission pre-test (gate for Track A)

The pre-test is fly-brain `runs/pretest.py`.

**Procedure.**
- The bike is held upright at 4.5 m/s with every sense at cruise rate.
- Half the brains get +30 Hz on the left VS (or haltere) inputs; the other half get it on the right.
- Each brain runs a 300 ms warm-up, then 1 s.
- There are 8 brains per cell, and 30 for the confirmatory run.

**Pass rule.** A rung passes at synapse scale s if both conditions hold:
- (a) The number of descending and motor neurons with |z| > 3 between left and right brains exceeds the largest value over the balanced relabellings. With 8 brains the null is all 18 relabellings. With 30 brains it is 1,000 drawn at random from the 19.3 million that exist (`--null-splits`). This must hold for both VS and haltere drive.
- (b) The network rate outside the driven neurons is within 2× of R0's rate at 0.47 (21,500 spikes/s), so between 10,750 and 43,000.

**Scales tried.** In order: 0.47, 0.6, 0.8, 1.0, 1.5 and 2.0. When a rung brackets the rate window between two ladder scales, the interval is bisected up to three times.

**Closed-loop riding scale.** The upright gate under-drives the network. In R4's pilot, the first 0.6 s of riding multiplied its rate by 10 to 22 at scales 1.0 to 1.3 (ledger, "R4 in closed loop"). So each rung's riding scale is set in closed loop:
- The reference replay is the balance gate's decoder `results/ride_slow_mu.json`, replayed on that brain (`ride-rung.sbatch` with `GENS=0`, then `tools/replay_rate.py`).
- From the scales run upright, the rung rides at the one whose rate over the first 0.6 s of that replay is closest in ratio to R0's 23,400 spikes/s (smallest |log(rate / 23,400)|). That rate must also be within 2× of R0's.
- R1, R2 and R3 are not rescaled. They ride at 0.47 on every draw.
- A rung that fails the upright gate at every scale gets one confirmatory Track A seed at this closed-loop scale.
- A rung with no scale inside the closed-loop window gets no ride.

**Status of the pre-tests.**

| Run | When | Result | Source |
|---|---|---|---|
| Draw 1, 30 brains per cell (pilot) | before the tag | R0 to R3 pass at 0.47. R3.5 fails at all nine scales run (0.47 to 2.0). R4 fails at every scale from 0.47 to 1.6. R5 passes at 2.0 only, with 7 and 8 lateralised outputs against a null maximum of 4. | jobs 37927, 37928, 37936, 37937, 37940 to 37942, 37947 |
| Confirmatory draws 3 to 5, 30 brains, scale 0.47 | 2026-11-09, after the tag | Every R1 and R3 draw passes. R2 draw 4 and R2 draw 5 pass. R2 draw 3 fails on the null only: 21 and 20 outputs against null maxima of 155 and 160. As preregistered, it is ridden anyway and enters the medians. | job 38261 |
| Closed-loop scale of R3.5 and R5 | after the tag | First-0.6 s rates against R0's 23,388 spikes/s: R3.5 20,763 at 0.47 (0.89×); R5 37,752 at 2.0 (1.61×). By the rule, R3.5 rides at 0.47, R5 at 2.0 and R4 at 1.2 (from its pilot, 1.66 to 1.68×). No bisection was needed. | jobs 38363 to 38368 |

### 2.4 Track A: closed-loop riding

**Speeds and criterion.**
- Rides run at 4.0 and 4.5 m/s.
- The criterion is the mean riding time over the 48 riders of the last generation, together with the fraction riding the full 15 s.

**Search.**
- The search is the cross-entropy method (CEM), starting from a blank decoder.
- Each generation has 48 riders × 15 s, an elite of 25% and sigma0 as in the balance gate.
- Each search runs 60 generations (`GENS=60`).
- Jobs are capped at 340 min. A run stopped by the cap is resumed until generation 60, and the resumed segment reseeds the search.
- CEM seeds 211 to 215 are used, the same on every rung. No pilot used them.
- All runs are on the GPU. A run that has to use the CPU is reported as such and still counts.

**Primary readout.** This was decided on 2026-11-09 (preregistration section 9a, point 5).
- It is the balance gate's hand-picked list of 42 cell types: 35 descending and 7 motor, 112 neurons on R0.
- It adds one lane signal: a matched filter over the list's neurons, weighted by that brain's own HS probe, with 300 ms smoothing (`ride-rung.sbatch`).
- The same names are read on every rung. The list was chosen on the real wiring, so it favours R0.
- It was chosen after pilot rides on rewiring draws 1 and 2, so the riding predictions are informed by pilot data, not blind.

**Secondary readout.**
- Each brain gets its own passenger screen (`runs/screen.py --brain`).
- The decoder reads the 32 descending neurons ranked highest by roll-rate correlation, plus up to 12 descending (type, side) groups picked by that brain's HS probe (those with |z| ≥ 3). These go through its matched filter with 300 ms smoothing (`ride-readout.sbatch ... topk 32`, `LANE_K=12`).
- Random-32 draws its 32 neurons at random from the same pool and uses the same lane channel.
- `bypass` reads the 10 sense populations directly and serves as a ceiling.
- On R0's pilot, top-32 plus lane did not hold the lane. Its results are read as a floor, and only prediction 3 uses it.

**Primary design (100 rides).**
- R0: 5 CEM seeds × 2 speeds.
- R1, R2 and R3: each with rewiring draws 3, 4 and 5 × 5 CEM seeds × 2 speeds.

**Secondary design (about 40 rides, after the primary design; 4.5 m/s unless stated).**
- Top-32 plus lane on R0 (5 seeds), on R1 to R3 (draws 3 to 5, seed 211) and on R4 (draw 1, seed 211, scale 1.2).
- Random-32 plus lane on R0 (`READOUT_SEED` 0, 1 and 2; seed 211).
- Bypass on R0 (seed 211, both speeds).
- The six model-side variants with the primary readout (seeds 211 to 213).

**Single rides.** R3.5, R4 and R5 each get one ride: primary readout, draw 1, seed 211, 4.5 m/s, at the closed-loop scale. R5 passes the upright gate at 2.0 only, weakly, and is treated like the rungs that fail it.

**Primary outcome and statistics.**
- The primary outcome per rung and speed is the last-generation mean riding time, as a median over the rung's runs: 5 for R0 and 15 for each of R1 to R3.
- Every run's value and final lane-filter gain are reported. No stall criterion is applied and no run is excluded (section 9a, point 8).
- The CI against R0 is descriptive. It uses 10,000 bootstrap replicates with RNG seed 0. Each replicate resamples the 5 CEM seeds once, shared by all rungs and speeds. Independently, it resamples each rung's 3 draws once.
- The statistic is median(rung) − median(R0), in seconds, with a 95% percentile interval.
- Secondary outcomes are the finish fraction and the generations needed to reach half of R0's final riding time ("never" at generation 60).

**Held-out tests (descriptive).** Each primary run's final mean decoder (CEM mu) is replayed under conditions not used in the search and not used by any prediction:
- unseen gust seeds 301 and 302;
- the training speed ±0.5 m/s, with the pedal bias reset to hold the test speed.

These replays use `tools/heldout.py` and `heldout.sbatch`, with 48 riders and 15 s. The speed conditions reuse replay seed 301.

**Status on 2026-11-12.** Primary rides done so far: 14 of 100.

| Speed | Rides done | Jobs |
|---|---|---|
| 4.5 m/s, seed 211 | R0, R1 draws 3 to 5, R2 draws 3 to 5, R3 draws 3 to 5 | 38263 to 38272, all on the GPU |
| 4.0 m/s, seed 211 | R0, R1 draws 3 to 5 | 38710, 38714, 38728, 38735 |

- Each of these 14 rides also has its held-out replays.
- The single rides of R3.5, R4 and R5 are done. They ran on the CPU (jobs 38371 to 38373) because the GPUs were taken.
- [pending: seeds 212 to 215 on every rung, and 4.0 m/s for R2 and R3; these fill the medians, the seed-SD and the bootstrap CI.]
- [pending: the secondary design.]

### 2.5 Track B: decoder-free predictions

**Rows.** The predictions are the rows of `docs/track_b_predictions.csv`. Each source was read for this purpose on 2026-11-09. Six rows are scored:

| Row | Stimulus | Readout | Comparison | Expected sign |
|---|---|---|---|---|
| sugar_mn9 | sugar GRNs (LB3b-d LB4b), both sides, 150 Hz | MN9 L+R spike rate | sugar vs no stimulus | + |
| bitter_suppression | sugar + bitter GRNs (LB1a-d), both sides, 150 Hz each | MN9 L+R | sugar+bitter vs sugar alone | − |
| ir94e_suppression | sugar + Ir94e GRNs (LB1e LB2a-c), both sides, 150 Hz each | MN9 L+R | sugar+Ir94e vs sugar alone | − |
| dose_response | sugar GRNs, both sides, at 20 Hz and at 100 Hz | MN9 L+R | 100 Hz vs 20 Hz | + |
| loom_gf | LPLC2 + LC4, both sides, 150 Hz | giant fiber DNp01 L+R | drive vs no stimulus | + |
| loom_dnp02_dnp11 | LPLC2 + LC4, both sides, 150 Hz | DNp02 and DNp11 | drive vs no stimulus | + |

Two control rows are reported and not scored. Both expect 0: bitter GRNs alone to MN9, and sugar GRNs to the giant fiber.

**Scoring rule.**
- A scored row passes on a brain if its difference has the expected sign and is at least half as large as on the real wiring at scale 0.47. This holds whatever scale the rung is scored at.
- A row without the expected sign on the real wiring passes on no brain.
- A rung's score is the fraction of scored rows passed. It is the mean over 100 draws for R1 and R2 and over 3 draws for the shuffles.
- Each rung is scored at its calibrated scale and at 0.47 (`runs/predictions.py`, `tools/track_b_score.py`).

Four choices were made after a pilot had been seen, so they are not blind:
- the half-of-R0 criterion;
- the choice of rows;
- the bilateral drive;
- dropping two rows that failed on the real wiring.

**Confirmatory run.**
- The run used `trackb-conf.sbatch` on the CPU (`results/track_b/confirmatory/`).
- R1 and R2 used draws 101 to 200. R3, R3.5, R4 and R5 used draws 3 to 5. These draws were picked before any run, so that no Track B pilot had used them.
- Every rung was scored at 0.47, and R4 also at 1.2 and R5 at 2.0.
- R0's reference is job 38414 and a one-draw test is job 38415. Jobs 38416 to 38429 ran the rest (218 brains, no failed draw).
- The preregistration states no numerical Track B prediction.

### 2.6 Track C: decodability

Ridge regression maps recorded spike counts to roll rate. Counts are in 100 ms bins, as in the replay exports.

**N90** is the number of neurons needed to reach 90% of the R² that all the neurons of a site give together. Each site uses its own R² (decided 2026-11-09, section 9a, point 9).
- Neurons are added in screen order, and in random order over all of the site's neurons, silent ones included.
- There are two sites: a brain descending-neuron site and a nerve-cord wing-motor site.

The preregistration also specifies:
- the same analysis from simulated jGCaMP8 dF/F at 30 and 10 Hz;
- R² against a probe's miss distance (0 to 50 µm) for probe radii of 10, 25 and 50 µm.

**What has run.** Only a pilot has run (2026-11-08, before the tag).
- It used R0 to R3 on draw 1, with one replay per brain of a final mean decoder (jobs 38178 to 38181).
- `tools/track_c.py` did the fit (job 38185, `results/track_c/<rung>.json`).
- It recorded 1,314 descending and 67 wing motor neurons, giving 7,200 samples per brain.
- It used five folds over riders and 20 random orders.

[pending: Track C on the confirmatory rides; the jGCaMP8 and probe-distance analyses; and R3.5 to R5, which had no decoder to replay when the pilot ran.]

### 2.7 Preregistered predictions

These are the predictions of preregistration section 8, in substance.

1. **P1.** R1's and R2's primary outcome lies within one seed-SD of R0's at each speed. The seed-SD is the SD (n − 1) of R0's five last-generation means at that speed. P1 holds only if |median(rung) − median(R0)| ≤ SD for R1 and for R2 at both speeds. Each of the four comparisons is reported.
2. **P2.** At each speed, R3 loses under 30% of R0's riding time: 1 − median(R3)/median(R0) < 0.30. The transition lies between R3 and R3.5: at 4.5 m/s, R3.5's one ride is below 70% of R0's primary outcome. If R3.5 had no closed-loop scale, this clause would be reported as not tested.
3. **P3.** R4, recalibrated to its own passing scale, rides no better than random-32 on R0. The test replays the final mean decoder of R4's top-32 plus lane ride (48 riders, 15 s, off-road rule on, replay seed 201). It must ride no longer than the median of R0's random-32 plus lane replayed decoders (`READOUT_SEED` 0, 1 and 2) at 4.5 m/s. R4's primary-readout ride is reported next to it.
4. **P4.** R5 fails the pre-test at every scale.
5. **P5.** If R4's single ride at 4.5 m/s, at its own calibration, rides as well as R0 with the primary readout, then closed-loop riding is not a valid acceptance test and Track B becomes the headline result. "As well as R0" means at or above R0's primary outcome minus one seed-SD. If it does not, that does not show riding is valid, because the list was chosen on R0.

**Status.** No prediction has been tested yet.
- P1, P2 and P5 need R0's median and seed-SD over five CEM seeds. [pending: CEM seeds 212 to 215.]
- P3 needs the secondary top-32 and random-32 rides and their replays. [pending: secondary design and prediction 3's four replays.]
- P4: the pilot pre-test on draw 1, run before the tag, found R5 passing at 2.0. Before the tag it was decided to keep P4 as written and report it as failed (section 9a, point 4).
- R3.5, R4 and R5 are tested on draw 1, which the pilots used. So P3, P5 and the R3.5 clause of P2 are not tested on a new draw.

### 2.8 Compute

**Hardware.**
- Rides run on one Slurm node with three GPUs (A6000).
- After the node's Debian 13 upgrade on 2026-11-05, CUDA would not initialise. Jobs then ran on the CPU with a C kernel (`brain/lif_kernel.c`).
- CUDA worked again on 2026-11-08.
- A GPU ride takes about 5 h. R0 seed 211 reached 60 generations in 294 min (job 38263).
- GPU runs do not repeat exactly. `index_add_` sums in no fixed order, and CPU and GPU random streams differ. So each run is one sample, quoted with its job id.

**Queue.**
- The cluster's default QoS sets one running job per user (`MaxJobsPU=1`). Slurm does not enforce it.
- The queue had been holding 2 of the 3 GPUs while another user waited. On 2026-11-11 it was rebuilt to run one job at a time, as a relay: `tools/submit_serial.py --next --after 38272`, with `serial-next.sbatch`. Slurm holds one link and one relay at a time.
- Each pass works out what is left from results on disk. A ride stopped by the cap is queued again and resumes.
- The list held 225 links: 128 rides and 97 replays.
- The rides and their order are unchanged, so this is not a deviation from the preregistration.
- It roughly doubles the time left, to about four weeks.

## 3. Results: Track A, riding

Track A asks whether a rewired brain can learn to ride the bike in closed loop. The criterion is the mean riding time over 48 riders in the last generation of a 60-generation cross-entropy search, together with the fraction of riders that ride the full 15 s (preregistration section 5). With no steering, the bike rides 3.5 s at 4.0 m/s and 5.7 s at 4.5 m/s. These hands-off floors come from 16 riders each (`results/gate/v4.*_s201/handsoff_trace.json`). Every ride in this section uses the hand-picked readout, the primary readout of section 5, unless stated otherwise.

### 3.1 Transmission pre-test and riding scale per rung

The pre-test (section 4) holds the bike upright and drives the left or right VS and haltere inputs. A rung passes at a given synapse scale if two things hold on both probes. First, its count of lateralised descending and motor neurons must exceed the null maximum. Second, its network rate must lie between 10,750 and 43,000 spikes/s.

Draw 1 was tested with 30 brains per cell before the tag (jobs 37927–37947; pilot, preregistration section 9):

| Rung | Outcome | Scale used for riding |
|---|---|---|
| R0 real wiring | pass at 0.47 (38 / 39 lateralised outputs, null max 11 / 5) | 0.47 |
| R1 transmitter errors | pass at 0.47 (35 / 31, null max 4 / 13) | 0.47 |
| R2 count jitter | pass at 0.47 (50 / 38, null max 8 / 6) | 0.47 |
| R3 type-preserving | pass at 0.47 (37 / 39, null max 5 / 4) | 0.47 |
| R3.5 strength-preserving | fail at all nine scales run (0.47 to 2.0) | 0.47 (closed loop) |
| R4 degree-preserving | fail at every scale run (0.47 to 1.6) | 1.2 (closed loop, from the pilot) |
| R5 random | pass at 2.0 only (7 / 8 outputs, null max 4 / 4); fail below | 2.0 (closed loop) |

The confirmatory draws 3 to 5 of R1, R2 and R3 were pre-tested at 0.47 with 30 brains after the tag (GPU, job 38261). Eight of the nine draws pass. R2 draw 3 fails on the null alone: its outputs are 21 / 20 against null maxima of 155 / 160. Section 5 says such a draw is ridden anyway, reported, and kept in the medians.

Section 4 sets the riding scale of R3.5 and R5 in closed loop. The scale chosen is the one whose network rate over the first 0.6 s of the reference replay is closest to R0's 23,388 spikes/s (jobs 38363–38368):
- R3.5 rides at 0.47, at 0.89 of R0's rate.
- R5 rides at 2.0, at 1.61 of R0's rate.
- R4 keeps the pilot's 1.2 (1.66–1.68 of R0's rate; job 37944, ride job 37945).

No bisection was needed.

### 3.2 Pilots (before the 9 November tag; not confirmatory)

The pilots used the hand-picked readout at 4.5 m/s. They ran on rewiring draws 1 and 2 with CEM seeds 201 to 203, mostly on the CPU. They do not test any prediction, because their draws and seeds are not the preregistered ones (section 9).

Last-generation riding time (`CURRENT_NUMBERS.md`, "Pilot rides on rewired brains"):

| Rung | Searches (last generation, finishing) | Jobs |
|---|---|---|
| R0 | 13.71 s (77%), 11.89 s (52%), 10.91 s (40%); three-seed mean 12.17 s, SD 1.42 s | 37492, 37494, 38124 |
| R1 | draw 1: 7.01 s (8%) and 12.27 s (56%); draw 2: 11.75 s (40%) | 38038, 38108, 38107 |
| R2 | draw 1: 13.42 s (69%) and 13.46 s (75%); draw 2: 11.96 s (44%) | 38039, 38125, 38135 |
| R3 | draw 1: 11.48 s (42%) and 11.14 s (52%); draw 2: 8.53 s (10%) and 10.89 s (40%) | 37938–38043, 37948–37953, 38134, 38154 |
| R4 at 1.2 | 1.69 s at generation 24, 0% finishing; cancelled after 25 generations | 37945 |

**Stalled searches.** Two of the 13 finished hand-picked-readout searches stalled:
- R1 draw 1, seed 201: 7.01 s.
- R3 draw 2, seed 201: 8.53 s.

Both ended with a lane-filter gain near zero (+0.011 and +0.003). The other eleven ended between −0.087 and −0.194, and rode 10.89 to 13.71 s. On each of these two draws, the other CEM seed used the same brain with a byte-identical lane filter and operating point, and rode 2.4 to 5.3 s longer. For R1 draw 1 the low value belongs to the search, not the draw. For R3 draw 2, this one further seed suggests a second stalled search rather than a worse draw.

Replays without the off-road rule show the same pattern for both stalled decoders. The riders stay upright: 47 of 48 and 48 of 48. Most drift off the road to one side: 35 and 32 riders end more than 3.5 m from the center line. In short, these decoders keep the bike balanced but do not hold the lane.

Every other pilot is within one three-seed SD of R0.

**R4.** R4 did not learn to ride. Its riding time stayed below the hands-off floor, and no rider finished.

### 3.3 Confirmatory rides so far

The confirmatory rides use CEM seed 211 and 60 generations each. The table gives last-generation values (`results/rungs/conf_*/v*_s211/cem.json`; `CURRENT_NUMBERS.md`, "Confirmatory rides so far").

| Rung | Draw | Speed (m/s) | Job | Device | Riding time (s) | Finished |
|---|---|---|---|---|---|---|
| R0 | — | 4.5 | 38263 | GPU | 12.79 | 62% |
| R1 | 3 | 4.5 | 38264 | GPU | 14.65 | 85% |
| R1 | 4 | 4.5 | 38265 | GPU | 13.72 | 71% |
| R1 | 5 | 4.5 | 38266 | GPU | 10.47 | 42% |
| R2 | 3 (failed the pre-test null) | 4.5 | 38267 | GPU | 12.02 | 44% |
| R2 | 4 | 4.5 | 38268 | GPU | 13.05 | 71% |
| R2 | 5 | 4.5 | 38269 | GPU | 13.26 | 71% |
| R3 | 3 | 4.5 | 38270 | GPU | 13.19 | 60% |
| R3 | 4 | 4.5 | 38271 | GPU | 13.37 | 69% |
| R3 | 5 | 4.5 | 38272 | GPU | 13.54 | 75% |
| R0 | — | 4.0 | 38710 | GPU | 12.74 | 60% |
| R1 | 3 | 4.0 | 38714 | GPU | 13.23 | 73% |
| R1 | 4 | 4.0 | 38728 | GPU | 9.35 | 21% |
| R1 | 5 | 4.0 | 38735 | GPU | 11.11 | 29% |
| R3.5 | 1, scale 0.47 | 4.5 | 38371 | CPU | 2.71 | 0% |
| R4 | 1, scale 1.2 | 4.5 | 38372 | CPU | 2.96 | 0% |
| R5 | 1, scale 2.0 | 4.5 | 38373 | CPU | 4.34 | 0% |

**R3.5, R4 and R5.** These rungs had to ride on the CPU because the GPUs were taken. The preregistration allows this, provided the rides are reported as CPU runs. Each of the three single rides ends below the 5.7 s hands-off floor, and none finishes a rider in its last generation. Over the last five generations, R4 rode 2.49 s and R5 rode 4.21 s.

**R1 at 4.0 m/s.**
- Draw 4 (9.35 s) was still climbing at the end of the search: 9.1 s at generation 50 and 9.3 s at generation 59. Its lane-filter weight is −0.07.
- Draw 5 (11.11 s) was also still rising at the end. Its lane-filter weight is −0.03.
- R0's own 4.0 m/s ride ends with a lane weight near zero (+0.01) and still rides 12.74 s. At this speed, therefore, a near-zero lane weight does not mark a stalled search.
- The median over R1's three draws at 4.0 m/s is 11.11 s, against R0's 12.74 s.

At 4.5 m/s, the median over R1's three draws is 13.72 s.

### 3.4 Held-out replays

Each primary run's final mean decoder was replayed with 48 riders for 15 s on the CPU. The replays used unseen gust seeds 301 and 302, and the training speed plus and minus 0.5 m/s. Section 5 makes these replays descriptive. No prediction uses them.

Riding time is in seconds, with riders finished out of 48 in brackets. For rides trained at 4.0 m/s, the "+0.5" column is 4.5 m/s and the "−0.5" column is 3.5 m/s.

| Ride | Job | gust301 | gust302 | +0.5 m/s | −0.5 m/s |
|---|---|---|---|---|---|
| R0, 4.5 m/s | 38413, 38436 | 14.05 (38) | 14.80 (46) | 13.10 (28) | 7.77 (0) |
| R1 draw 3, 4.5 m/s | 38437 | 14.75 (44) | 15.00 (48) | 14.61 (42) | 12.71 (24) |
| R1 draw 4, 4.5 m/s | 38438 | 14.89 (46) | 14.84 (47) | 14.45 (42) | 11.43 (10) |
| R1 draw 5, 4.5 m/s | 38442 | 13.56 (36) | 13.87 (41) | 10.10 (17) | 7.85 (0) |
| R2 draw 3, 4.5 m/s | 38445 | 11.92 (26) | 11.99 (24) | 12.13 (27) | 8.89 (4) |
| R2 draw 4, 4.5 m/s | 38455 | 15.00 (48) | 14.63 (44) | 14.32 (42) | 12.31 (18) |
| R2 draw 5, 4.5 m/s | 38456 | 14.21 (41) | 14.46 (42) | 11.08 (19) | 8.76 (4) |
| R3 draw 3, 4.5 m/s | 38691 | 14.07 (33) | 14.15 (34) | 10.99 (15) | 10.50 (9) |
| R3 draw 4, 4.5 m/s | 38706 | 13.87 (34) | 13.05 (30) | 11.42 (17) | 7.19 (0) |
| R3 draw 5, 4.5 m/s | 38708 | 14.54 (43) | 14.40 (39) | 9.35 (14) | 11.52 (10) |
| R0, 4.0 m/s | 38712 | 14.21 (40) | 14.73 (44) | 12.78 (32) | 9.27 (4) |
| R1 draw 3, 4.0 m/s | 38726 | 14.88 (47) | 14.42 (42) | 14.52 (42) | 9.31 (4) |
| R1 draw 4, 4.0 m/s | 38731 | 10.89 (15) | 10.54 (12) | 9.18 (7) | 7.79 (0) |
| R1 draw 5, 4.0 m/s | 38743 | 12.74 (32) | 12.55 (30) | 7.06 (3) | 7.37 (2) |

What the replays show:
- **Unseen gusts cost little** for most decoders.
- **Slowing down costs the most.**
  - At 4.0 m/s, R0's 4.5 m/s decoder finishes no rider, and 35 of 48 fall.
  - At the same speed, the falls out of 48 are 26, 29 and 32 for R2's draws, 10, 12 and 23 for R3's, and 14, 1 and 15 for R1's.
  - R1 and R3 lose more riders off the road there (R1: 10, 37, 33; R3: 29, 36, 15) than R0 (13) and R2 (18, 1, 12).
- **The weakest 4.0 m/s decoders lose the lane when sped up.** R1 draw 4 (job 38731) has 41 of 48 riders leave the road at 4.5 m/s, and R1 draw 5 (job 38743) has 45. Neither has a rider fall.
- **R0's 4.0 m/s decoder** loses most riders to falls at 3.5 m/s (28 fall), as R0's 4.5 m/s decoder does at 4.0 m/s.

Section 5 gives held-out tests to the primary runs only. R3.5, R4 and R5 therefore get none.

### 3.5 What can and cannot be concluded yet

**No preregistered Track A prediction has been tested.** So far each rung has at most one CEM seed (211) per speed. R0 and R1 have it at both speeds, R2 and R3 only at 4.5 m/s, and R3.5, R4 and R5 have their single 4.5 m/s ride.

- **Prediction 1 (R1 and R2 within one seed-SD of R0).** This needs the SD of R0's five last-generation means at each speed. R0 has one confirmatory seed per speed, so the SD does not exist yet.
  - R1's three draws at 4.5 m/s (median 13.72 s) ride above R0's first seed (12.79 s). This says nothing yet.
  - The pilots' three-seed R0 SD (1.42 s) does not substitute for the confirmatory SD.
  - [pending: R0 CEM seeds 212–215 at both speeds; R1 and R2 seeds 212–215 on draws 3–5 at both speeds; R2 at 4.0 m/s]
- **Prediction 2, R3 clause (R3 loses under 30% of R0's riding time at each speed).** R3's three draws at 4.5 m/s (13.19, 13.37 and 13.54 s) all ride above R0's first seed. This tests nothing until R0 has five seeds. [pending: R0's five seeds; R3 seeds 212–215; R3 at 4.0 m/s]
- **Prediction 2, transition clause (R3.5's one ride below 70% of R0's primary outcome at 4.5 m/s).** R3.5's ride (2.71 s) is 21% of R0's first ride. The test compares it with R0's median over five seeds, which does not exist yet. [pending: R0's median over five seeds at 4.5 m/s]
- **Prediction 5 (does R4 at its own calibration ride as well as R0?).** R4's single ride is 2.96 s, or 23% of R0's first ride (2.49 s over its last five generations). The ledger states the condition's status as follows: unless R0's five seeds come out very differently, R4 does not ride as well as R0, and prediction 5's condition is not met. The formal decision uses R0's primary outcome minus one seed-SD. [pending: R0's five seeds at 4.5 m/s; R4's top-32 plus lane ride, reported next to it]
- **Below the hands-off floor.** R3.5 (2.71 s), R4 (2.96 s) and R5 (4.34 s) all ride below the 5.7 s floor at 4.5 m/s. With the hand-picked readout, a searched decoder on these brains does worse than no steering. The list of cells this readout reads was chosen on R0. So on its own, this result does not show that these rungs carry no usable signal (section 5). The secondary readout is there for that question. [pending: secondary design, after the primary design]
- **Prediction 3 (R4 against random-32 on R0).** This uses the secondary readout. None of its rides has run yet. [pending: R4 top-32 plus lane, and R0 random-32 plus lane with `READOUT_SEED` 0–2]
- **Bootstrap CIs and generations-to-half-of-R0.** These need the full set of seeds. [pending: primary design complete]

The rides run one at a time as a relay queue (`tools/submit_serial.py --next`), with about four weeks of queue left as of 2026-11-12. Section 10 of the preregistration records no deviations.

## 4. Results: Tracks B and C

This section reports the decoder-free predictions (Track B) and decodability (Track C). Track B has a confirmatory run, done after the `prereg-v1` tag of 9 November. Track C has only a pilot, run on 8 November, before the tag. Neither track carries a numbered prediction in preregistration section 8. Section 4.3 sets out which predictions these results touch.

### 4.1 Track B: confirmatory scores

**Design.** The scored items are the six scored rows of `docs/track_b_predictions.csv`: sugar to MN9, bitter suppression, Ir94e suppression, dose response, loom to the giant fiber, and loom to DNp02/DNp11. Two further rows are controls and are reported only. Taste groups are driven on both sides.

A row passes on a brain if two things hold:
- its difference has the expected sign;
- the difference is at least half as large as on the real wiring at scale 0.47.

A rung's score is the fraction of scored rows passed, averaged over its draws (preregistration section 6). The preregistration fixes the number of draws but not which ones. They were picked before any run, so that no Track B pilot had used them:
- R1 and R2: draws 101 to 200.
- R3, R3.5, R4 and R5: draws 3 to 5.

Every rung was scored at 0.47. R4 and R5 were also scored at their closed-loop scales of 1.2 and 2.0. R3.5's closed-loop scale is 0.47, so it has one score.

**Runs.**
- R0 reference: job 38414. It came out identical to the pilot's `final/r0.json`.
- Test run on draw 101 of R1 and of R2: job 38415.
- Remaining runs: jobs 38416 to 38429, from 2026-11-10 01:33 to 13:52. All completed, covering 218 brains with no failed draw.
- Sources: `results/track_b/confirmatory/scores.json`, scored with `tools/track_b_score.py --by-rung`.

| Rung | Scale | Draws | Mean score | Draws by score |
|---|---|---|---|---|
| R0 | 0.47 | 1 | 1.000 | |
| R1 | 0.47 | 100 | 0.682 | 31 at 1.0, 27 at 0.83, 2 at 0.67, 40 at 0.33 |
| R2 | 0.47 | 100 | 0.993 | 96 at 1.0, 4 at 0.83 |
| R3 | 0.47 | 3 | 1.000 | |
| R3.5 | 0.47 | 3 | 0.000 | |
| R4 | 0.47 / 1.2 | 3 / 3 | 0.000 / 0.000 | |
| R5 | 0.47 / 2.0 | 3 / 3 | 0.000 / 0.056 | one draw at 2.0 (draw 4, 0.17) passes loom to DNp02/DNp11 |

The ladder therefore has three tiers:
- R0, R2 and R3 score at or near full.
- R1 is in between.
- Every rung from R3.5 up scores at or near zero.

**The R1 split.** R1's scores are bimodal, and the mean of 0.682 sits between the two modes:
- 58 of 100 draws score 0.83 or 1.0.
- 40 draws score 0.33, which means they pass the two loom rows only.
- 2 draws score 0.67.

R1 loses only taste rows. Both loom rows pass on all 100 draws, with medians of 255 and 174 Hz against R0's 264 and 183 Hz.

The four taste rows mostly keep their sign but fall below half of R0. The R1 medians are 18, -17, -16 and 2.4 Hz, against R0's 30, -30, -30 and 7.4 Hz.

Of the 191 failed R1 rows, 13 are sign flips; the rest keep their sign but fall short of half of R0. When one taste row fails, the others usually fail with it.

The 191 failed rows by row (`scores.json`):

| Row | Failed draws |
|---|---|
| Dose response | 63 |
| Ir94e suppression | 45 |
| Bitter suppression | 43 |
| Sugar to MN9 | 40 |

**R2.** R2 loses only the dose-response row. It fails on 4 draws, by size, not by sign.

**R3.5, R4 and R5.** The taste rows give exactly 0 Hz difference: no response reaches MN9 or the suppression readouts. They therefore fail by sign. The loom rows keep at most a fraction of R0's difference.

The closed-loop scales (R4 at 1.2, R5 at 2.0) do not bring the rows back. The single nonzero entry is R5 draw 4 at 2.0, which passes loom to DNp02/DNp11 and scores 0.17.

**Caveats.** Several choices were made after the Track B pilot had been seen (preregistration sections 6 and 9a, point 10), so this part of Track B is not blind:
- the half-of-R0 criterion;
- the choice of rows;
- the two-sided taste drive;
- dropping the two rows that failed on the real wiring (water to MN9, JO-F to MDN).

**Pilots before the tag, for context only.** The first Track B pilot (jobs 38186 and 38187) used five signed rows of the draft CSV and right-side taste drive only. On it, R0 and every R1 to R3 draw scored 0.6, and R3.5, R4 and R5 scored 0. Driving the left side instead (job 38189), sugar drove MN9 at 0.13 Hz on R0, against 22.48 Hz from the right.

### 4.2 Track C: pilot decodability (R0 to R3 only)

**Status.** Everything in this subsection is a pilot from before the tag. No confirmatory Track C run exists.

**Data.**
- One replay per brain of a final CEM mean decoder: hand-picked readout, draw 1, 48 riders × 15 s, seed 201, no off-road rule.
- Jobs 38178 to 38181. R1 uses the seed-202 decoder, because the seed-201 search stalled.
- Spike counts of all 1,314 descending neurons and 67 wing motor neurons, in 100 ms bins.

**Analysis.**
- Ridge regression to roll rate (job 38185, `tools/track_c.py`, `results/track_c/<rung>.json`).
- 7,200 samples per brain, five folds over riders. R² is pooled out of fold.
- N90 is the number of neurons needed to reach 90% of a reference R². Neurons are added either in the brain's own screen order or in 20 random orders.
- Random orders are drawn over all of a site's neurons, silent ones included.

**Descending site.**

| Brain | Active neurons | R² of the site | Target R² | N90, screen order | N90, random: median (25–75%) | Random, active only: median |
|---|---|---|---|---|---|---|
| R0 | 393 of 1,314 | 0.962 | 0.866 | 3 | 277 (188–355) | 73 |
| R1 | 350 | 0.927 | 0.834 | 3 | 454 (345–574) | 100.5 |
| R2 | 408 | 0.964 | 0.867 | 3 | 249.5 (144–345) | 57.5 |
| R3 | 371 | 0.958 | 0.863 | 3 | 297 (188–385) | 80 |

**Wing-motor site, against its own R².** This is the reference chosen on 2026-11-09 (preregistration 9a, point 9).

| Brain | Active neurons | R² of the site | Target R² | N90, screen order | N90, random: median (25–75%) | Random, active only: median |
|---|---|---|---|---|---|---|
| R0 | 33 of 67 | 0.909 | 0.818 | 4 | 29.5 (24–34) | 14 |
| R1 | 31 | 0.903 | 0.812 | 4 | 37 (25–43) | 14 |
| R2 | 35 | 0.905 | 0.814 | 3 | 31 (24–35) | 13.5 |
| R3 | 40 | 0.867 | 0.780 | 6 | 35.5 (30–42) | 17.5 |

**Wing-motor site, against the descending R².** This reference is shown for comparison only. Screened N90 is 7, 4, 7 and 29 on R0 to R3. R3's wing-motor site reaches 0.867 against a target of 0.863, so its 29 sits at the edge of what that site can reach.

**What the pilot shows.**
- Screened neurons are far cheaper than random ones at the descending site. N90 is 3 in screen order on all four brains, against random-order medians of 249.5 to 454.
- With these data, N90 does not separate R0 to R3.
- The roll-rate SD differs between the replays: 0.42, 0.27, 0.43 and 0.40 on R0 to R3. Each brain rides under its own decoder.

**Limits.**
- One replay seed and one rewiring draw per brain.
- Closed loop: a neuron can predict roll rate because it follows the haltere input, or because the decoder reads it and steers.
- The ridge penalty is chosen once per site.
- One replay per brain cannot say whether R3's difference at the wing-motor site is real.

**Not yet measured on R3.5 to R5.** The pilot needs a decoder to replay. When it ran, no rung past R3 had one: R3.5 and R5 had not been ridden, and the R4 pilot did not learn.

Each of these rungs now has one confirmatory ride. None finishes a rider in its last generation.

| Rung | Job | Scale | Riding time (s) |
|---|---|---|---|
| R3.5 | 38371 | 0.47 | 2.71 |
| R4 | 38372 | 1.2 | 2.96 |
| R5 | 38373 | 2.0 | 4.34 |

[pending: Track C on these rides, and confirmatory Track C on all rungs]

[pending: the simulated jGCaMP8 dF/F (30 and 10 Hz) and probe-distance (10, 25, 50 µm) parts of preregistration section 7; neither has been run]

### 4.3 Which predictions these results bear on

**No prediction is tested by Track B or Track C.** The preregistration states no numerical Track B prediction. Section 4.1 is reported as the decoder-free result of section 6. Track C likewise has no numbered prediction, and its data so far are pilot only.

**Prediction 2 (transition between R3 and R3.5).** Track B falls at the same place: R3 scores 1.000 and R3.5 scores 0.000. Prediction 2 is stated on riding time, though. Its R3.5 clause waits on R0's median over five seeds.

R3.5's single ride (2.71 s) is 21% of R0's first ride. [pending: R0 CEM seeds 212 to 215 at 4.5 m/s, for R0's primary outcome]

**Prediction 5 (Track B as headline).** This prediction makes Track B the headline result only if R4's single ride rides as well as R0, meaning at or above R0's primary outcome minus one seed-SD. R4 rode 2.96 s, 23% of R0's first ride (12.79 s, job 38263).

So unless R0's five seeds come out very differently, the condition is not met. The decision waits on R0's five-seed median and seed-SD. [pending: R0 CEM seeds 212 to 215 at 4.5 m/s]

**Prediction 4 (R5 fails the pre-test at every scale).** This prediction concerns the transmission pre-test, not Track B. R5's Track B score at its closed-loop scale (0.056) is reported next to it and does not decide it.

**Predictions 1 and 3.** Neither uses Track B or Track C.

## 5. Status, deviations and limitations

### 5.1 Milestones

| Milestone | Date | Status on 2026-11-12 |
|---|---|---|
| M2: interim three-row figure (riding, decoder-free predictions, decodability; R0 to R5 on a shared axis) | 13 Nov 2026 | Done. First version 2026-11-11, after three independent reviews. It is built by `tools/interim_figure.py` and written to `site/figures/interim.{svg,png,json}`, with data up to 2026-11-11. |
| All runs done (semester plan) | 20 Nov 2026 | Not met: 14 of 100 primary rides done on 2026-11-12, about four weeks of queue left. |
| M3: semester report (figure, methods, a ledger of every job, all code and decoders released) | 4 Dec 2026 | [pending: the rides will not all be finished by this date if the queue runs at its estimated length] |
| Confirmatory and secondary rides | Jun 2027 | In progress: 14 of 100 primary rides done; about four weeks of queue left on 2026-11-11 (section 5.3). |

The interim figure has three rows:

- **Row A:** the last-generation riding time of every finished hand-picked-readout search at 4.5 m/s. These are the 60-generation searches, plus R0's three gate pilots, which stopped at 58, 57 and 60 generations. Confirmatory rides are shown filled and pilots open.
- **Row B:** the Track B confirmatory score for each draw.
- **Row C:** the Track C pilot N90 at the descending site, for R0 to R3 only. R3.5 to R5 have not been measured, because the pilot ran before those rungs were ridden.

### 5.2 What is done and what is pending

**Track A, primary design (100 rides).** 14 of the 100 rides are done, all on CEM seed 211 (`results/rungs/conf_*/v*_s211/cem.json`):

- 4.5 m/s: R0, plus draws 3, 4 and 5 of each of R1, R2 and R3 (jobs 38263 to 38272).
- 4.0 m/s: R0 and R1 draws 3 to 5 (jobs 38710, 38714, 38728, 38735).

Held-out replays have finished for each of these rides.

The 9 confirmatory draws took the 30-brain pre-test at scale 0.47 (job 38261). R2 draw 3 fails it, on the null only. As section 5 of the preregistration requires, it was ridden anyway, it is reported, and it enters the medians.

**Track A, single rides at each rung's closed-loop scale.** All three are done, on the CPU, on draw 1 with CEM seed 211 at 4.5 m/s:

| Rung | Job | Riding time (s) | Finished |
|---|---|---|---|
| R3.5 at scale 0.47 | 38371 | 2.71 | 0% |
| R4 at scale 1.2 | 38372 | 2.96 | 0% |
| R5 at scale 2.0 | 38373 | 4.34 | 0% |

**Track A, secondary design.** The queue holds 38 secondary rides and prediction 3's four replays. None of them has run. [pending: secondary rides and prediction 3 replays]

**Track B.** Done: R0's reference (job 38414), a one-draw test (job 38415) and the remaining runs, jobs 38416 to 38429 (218 brains, no failed draw). `results/track_b/confirmatory/scores.json` holds 219 brains: R0's reference and 218 rewired brains. The preregistration gives no numerical Track B prediction, so this result does not test anything.

**Track C.** Only the pilot on R0 to R3 exists (`results/track_c/r0..r3.json`). [pending: confirmatory Track C decodability runs]

**Predictions.** None of the preregistered predictions has been tested yet:

- **Prediction 1** compares R1's and R2's medians (15 runs each: 3 draws x 5 CEM seeds) with R0's median over five seeds, against the SD of R0's five seed means. **Prediction 2** asks whether 1 - median(R3)/median(R0) < 0.30. At 4.5 m/s only CEM seed 211 exists for each rung and draw. At 4.0 m/s only R0 and R1 draws 3 to 5 have run, and R2 and R3 have not. Both predictions wait for seeds 212 to 215 and for the remaining 4.0 m/s rides.
- **Prediction 2, transition clause:** R3.5's single ride is 21% of R0's first ride. The test waits for R0's median.
- **Prediction 5:** R4's single ride is 23% of R0's first ride. The ledger says that unless R0's five seeds come out very differently, prediction 5's condition is not met. That is not final until R0 has all five seeds.
- **Prediction 3** waits for the secondary design.
- **Prediction 4** (R5 fails the pre-test at every scale) is contradicted by the pre-tag pre-test, where R5 passes at 2.0, weakly. Section 9a, point 4 of the preregistration keeps the prediction as written and reports it as failed. That evidence is pilot data from before the tag.

### 5.3 Remaining queue

On 2026-11-11 all remaining work was put into one chain, then run as a relay (`tools/submit_serial.py --next --after 38272`). Slurm holds one link and one relay job at a time. When it was set up, the chain had 225 links: 128 rides and 97 held-out replays, ordered as follows:

1. the held-out replays of R3 draws 3 to 5;
2. each remaining primary ride, followed by its held-out replays;
3. the 38 secondary rides;
4. prediction 3's four replays.

The ledger estimated about four weeks at that point, at about 5 h per ride and 30 min per replay. The first link was job 38691. A ride stopped by the 340 min cap is queued again and resumes. A link submitted three times is skipped and named in the relay's log.

### 5.4 Deviations from the preregistration

Section 10 of the preregistration lists no deviations ("(none yet)").

The move to one job at a time on 2026-11-11 is not a deviation. The cluster QoS sets one running job per user (`MaxJobsPU=1`). Slurm does not enforce that limit, but the queue had been holding 2 of the node's 3 GPUs while another user waited. The rides and their order did not change. The only effect is that the time left roughly doubled.

The preregistration left three details open. They were filled in as follows:

- **Track B draws.** The preregistration gives the number of draws but not which ones. They were picked before any run so that no Track B pilot had used them: R1 and R2 use draws 101 to 200; R3, R3.5, R4 and R5 use draws 3 to 5.
- **Held-out speed conditions.** Section 5 gives gust seeds only for the gust test. The speed conditions reuse replay seed 301.
- **Single rides on the CPU.** The three single rides ran on the CPU because the GPUs were taken. Section 5 allows this, and they are reported as CPU runs.

### 5.5 Limitations

- **One CEM seed so far.** Every confirmatory ride uses CEM seed 211. Seeds 212 to 215 have not run. The 4.0 m/s rides exist only for R0 and R1 draws 3 to 5. Single-seed numbers vary a lot: on R1 at 4.0 m/s, draw 4 rode 9.35 s and draw 3 rode 13.23 s. In the pilots, 2 of 13 searches stalled.
- **GPU nondeterminism.** The engine adds synaptic input with `index_add_` (`brain/engine.py:134`). On a GPU these additions happen in no fixed order, so two runs with the same seed drift apart. Jobs 36543 and 36555 ran the same search with the same seed. Both ended with 35 of 48 riders finishing, but with 885 and 836 finished attempts overall. A CPU run does not reproduce a GPU run either, because the random streams differ by device. The R3.5, R4 and R5 single rides ran on the CPU, the primary rides on the GPU. Each run is one sample and is quoted with its job id.
- **Pilot and confirmatory.** Runs before the `prereg-v1` tag (2026-11-09) are pilots. They used rewiring draws 1 and 2 and CEM seeds 201 to 203 (203 on R0 only), mostly on the CPU. Confirmatory rides use draws 3 to 5 and seeds 211 to 215.
  - The riding predictions were informed by the pilots, so they are not blind.
  - R3.5, R4 and R5 ride draw 1, which the pilots used. For R4 this includes a pilot ride with the primary readout. Predictions 3 and 5, and the R3.5 clause of prediction 2, are therefore not tested on a new draw.
  - In Track B, the half-of-R0 criterion, the choice of rows and the bilateral drive were set after the pilot.
- **Readout chosen on R0.** The primary readout (42 cell types, 112 neurons on R0, plus the lane channel) was chosen on the real wiring, after the pilots, so it favours R0. A rung that loses riding time is not, by itself, evidence that the rung carries no usable signal.
- **Top-32 readout is a floor.** On R0's pilot, the secondary top-32 readout with the lane channel did not hold the lane. Its results are read only as a floor on what a screened readout carries.

## 6. Data and code availability

| Item | Location |
|---|---|
| Project repository (preregistration, Track B prediction table, figure scripts, site) | github.com/victory-c/scrambled-brains |
| Simulator, rung generators, ride and replay pipeline, results and ledger (`docs/CURRENT_NUMBERS.md`, `JOBS.md`) | github.com/victory-c/fly-brain |
| Project site and interim figure | victory-c.github.io/scrambled-brains |
| Preregistration | `docs/PREREGISTRATION.md` in victory-c/scrambled-brains, fixed by git tag `prereg-v1` (2026-11-09) |
| Track B predictions | `docs/track_b_predictions.csv` in victory-c/scrambled-brains |
| Interim figure values with source files | `site/figures/interim.json` in victory-c/scrambled-brains |
| Archived release (code, decoders, traces, job ledger) | Zenodo [pending: release with the semester report] |

The simulator implements the Shiu et al. 2024 leaky integrate-and-fire model and matches Brian2 spike for spike (`tests/test_brian2.py`). It runs on the male CNS v1.0 connectome (Janelia FlyEM, Cambridge, Google; CC BY 4.0).

Each Track A search writes its results to `results/rungs/<tag>/v<speed>_s<seed>/cem.json`, and its held-out replays go under `heldout/`. Track B results are in `results/track_b/confirmatory/` and the Track C pilot in `results/track_c/`.
