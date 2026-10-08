<div align="center">

# 🧪 article-labs

**Small, runnable apps behind my LinkedIn articles.**<br>
One folder per article. Each one runs with a single command and is tested on every push.

[![labs](https://github.com/atonyhonesto/article-labs/actions/workflows/labs.yml/badge.svg)](https://github.com/atonyhonesto/article-labs/actions/workflows/labs.yml)
![Labs](https://img.shields.io/badge/labs-14-6f42c1?style=flat-square)
[![Articles](https://img.shields.io/badge/articles-tech--articles-0A66C2?style=flat-square)](https://github.com/atonyhonesto/tech-articles)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Tony_Honesto-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/tony-honesto-4195023)

</div>

---

## How the labs work

- **One idea per lab.** Each lab takes the core idea of one article and turns it into the smallest program that shows it working, usually with synthetic data so it runs anywhere.
- **Runs locally in one step.** Every lab has a `ci.sh` that installs what it needs, runs the tests and runs the demo. Most need only Python 3.10+ and no extra packages.
- **Honest about scope.** These are teaching-sized apps, not production systems. Each README says what's simulated and what a real deployment would swap in.
- **Tested in CI.** GitHub Actions discovers every `labs/*/lab.json` and runs each lab as its own job, so one red lab never hides behind another.

```bash
git clone https://github.com/atonyhonesto/article-labs.git
cd article-labs
bash labs/kafka-consumer-groups/ci.sh     # any lab, same pattern
```

Bigger companion projects live in their own repos: [race-speed-inference](https://github.com/atonyhonesto/race-speed-inference) · [ai-coding-tax-analyzer](https://github.com/atonyhonesto/ai-coding-tax-analyzer) · [edi-x12-mapper](https://github.com/atonyhonesto/edi-x12-mapper) · [signalr-vs-sse-dotnet10](https://github.com/atonyhonesto/signalr-vs-sse-dotnet10) · [csharp-fargate-stepfunctions](https://github.com/atonyhonesto/csharp-fargate-stepfunctions) · [race-data-redis-streams](https://github.com/atonyhonesto/race-data-redis-streams) · [oauth2-pkce-jwt-walkthrough](https://github.com/atonyhonesto/oauth2-pkce-jwt-walkthrough) · [nodejs-architecture-patterns](https://github.com/atonyhonesto/nodejs-architecture-patterns) · [watch-session-tracker](https://github.com/atonyhonesto/watch-session-tracker-lightweight) · [ParquetMCPServer](https://github.com/atonyhonesto/ParquetMCPServer)

## The labs

<!-- INDEX:START -->
**14 labs.** Each folder runs on its own and is tested on every push.

### 🏎️ Motorsports & Sports Technology

| Lab | What it shows | Stack | Article |
|---|---|---|---|
| [`anti-dive-geometry`](labs/anti-dive-geometry) | Computes front anti-dive percentage from suspension pickup points and shows how geometry changes pitch under braking | Python · NumPy | [Anti-Dive & Downwash Geometry in F1](https://www.linkedin.com/pulse/anti-dive-downwash-geometry-f1-tony-honesto-b5xlc/) · [Helmut Schmidt University - Vehicle Dynamics Certificate](https://www.linkedin.com/pulse/helmut-schmidt-university-vehicle-dynamics-tony-honesto-lanoc/) |
| [`athlete-evaluation-pipeline`](labs/athlete-evaluation-pipeline) | An end-to-end scikit-learn pipeline (impute, scale, encode, model) scoring athlete prospects with leakage-safe CV | Python · scikit-learn | [ML Pipelines for Athlete Evaluation](https://www.linkedin.com/pulse/ml-pipelines-athlete-evaluation-tony-honesto-q1vsc/) |
| [`dynamic-ticket-pricing`](labs/dynamic-ticket-pricing) | Fits a price-demand curve per section and picks revenue-maximising prices inside floor and ceiling guardrails | Python · NumPy | [ML Pipelines Powering Dynamic Ticket Pricing](https://www.linkedin.com/pulse/ml-pipelines-powering-dynamic-ticket-pricing-tony-honesto-8kcrc/) |
| [`ers-energy-budget`](labs/ers-energy-budget) | Simulates a lap's battery state of charge with and without MGU-H recovery to show what the 2026 rules change | Python · stdlib | [MGU-H Removed from F1 Power Units in 2026](https://www.linkedin.com/pulse/mgu-h-removed-from-f1-power-units-2026-tony-honesto-oahtc/) |
| [`fuel-burn-bar`](labs/fuel-burn-bar) | Rebuilds a broadcast 'burn bar': live fuel use per lap versus the target needed to reach the finish | Python · stdlib | [Amazon Prime Video: Burn Bar, Tech behind the display](https://www.linkedin.com/pulse/amazon-prime-video-burn-bar-tech-behind-display-tony-honesto-p6mgc/) · [Prime Vision + Next Gen Stats](https://www.linkedin.com/pulse/prime-vision-next-gen-stats-tony-honesto-7yt8c/) |
| [`lambda-race-events`](labs/lambda-race-events) | Event-driven Lambda handlers for timing-loop and file-landed events, with idempotency and partial-batch failure | Python · AWS Lambda pattern | [AWS Lambda](https://www.linkedin.com/pulse/aws-lambda-tony-honesto-5risc/) |
| [`lap-time-model-comparison`](labs/lap-time-model-comparison) | Linear, random forest and gradient boosting models compared on lap-time prediction with grouped cross-validation | Python · scikit-learn | [Machine Learning Approaches for Motorsports Competitive Advantage](https://www.linkedin.com/pulse/machine-learning-approaches-motorsports-competitive-tony-honesto-agstc/) |
| [`pit-strategy-monte-carlo`](labs/pit-strategy-monte-carlo) | Monte Carlo of one-stop vs two-stop strategies under random cautions, reporting expected finish and risk | Python · NumPy | [Winning in NASCAR with AI/ML](https://www.linkedin.com/pulse/winning-nascar-aiml-tony-honesto-tkdvc/) · [Motorsports competitive edge via AI use cases](https://www.linkedin.com/pulse/motorsports-competitive-edge-via-ai-use-cases-tony-honesto-d2j3c/) |
| [`rfid-player-tracking`](labs/rfid-player-tracking) | Turns 10 Hz RFID location pings into distance, top speed, sprints and acceleration per player | Python · NumPy | [Zebra Technologies MotionWorks RFID](https://www.linkedin.com/pulse/zebra-technologies-motionworks-rfid-tony-honesto-pa5mc/) |
| [`s3-telemetry-lake`](labs/s3-telemetry-lake) | Partitioned telemetry key layout, prefix queries and a per-team sync that only copies each team its own car | Python · Amazon S3 pattern | [Amazon S3](https://www.linkedin.com/pulse/amazon-s3-tony-honesto-o8hmc/) |
| [`stint-pace-analyzer`](labs/stint-pace-analyzer) | Splits laps into stints, removes in/out laps and fuel effect, and compares drivers on corrected pace | Python · pandas | [F1 Lap Time Analyzer — Python, Streamlit & FastF1 in Action](https://www.linkedin.com/pulse/f1-lap-time-analyzer-python-streamlit-fastf1-action-tony-honesto-qlmgc/) · [ATLAS Data-Driven Race Strategy](https://www.linkedin.com/pulse/atlas-data-driven-race-strategy-tony-honesto-5s2gc/) |
| [`streaming-telemetry-windows`](labs/streaming-telemetry-windows) | Tumbling-window aggregation over an out-of-order telemetry stream, with watermarks and late-event handling | Python · stdlib | [Motorsports - Streaming Telemetry & Real-Time Performance](https://www.linkedin.com/pulse/motorsports-streaming-telemetry-real-time-tony-honesto-rfexc/) |
| [`tire-deg-pit-window`](labs/tire-deg-pit-window) | Learns tire fall-off from lap data and recommends the pit lap that minimises race time | Python · scikit-learn · pandas | [Python Machine Learning in Motorsports](https://www.linkedin.com/pulse/python-machine-learning-motorsports-tony-honesto-aqmmc/) |
| [`var-offside-homography`](labs/var-offside-homography) | Uses a pitch homography to draw a true offside line in camera space and decide offside in pitch metres | Python · OpenCV · NumPy | [VAR Graphics in FIFA](https://www.linkedin.com/pulse/var-graphics-fifa-tony-honesto-yo01c/) |

<!-- INDEX:END -->

## Layout of a lab

```text
labs/<lab>/
  lab.json        title, article link, theme, stack, runtime (drives CI and this index)
  README.md       what it shows, how to run it, sample output, what's simulated
  ci.sh           install → test → demo, the same command locally and in CI
  ...             source, tests, demo
```

---

<sub>Built by <b>Tony Honesto</b> · Cloud & Integration Engineer · <a href="https://github.com/atonyhonesto">GitHub</a> · <a href="https://www.linkedin.com/in/tony-honesto-4195023">LinkedIn</a> · MIT licensed</sub>
