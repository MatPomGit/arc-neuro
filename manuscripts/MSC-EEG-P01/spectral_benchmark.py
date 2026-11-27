"""Compare the pinned Neurolyze Welch implementation to an explicit SciPy reference."""
import csv
import sys

import numpy as np
from scipy.signal import welch
from eeg_athenalyze.analysis.spectral import band_power, welch_psd


def main():
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["sample_rate_hz", "samples", "signal", "max_psd_difference", "alpha_power_uv2"])
    rng = np.random.default_rng(27112026)
    for rate in (128, 200, 256):
        for n in (rate + 3, 5 * rate + 7):
            t = np.arange(n) / rate
            for label, values in (
                ("pure_alpha", 20 * np.sin(2 * np.pi * 10 * t)),
                ("alpha_drift_noise", 5 * np.sin(2 * np.pi * 10 * t) + 4 * t + rng.normal(0, 3, n)),
                ("zero", np.zeros(n)),
            ):
                actual = welch_psd(tuple(values), rate)
                segment = min(n, 2 * rate)
                step = segment // 2
                f, p = welch(values, fs=rate, window=np.hanning(segment),
                             nperseg=segment, noverlap=segment-step, nfft=1 << (segment-1).bit_length(),
                             detrend="constant", scaling="density", return_onesided=True, average="mean")
                np.testing.assert_allclose(actual.frequencies_hz, f, rtol=0, atol=0)
                np.testing.assert_allclose(actual.power_uv2_per_hz, p, rtol=1e-10, atol=1e-10)
                alpha = band_power(actual, 8, 13)
                np.testing.assert_allclose(alpha, p[(f >= 8) & (f <= 13)].sum() * (f[1] - f[0]),
                                           rtol=1e-10, atol=1e-10)
                writer.writerow([rate, n, label,
                                 f"{np.max(np.abs(actual.power_uv2_per_hz - p)):.9e}", f"{alpha:.9f}"])


if __name__ == "__main__":
    main()
