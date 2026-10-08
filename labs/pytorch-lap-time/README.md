<sub>[← all labs](../../README.md)</sub>

# Lap-time prediction with PyTorch

> A small network, trained the careful way: normalised inputs, a validation split, early stopping, and a checkpoint that remembers its own scaling.

`Python` · `PyTorch`

**Companion to:**
- [PyTorch for Predictive Analytics](https://www.linkedin.com/pulse/pytorch-predictive-analytics-tony-honesto-1z0lc/)

## What it shows

- A two-hidden-layer MLP in PyTorch predicting lap time from tire age, fuel, track temperature and compound.
- Normalisation statistics computed on training data only, then saved inside the checkpoint.
- Early stopping on validation loss, restoring the best weights.
- Tests check it beats predicting the mean, learns the soft-tire cliff and round-trips through a saved file.

## Run it

```bash
bash labs/pytorch-lap-time/ci.sh        # install, test, run the demo
# or, from this folder:
python demo.py
```

Real output (from this lab's CI run):

```text
Trained on 3200 laps, stopped after 65 epochs, validation MAE 83 ms
  age  5, fuel  80 kg, soft: 91.93 s
  age 25, fuel  30 kg, soft: 92.68 s
  age 25, fuel  30 kg, hard: 91.92 s
Checkpoint round-trip identical: True
```

## What's in here

| File | Purpose |
|---|---|
| `laptime_net.py` | Data, model, training loop, save/load |
| `demo.py` | Trains, predicts three scenarios and checks the checkpoint |
| `tests/` | Accuracy, behaviour and checkpoint tests |
| `requirements.txt` | CPU-only PyTorch wheel |

## Simulated here vs. a real deployment

| In this lab | In production |
|---|---|
| Synthetic laps | Telemetry-derived features per lap |
| Small MLP | Sequence models over the stint, or gradient boosting if tabular |
| Local checkpoint | TorchScript/ONNX export and a model registry |
