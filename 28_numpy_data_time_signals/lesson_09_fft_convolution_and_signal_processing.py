import numpy as np

# FOURIER TRANSFORMS: a signal as a sum of sine waves
#   np.fft.fft / ifft            complex spectrum of N samples (and back)
#   np.fft.rfft / irfft          the same for REAL signals: only the non-negative frequencies (half the work)
#   np.fft.fftfreq(n, d) / rfftfreq(n, d)    the frequency of every bin; d = 1 / sampling rate
#   np.fft.fftshift             put the zero frequency in the middle
#   amplitude of a sine at a bin:  2 * |X[k]| / N        (the DC bin 0 needs no factor 2)
# Frequency resolution = sampling rate / N. In this lesson fs = 1000 Hz and N = 1000, so every bin is 1 Hz
# and the test signals sit exactly on bins: that keeps the numbers clean.

fs, N = 1000, 1000
t = np.arange(N) / fs
signal = 1.0 * np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

# DISCRETE FOURIER TRANSFORM by the definition (N x N matrix) and by the FFT
x = signal[:64]
k = np.arange(64).reshape(-1, 1)
dft = np.exp(-2j * np.pi * k * np.arange(64) / 64) @ x
print(np.allclose(dft, np.fft.fft(x)))                  # same result; the FFT needs N log N steps instead of N * N

# FAST FOURIER TRANSFORM: which frequencies are in the signal?
spectrum = np.fft.rfft(signal)
freqs = np.fft.rfftfreq(N, 1 / fs)
amplitude = 2 * np.abs(spectrum) / N
print(spectrum.shape, freqs[:3], freqs[-1])
print(np.sort(freqs[np.argsort(amplitude)[-2:]]), np.round(amplitude[[50, 120]], 3))
print(np.fft.fftfreq(8, 1 / 8), np.fft.fftshift(np.fft.fftfreq(8, 1 / 8)))

# INVERSE: rebuild the signal from its spectrum
print(np.allclose(np.fft.irfft(spectrum, n=N), signal))
print(np.allclose(np.fft.ifft(np.fft.fft(signal)).real, signal))

# SIGNAL PROCESSING: remove the 120 Hz part with a low-pass filter in the frequency domain
filtered = spectrum.copy()
filtered[freqs > 80] = 0
low_passed = np.fft.irfft(filtered, n=N)
print(np.allclose(low_passed, np.sin(2 * np.pi * 50 * t)))

# Remove 50 Hz hum from a slow 3 Hz signal (a notch filter)
slow = np.sin(2 * np.pi * 3 * t)
noisy = slow + 0.8 * np.sin(2 * np.pi * 50 * t)
spec = np.fft.rfft(noisy)
spec[(freqs > 48) & (freqs < 52)] = 0
print(np.allclose(np.fft.irfft(spec, n=N), slow))

# Parseval: the energy is the same in both domains
print(np.isclose(np.sum(signal ** 2), np.sum(np.abs(np.fft.fft(signal)) ** 2) / N))

# ALIASING: a 60 Hz sine sampled at only 100 Hz (Nyquist limit 50 Hz) looks like 40 Hz
fs2 = 100
t2 = np.arange(100) / fs2
alias = np.sin(2 * np.pi * 60 * t2)
f2 = np.fft.rfftfreq(100, 1 / fs2)
print(f2[np.argmax(np.abs(np.fft.rfft(alias)))])

# LEAKAGE: a frequency between two bins spreads out; a window reduces the spread far from the peak
odd = np.sin(2 * np.pi * 52.5 * t)
plain = np.abs(np.fft.rfft(odd)) * 2 / N
windowed = np.abs(np.fft.rfft(odd * np.hanning(N))) * 2 / N
print(plain[200] > windowed[200], windowed[200] < 1e-3)

# FOURIER SERIES: a square wave is a sum of odd sine harmonics: (4/pi) * sum of sin(k x) / k for odd k
x = np.linspace(0, 1, 1000, endpoint=False)
square = np.where(x < 0.5, 1.0, -1.0)
errors = []
for terms in (1, 3, 9, 49):
    series = sum(4 / np.pi * np.sin(2 * np.pi * h * x) / h for h in range(1, 2 * terms, 2))
    errors.append(float(np.mean((series - square) ** 2)))
print(np.round(errors, 3), errors[0] > errors[1] > errors[2] > errors[3])

# CONVOLUTION: slide one array over another
print(np.convolve([1, 2, 3], [0, 1, 0.5]))
a, b = np.arange(1.0, 6.0), np.array([1.0, 0.0, -1.0])
print(len(np.convolve(a, b)), len(np.convolve(a, b, mode="same")), len(np.convolve(a, b, mode="valid")))
print(np.convolve(a, np.ones(3) / 3, mode="valid"))                           # moving average = convolution with a box
fast = np.fft.irfft(np.fft.rfft(a, 8) * np.fft.rfft(b, 8), 8)[:len(a) + len(b) - 1]
print(np.allclose(fast, np.convolve(a, b)))                                   # the convolution theorem

# CROSS-CORRELATION: how many samples is one signal delayed against another?
pulse = np.zeros(50)
pulse[10:14] = [1.0, 2.0, 3.0, 1.0]
delayed = np.roll(pulse, 7)
lag = np.argmax(np.correlate(delayed, pulse, mode="full")) - (len(pulse) - 1)
print(lag)

# A smoothing FIR filter and a differentiator
steps = np.array([0, 0, 0, 1, 1, 1, 1], dtype=float)
print(np.round(np.convolve(steps, [0.25, 0.5, 0.25], mode="same"), 2), np.convolve(steps, [1, -1], mode="valid"))

# EXPECTED OUTPUT
# True
# (501,) [0. 1. 2.] 500.0
# [ 50. 120.] [1.  0.5]
# [ 0.  1.  2.  3. -4. -3. -2. -1.] [-4. -3. -2. -1.  0.  1.  2.  3.]
# True
# True
# True
# True
# True
# 40.0
# True True
# [0.189 0.067 0.023 0.004] True
# [0.  1.  2.5 4.  1.5]
# 7 5 3
# [2. 3. 4.]
# True
# 7
# [0.   0.   0.25 0.75 1.   1.   0.75] [0. 0. 1. 0. 0. 0.]