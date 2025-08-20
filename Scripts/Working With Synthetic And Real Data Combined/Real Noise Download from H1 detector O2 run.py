from gwpy.timeseries import TimeSeries
from gwosc.datasets import run_segment
import numpy as np
import os

# ==============================
# === SETTINGS AND PARAMETERS ===
# ==============================
detector = "H1"            # Detector choice: 'H1' (Hanford), 'L1' (Livingston), or 'V1' (Virgo)
sample_rate = 4096         # Sampling frequency in Hz
duration = 4               # Length of each segment in seconds
n_segments = 5000          # Number of noise segments to download
output_dir = "./real-noise-files/"
os.makedirs(output_dir, exist_ok=True)  # Create output folder if it doesn’t exist

# ===================================
# === GET AVAILABLE SEGMENT (O2) ===
# ===================================
# Get GPS start and end times for O2 run
# Note: run_segment("O2") returns (start, end) of the full O2 run
start, end = run_segment("O2")

# Create candidate 4-second start times covering the O2 run
all_start_times = np.arange(start, end - duration, duration)

# Shuffle start times for randomness (seed ensures reproducibility)
np.random.seed(42)
np.random.shuffle(all_start_times)

# ==============================
# === DOWNLOAD LOOP (O2 DATA) ===
# ==============================
downloaded = 0  # Counter for successfully downloaded segments
i = 0           # Index over candidate start times

while downloaded < n_segments and i < len(all_start_times):
    try:
        # Define GPS interval [gps_start, gps_end]
        gps_start = int(all_start_times[i])
        gps_end = gps_start + duration
        
        # Fetch strain data for the detector from GWOSC
        ts = TimeSeries.fetch_open_data(detector, gps_start, gps_end, sample_rate=sample_rate)

        # Ensure correct segment length (skip if corrupted or incomplete)
        if len(ts) != sample_rate * duration:
            i += 1
            continue

        # Save noise segment as a text file
        ts.write(os.path.join(output_dir, f"real_noise_{downloaded}.txt"))

        # Update counter after successful save
        downloaded += 1
    except Exception as e:
        # Handle errors (e.g., missing data, connection issues)
        print(f"⚠️ Skipping GPS {gps_start}: {e}")

    # Move to next candidate start time
    i += 1

# Final status update
print(f"✅ Downloaded {downloaded} real noise segments from {detector} into: {output_dir}")