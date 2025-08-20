import os
import shutil

# ==============================
# === PATH SETTINGS ===
# ==============================
input_dir = "./real-noise-files/"          # Source directory (raw downloaded noise files)
output_dir = "./dataset/real-noise-files/" # Destination directory (filtered files)
os.makedirs(output_dir, exist_ok=True)     # Create output folder if it doesn’t exist

# ==============================
# === FILE SIZE THRESHOLD ===
# ==============================
MIN_SIZE_KB = 800  # Minimum file size (in KB) to accept as valid

# ==============================
# === FILTERING LOOP ===
# ==============================
moved = 0   # Counter for successfully copied files
skipped = 0 # Counter for skipped (too small) files

for filename in os.listdir(input_dir):
    # Skip non-text files
    if not filename.endswith(".txt"):
        continue

    full_path = os.path.join(input_dir, filename)
    file_size_kb = os.path.getsize(full_path) / 1024

    # --- Check file size against threshold ---
    if file_size_kb >= MIN_SIZE_KB:
        # Copy valid file into dataset folder
        shutil.copy(full_path, os.path.join(output_dir, filename))
        moved += 1
    else:
        # Skip invalid (too small) file
        skipped += 1
        print(f"❌ Skipping {filename}: only {file_size_kb:.1f} KB")

# ==============================
# === FINAL SUMMARY ===
# ==============================
print(f"\n✅ Done! {moved} files moved to '{output_dir}'")
print(f"⚠️ {skipped} files were too small and skipped.")
