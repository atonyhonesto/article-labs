"""Three everyday engineering calculations, written the NumPy way.

The same steps are in analysis.m in MATLAB syntax. Both print identical key=value
lines so CI can run them side by side (MATLAB code runs under GNU Octave there).

  1. Distance from a speed trace        trapezoidal integration
  2. Dominant vibration frequency       FFT of a suspension sensor
  3. Brake cooling time constant        straight-line fit to log(temperature)
"""
import numpy as np

FS = 200.0                                    # Hz
t = np.arange(0, 10, 1 / FS)                  # 10 s, 2000 samples (MATLAB: t = 0:1/fs:10-1/fs)

speed = 60 + 8 * np.sin(2 * np.pi * 0.1 * t)                          # m/s
vib = np.sin(2 * np.pi * 12.5 * t) + 0.4 * np.sin(2 * np.pi * 31 * t) + 0.1 * np.sin(97 * t)
temp = 25 + 500 * np.exp(-t / 3.2) + 0.5 * np.sin(5 * t)              # °C

distance = np.trapezoid(speed, t)

spec = np.abs(np.fft.rfft(vib))
freqs = np.fft.rfftfreq(len(vib), 1 / FS)
dominant = freqs[np.argmax(spec[1:]) + 1]                             # skip DC

slope, _ = np.polyfit(t, np.log(temp - 25), 1)
tau = -1 / slope

results = {"distance_m": distance, "dominant_hz": dominant, "tau_s": tau, "mean_speed": speed.mean()}

if __name__ == "__main__":
    for k, v in results.items():
        print(f"{k}={v:.4f}")
