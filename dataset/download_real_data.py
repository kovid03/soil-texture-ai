"""
Download real soil images from Phantom-fs/Soil-Classification-Dataset (GitHub).
Uses BOTH Original and CyAUG datasets for more data.

Source: https://github.com/Phantom-fs/Soil-Classification-Dataset

Mapping (7 GitHub classes -> our 5 target classes):
  Black_Soil      -> Clay        (black/vertisol soils = high clay content)
  Alluvial_Soil   -> Loam        (alluvial soils = typically loamy)
  Red_Soil        -> Sandy       (red soils = sandy texture)
  Yellow_Soil     -> Loamy Sand  (yellow soils = sandy-loam mix)
  Laterite_Soil   -> Sandy Loam  (laterite = iron-rich sandy-loam)
  Arid_Soil       -> Sandy       (arid/desert soils = very sandy)  [extra for Sandy]
  Mountain_Soil   -> Loam        (mountain soils = often loamy)    [extra for Loam]
"""

import os
import urllib.request
import time
import sys

ORIG_URL = "https://raw.githubusercontent.com/Phantom-fs/Soil-Classification-Dataset/main/Orignal-Dataset"
CYAUG_URL = "https://raw.githubusercontent.com/Phantom-fs/Soil-Classification-Dataset/main/CyAUG-Dataset"

OUTPUT_DIR = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'dataset', 'train')

# Primary mapping (1 source -> 1 target)
PRIMARY = {
    "Black_Soil":    "Clay",
    "Alluvial_Soil": "Loam",
    "Red_Soil":      "Sandy",
    "Yellow_Soil":   "Loamy Sand",
    "Laterite_Soil": "Sandy Loam",
}

# Secondary sources to boost classes that need more images
SECONDARY = {
    "Arid_Soil":     "Sandy",
    "Mountain_Soil": "Loam",
}

IMAGES_PER_SOURCE = 40  # images to download from each source folder


def download_from_source(base_url, src_folder, target_class, tag, max_images):
    """Download images from a GitHub raw URL into the target class folder."""
    target_dir = os.path.join(OUTPUT_DIR, target_class)
    os.makedirs(target_dir, exist_ok=True)

    existing = len([f for f in os.listdir(target_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    downloaded = 0

    for i in range(1, 500):
        if downloaded >= max_images:
            break
        url = f"{base_url}/{src_folder}/{i}.jpg"
        dest = os.path.join(target_dir, f"{tag}_{src_folder}_{i}.jpg")
        if os.path.exists(dest):
            downloaded += 1
            continue
        try:
            urllib.request.urlretrieve(url, dest)
            downloaded += 1
            sys.stdout.write(f"\r  {tag}/{src_folder} -> {target_class}: {downloaded}/{max_images}")
            sys.stdout.flush()
            time.sleep(0.15)
        except Exception:
            continue

    print(f"\r  {tag}/{src_folder} -> {target_class}: {downloaded} downloaded")
    return downloaded


def main():
    print("=== Downloading Real Soil Images ===\n")

    # Primary sources from Original dataset
    print("--- Original Dataset ---")
    for src, tgt in PRIMARY.items():
        download_from_source(ORIG_URL, src, tgt, "orig", IMAGES_PER_SOURCE)

    # Primary sources from CyAUG dataset (GAN-augmented, more variety)
    print("\n--- CyAUG Dataset (GAN-augmented) ---")
    for src, tgt in PRIMARY.items():
        download_from_source(CYAUG_URL, src, tgt, "cyaug", IMAGES_PER_SOURCE)

    # Secondary sources for balance
    print("\n--- Secondary sources for class balance ---")
    for src, tgt in SECONDARY.items():
        download_from_source(ORIG_URL, src, tgt, "orig2", 20)
        download_from_source(CYAUG_URL, src, tgt, "cyaug2", 20)

    # Summary
    print("\n\n=== Dataset Summary ===")
    total = 0
    for cls in sorted(os.listdir(OUTPUT_DIR)):
        cls_path = os.path.join(OUTPUT_DIR, cls)
        if os.path.isdir(cls_path):
            count = len([f for f in os.listdir(cls_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"  {cls}: {count} images")
            total += count
    print(f"\n  TOTAL: {total} images")
    print(f"\nDataset source: https://github.com/Phantom-fs/Soil-Classification-Dataset")


if __name__ == "__main__":
    main()
