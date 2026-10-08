<sub>[← all labs](../../README.md)</sub>

# Reinforcement learning: learning when to pit

> Nobody tells the agent how tires work. It learns when to stop from the time each lap costs.

`Python` · `NumPy`

**Companion to:**
- [PyTorch Reinforcement Learning](https://www.linkedin.com/pulse/pytorch-reinforcement-learning-tony-honesto-jh6ec/)

## What it shows

- Tabular Q-learning with ε-greedy exploration over (laps left, tire wear) states.
- Rewards are just minus the seconds each lap costs, with a fixed pit-stop loss.
- An exact dynamic-programming optimum, so the learned policy can be checked: it lands within a few percent.
- The same loop a PyTorch DQN uses; the table is what the neural network replaces when the state gets large.

## Run it

```bash
bash labs/q-learning-pit-stops/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output:

```text
start wear 0: learned policy pits on laps [9, 17, 25, 33], loses 171 s to wear and stops (optimum 166 s, never pitting 296 s)
start wear 6: learned policy pits on laps [1, 9, 17, 25, 33], loses 191 s to wear and stops (optimum 186 s, never pitting 340 s)
```

## What's in here

| File | Purpose |
|---|---|
| `qlearn.py` | Environment, Q-learning, policy rollout and DP optimum |
| `demo.py` | Learns, then compares to the optimum and to never pitting |
| `tests/` | Beats never-pitting, near-optimal, sensible stop timing |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Bucketed states | Continuous state (gaps, fuel, weather) with a neural Q-function |
| Fixed pit loss | Track position, traffic and caution timing |
| Single car | Multi-agent effects: rivals react to your stop |
