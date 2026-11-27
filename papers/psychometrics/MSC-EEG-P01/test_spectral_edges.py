"""Additional E3.1 regression cases; no empirical EEG data."""
import unittest
import numpy as np
from scipy.signal import welch
from eeg_athenalyze.analysis.spectral import welch_psd, band_power, Spectrum


class SpectralEdges(unittest.TestCase):
    def test_reference_edges(self):
        for n in (8, 9, 128, 129, 256, 257, 513):
            t = np.arange(n) / 128
            for values in (np.ones(n), (-1.) ** np.arange(n),
                           np.sin(2*np.pi*8*t), np.sin(2*np.pi*13*t)):
                with self.subTest(n=n, signal=values[:3]):
                    m = min(n, 256)
                    f, p = welch(values, fs=128, window=np.hanning(m),
                                 nperseg=m, noverlap=m-m//2,
                                 nfft=1 << (m-1).bit_length(),
                                 detrend="constant", scaling="density")
                    actual = welch_psd(tuple(values), 128)
                    np.testing.assert_array_equal(actual.frequencies_hz, f)
                    np.testing.assert_allclose(actual.power_uv2_per_hz, p,
                                               atol=1e-10, rtol=1e-10)
                    self.assertTrue(np.all(np.asarray(actual.power_uv2_per_hz) >= 0))
                    np.testing.assert_allclose(band_power(actual, 8, 13),
                        p[(f >= 8) & (f <= 13)].sum()*(f[1]-f[0]),
                        atol=1e-10, rtol=1e-10)

    def test_inclusive_band(self):
        self.assertEqual(band_power(Spectrum((7.,8.,9.,13.,14.), (0.,2.,3.,5.,0.)), 8, 13), 10.)

    def test_invalid_inputs(self):
        for samples, rate in [([0.]*7,128), ([0.]*8,0), ([0.]*8,-1),
                              ([0.]*8,float("nan")), ([0.]*8,float("inf")),
                              ([0.]*7+[float("nan")],128),
                              ([0.]*7+[float("inf")],128)]:
            with self.subTest(rate=rate, samples=samples):
                with self.assertRaises(ValueError):
                    welch_psd(samples, rate)
        for duration in (0,-1,float("nan"),float("inf")):
            with self.assertRaises(ValueError):
                welch_psd([0.]*8,128,segment_seconds=duration)


if __name__ == "__main__":
    unittest.main()
