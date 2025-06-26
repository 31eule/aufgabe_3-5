import numpy as np

# Parameter
sampling_rate = 500  # Hz
duration_sec = 15  # Dauer in Sekunden
bpm = 60  # Herzfrequenz
num_samples = sampling_rate * duration_sec
time = np.arange(num_samples)

# Herzschläge positionieren
rr_interval = int(sampling_rate * 60 / bpm)
r_peaks = np.arange(rr_interval, num_samples, rr_interval)

# EKG-Kurve simulieren
signal = np.zeros(num_samples)

# Ein einfacher QRS-Komplex-Modellierer
def add_qrs(signal, center, amp=80):
    # R-Zacke
    if center - 2 >= 0 and center + 2 < len(signal):
        signal[center - 2] += int(amp * 0.3)   # Q
        signal[center] += int(amp)            # R
        signal[center + 2] += int(amp * 0.4)   # S
    return signal

# Grundlinie simulieren (leicht fluktuierend)
baseline = 300 + 10 * np.sin(2 * np.pi * time / (sampling_rate * 3))

# QRS-Komplexe hinzufügen
for peak in r_peaks:
    signal = add_qrs(signal, peak, amp=80)

# Gesamtsignal: baseline + QRS
ekg = baseline + signal

# Werte runden
ekg = np.round(ekg).astype(int)

# Textdatei schreiben (Tab-getrennt)
with open("bradykardie_simuliert_realistisch.txt", "w") as f:
    for t, v in zip(time, ekg):
        f.write(f"{v}\t{t}\n")

print("Datei erfolgreich erstellt: bradykardie_simuliert_realistisch.txt")