<div align="center">

# 🧪 article-labs

**Small, runnable apps behind my LinkedIn articles.**<br>
One folder per article. Each one runs with a single command and is tested on every push.

[![labs](https://github.com/atonyhonesto/article-labs/actions/workflows/labs.yml/badge.svg)](https://github.com/atonyhonesto/article-labs/actions/workflows/labs.yml)
![Labs](https://img.shields.io/badge/labs-50-6f42c1?style=flat-square)
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
**50 labs.** Each folder runs on its own and is tested on every push.

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

### 🤖 AI, Machine Learning & Agents

| Lab | What it shows | Stack | Article |
|---|---|---|---|
| [`agent-tool-loop`](labs/agent-tool-loop) | An agent loop with typed tools, a step budget and an audit trail, producing a stock analysis report from offline data | Python · stdlib | [Use Case: Agentic Workflow to Build a Stock Analysis & Reporting Agent](https://www.linkedin.com/pulse/use-case-agentic-workflow-build-stock-analysis-agent-tony-honesto-qetxc/) · [ChatGPT Agents as "Research and Execution Assistants"](https://www.linkedin.com/pulse/chatgpt-agents-research-execution-assistants-tony-honesto-pc5yc/) |
| [`ai-eval-harness`](labs/ai-eval-harness) | Why AI projects stall: an evaluation harness with a baseline, acceptance criteria and a go/no-go report | Python · stdlib | [Why Most AI Projects Don't Deliver](https://www.linkedin.com/pulse/why-most-ai-projects-dont-deliver-tony-honesto-yuhac/) |
| [`causal-inference-basics`](labs/causal-inference-basics) | Shows a confounded naive estimate, then recovers the true effect with regression adjustment and inverse propensity weighting | Python · NumPy · scikit-learn | [Statistics: Causal Inference](https://www.linkedin.com/pulse/statistics-causal-inference-tony-honesto-6bkyc/) |
| [`chat-webhook-bot`](labs/chat-webhook-bot) | Slack and Webex webhook receivers with signature verification, replay protection and a pluggable LLM reply | Python · Flask | [ChatGPT + Slack](https://www.linkedin.com/pulse/chatgpt-slack-tony-honesto-jcmjc/) · [ChatGPT + Webex Webhooks](https://www.linkedin.com/pulse/chatgpt-webex-webhooks-tony-honesto-uh5tc/) |
| [`gradient-boosting-forecast`](labs/gradient-boosting-forecast) | Gradient-boosted demand forecasting with lag features, time-based backtesting and a naive-baseline comparison | Python · scikit-learn · XGBoost-compatible | [Forecasting with XGBoost](https://www.linkedin.com/pulse/forecasting-xgboost-tony-honesto-pdwmc/) |
| [`intent-classifier`](labs/intent-classifier) | A conversational-ML intent classifier with slot extraction and a confidence threshold that hands off to a human | Python · scikit-learn | [Conversational ML](https://www.linkedin.com/pulse/conversational-ml-tony-honesto-rsycc/) · [The Cosmopolitan's AI Rose SMS Chatbot](https://www.linkedin.com/pulse/cosmopolitans-ai-rose-sms-chatbot-tony-honesto-rxmec/) |
| [`llm-provider-adapter`](labs/llm-provider-adapter) | One interface over Bedrock, Gemini and OpenAI-style APIs with retries, fallback and token cost accounting | Python · stdlib | [Amazon Bedrock](https://www.linkedin.com/pulse/amazon-bedrock-tony-honesto-gxmpc/) · [LLM: Gemini](https://www.linkedin.com/pulse/llm-gemini-tony-honesto-nytwc/) · [ChatGPT + Python](https://www.linkedin.com/pulse/chatgpt-python-tony-honesto-bjsac/) |
| [`mcp-server-stdio`](labs/mcp-server-stdio) | A dependency-free Model Context Protocol server over stdio with race-data tools, plus a test client that speaks the protocol | Python · MCP · JSON-RPC | [Claude Code MCPs](https://www.linkedin.com/pulse/claude-code-mcps-tony-honesto-v3loc/) |
| [`opencv-motion-insight`](labs/opencv-motion-insight) | Real-time motion detection with background subtraction, contour tracking and a per-frame latency budget | Python · OpenCV | [Real-Time Video Processing with OpenCV (Python)](https://www.linkedin.com/pulse/real-time-video-processing-opencv-python-tony-honesto-bmgvc/) · [Real-Time Video Insight with OpenCV + Python](https://www.linkedin.com/pulse/real-time-video-insight-opencv-python-tony-honesto-yrfic/) |
| [`pytorch-lap-time`](labs/pytorch-lap-time) | A small PyTorch MLP that predicts lap time, with train/validation split, early stopping and a saved model | Python · PyTorch | [PyTorch for Predictive Analytics](https://www.linkedin.com/pulse/pytorch-predictive-analytics-tony-honesto-1z0lc/) |
| [`q-learning-pit-stops`](labs/q-learning-pit-stops) | Reinforcement learning from scratch: tabular Q-learning learns when to pit from tire wear and laps left | Python · NumPy | [PyTorch Reinforcement Learning](https://www.linkedin.com/pulse/pytorch-reinforcement-learning-tony-honesto-jh6ec/) |
| [`rag-retrieval-pipeline`](labs/rag-retrieval-pipeline) | The retrieval pattern LangChain wraps: chunking, TF-IDF retrieval, prompt assembly with citations and a pluggable LLM | Python · stdlib | [LangChain](https://www.linkedin.com/pulse/langchain-tony-honesto-gl8oc/) |
| [`robots-txt-audit`](labs/robots-txt-audit) | Audits robots.txt files for which AI crawlers (GPTBot, ClaudeBot, CCBot, Google-Extended...) are allowed, blocked or forgotten | Python · urllib.robotparser | [Age of AI Scrapers - Robots.txt](https://www.linkedin.com/pulse/age-ai-scrapers-robotstxt-tony-honesto-m1h4c/) |

### ☁️ Cloud, Data & Integration

| Lab | What it shows | Stack | Article |
|---|---|---|---|
| [`geotab-feed-client`](labs/geotab-feed-client) | A Geotab-style JSON-RPC client that pulls GPS data incrementally with GetFeed version tokens and session re-auth | Python · stdlib | [Geotab API Integration](https://www.linkedin.com/pulse/geotab-api-integration-tony-honesto-kzdac/) |
| [`graph-api-paging`](labs/graph-api-paging) | Reading a 25,000-item SharePoint list through Microsoft Graph paging, throttling retries and delta queries | Python · stdlib | [Managing Huge Data Sets in SharePoint Online](https://www.linkedin.com/pulse/managing-huge-data-sets-sharepoint-online-tony-honesto-nazyc/) · [SharePoint — More Than Just File Storage](https://www.linkedin.com/pulse/sharepoint-more-than-just-file-storage-tony-honesto-p2eic/) |
| [`itsm-sla-engine`](labs/itsm-sla-engine) | ITIL-style priority from impact x urgency, with SLA clocks that respect business hours and pause while waiting on the customer | Python · stdlib | [ITSM Platforms Are More Strategic Than Ever](https://www.linkedin.com/pulse/itsm-platforms-more-strategic-than-ever-tony-honesto-j8msc/) · [IFS assyst - Enterprise Service Delivery](https://www.linkedin.com/pulse/ifs-assyst-enterprise-service-delivery-tony-honesto-sncfc/) |
| [`kafka-consumer-groups`](labs/kafka-consumer-groups) | A partitioned log with keyed ordering, consumer groups, offset commits and rebalancing when a consumer dies | Python · stdlib | [Apache Kafka | Real-Time Event Streaming](https://www.linkedin.com/pulse/apache-kafka-real-time-event-streaming-tony-honesto-odsrc/) |
| [`kinesis-vs-dynamodb-streams`](labs/kinesis-vs-dynamodb-streams) | Side-by-side simulation of Kinesis shards and DynamoDB Streams: ordering, retention, fan-out and checkpointing | Python · stdlib | [Amazon Kinesis Streams vs DynamoDB Streams](https://www.linkedin.com/pulse/amazon-kinesis-streams-vs-dynamodb-tony-honesto-ble7c/) |
| [`kml-track-analysis`](labs/kml-track-analysis) | Parses a KML track, measures distance with the haversine formula and splits a lap into timed sectors | Python · stdlib | [KML Data Into Actionable Geospatial Insights](https://www.linkedin.com/pulse/kml-data-actionable-geospatial-insights-tony-honesto-bf14c/) |
| [`medallion-sql`](labs/medallion-sql) | Bronze, silver and gold layers in portable SQL, with data-quality checks and an idempotent incremental load | Python · SQL · SQLite | [Snowflake and Databricks — Two Platforms, One Data Universe](https://www.linkedin.com/pulse/snowflake-databricks-two-platforms-one-data-universe-tony-honesto-nzyic/) · [Google BigQuery](https://www.linkedin.com/pulse/google-bigquery-tony-honesto-w6fyc/) |
| [`parquet-feature-store`](labs/parquet-feature-store) | Writes partitioned Parquet features, then reads them with column pruning and partition filters for model training | Python · PyArrow · Parquet | [Parquet for Analytics & Feature Consumption](https://www.linkedin.com/pulse/parquet-analytics-feature-consumption-tony-honesto-oww7c/) |
| [`pubsub-subscriptions`](labs/pubsub-subscriptions) | AppSync-style pub/sub: clients subscribe with argument filters and only receive the mutations that match | Python · asyncio | [Pub/Sub | AWS AppSync](https://www.linkedin.com/pulse/pubsub-aws-appsync-tony-honesto-qy7cc/) |
| [`terraform-hybrid-cloud`](labs/terraform-hybrid-cloud) | A Terraform layout for a hybrid SaaS platform: reusable modules, per-environment stacks, validated in CI | Terraform · Azure · AWS | [Hybrid-Cloud SaaS Platform with Terraform](https://www.linkedin.com/pulse/hybrid-cloud-saas-platform-terraform-tony-honesto-adfac/) |
| [`twilio-sms-webhook`](labs/twilio-sms-webhook) | A Twilio SMS webhook that validates X-Twilio-Signature, handles opt-out keywords and replies in TwiML | Python · Flask | [Twilio for Customer Engagement](https://www.linkedin.com/pulse/twilio-customer-engagement-tony-honesto-hevsc/) |
| [`user-journey-funnel`](labs/user-journey-funnel) | Sessionises clickstream events, builds an ordered conversion funnel and finds where users drop off | Python · pandas | [User Journey Analytics with PySpark](https://www.linkedin.com/pulse/user-journey-analytics-pyspark-tony-honesto-ckqbc/) |
| [`xmpp-routing`](labs/xmpp-routing) | Two federated XMPP servers routing message and presence stanzas by JID, with roster subscriptions and offline delivery | Python · XMPP · XML stanzas | [XMPP — Real-Time, Federated Communication](https://www.linkedin.com/pulse/xmpp-real-time-federated-communication-tony-honesto-rdq1c/) |

### 🧱 Software Architecture & Engineering Practice

| Lab | What it shows | Stack | Article |
|---|---|---|---|
| [`grpc-telemetry`](labs/grpc-telemetry) | A .proto contract with unary and server-streaming calls, deadlines, and a size comparison of protobuf vs. JSON | Python · gRPC · Protocol Buffers | [gRPC Still Matters](https://www.linkedin.com/pulse/grpc-still-matters-tony-honesto-rdexc/) |
| [`java-coding-standards`](labs/java-coding-standards) | A Maven build with a Checkstyle quality gate and JUnit tests that fails on the issues SonarQube would flag | Java 21 · Maven · Checkstyle · JUnit 5 | [Enforcing Java Coding Standards with SONAR (SonarQube)](https://www.linkedin.com/pulse/enforcing-java-coding-standards-sonar-sonarqube-tony-honesto-ku4lc/) |
| [`podman-container`](labs/podman-container) | A rootless, non-root, health-checked container built and run with Podman in CI, plus a Containerfile policy linter | Podman · Containerfile · Python | [Podman - Containerized Deployment & Secure DevOps Pipelines](https://www.linkedin.com/pulse/podman-containerized-deployment-secure-devops-tony-honesto-wfryc/) |
| [`spring-boot-api`](labs/spring-boot-api) | A small Spring Boot REST API with validation, a service layer, error handling and MockMvc tests | Java 21 · Spring Boot 3 · Maven · JUnit 5 | [Spring Boot](https://www.linkedin.com/pulse/spring-boot-tony-honesto-ijwqc/) |
| [`wpf-mvvm`](labs/wpf-mvvm) | A WPF lap-timer app built MVVM-style: the view model is plain C# and unit-tested without a window | C# · .NET 10 · WPF · MVVM · xUnit | [Windows Desktop Applications with WPF](https://www.linkedin.com/pulse/windows-desktop-applications-wpf-tony-honesto-h0kmc/) |

### 🛠️ Simulation & Engineering

| Lab | What it shows | Stack | Article |
|---|---|---|---|
| [`battery-digital-twin`](labs/battery-digital-twin) | An equivalent-circuit battery twin that tracks state of charge and temperature, and flags when the real cell drifts from it | Python · NumPy | [Elysia - Battery Management Software | Digital Twin Intelligence](https://www.linkedin.com/pulse/elysia-battery-management-software-digital-twin-tony-honesto-adm1c/) |
| [`packaging-box-optimizer`](labs/packaging-box-optimizer) | Right-sized boxes vs. a fixed carton catalog: corrugate, void fill and dimensional-weight savings over a day of orders | Python | [AI-Enhanced On-Demand Packaging with Packsize](https://www.linkedin.com/pulse/ai-enhanced-on-demand-packaging-packsize-tony-honesto-d6qmc/) |
| [`python-vs-matlab`](labs/python-vs-matlab) | The same signal-processing task in Python and MATLAB syntax, run side by side (Octave in CI) with matching results | Python · NumPy · SciPy · GNU Octave | [Python vs MATLAB](https://www.linkedin.com/pulse/python-vs-matlab-tony-honesto-4bg9c/) · [MathWorks - MATLAB Onramp - Interactive Introduction](https://www.linkedin.com/pulse/matlab-onramp-free-interactive-introduction-tony-honesto-yg5pc/) |
| [`qr-codes`](labs/qr-codes) | Generates QR codes at each error-correction level, then damages them to show how much each level can survive | Python · OpenCV | [Python + QR Codes](https://www.linkedin.com/pulse/python-qr-codes-tony-honesto-98olc/) |
| [`quarter-car-virtual-testing`](labs/quarter-car-virtual-testing) | A quarter-car model run over a bump and rough road to sweep damper settings: ride comfort vs. road holding, before any hardware exists | Python · SciPy · ODE simulation | [Virtual Testing with MSC Adams](https://www.linkedin.com/pulse/virtual-testing-msc-adams-tony-honesto-wwq4c/) · [Helmut Schmidt University - Vehicle Dynamics Certificate](https://www.linkedin.com/pulse/helmut-schmidt-university-vehicle-dynamics-tony-honesto-lanoc/) · [MATLAB and Simulink](https://www.linkedin.com/pulse/matlab-simulink-tony-honesto-ltrfc/) |

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
