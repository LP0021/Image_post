import cv2
import numpy as np
import os

input_dir = r'C:\Users\paule\vsc_local_user\sequator_photography\2025-07-18\script_processing'
output_dir = os.path.join(input_dir, 'script_processed_output_2saturation')
os.makedirs(output_dir, exist_ok=True)

frame_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith(('.jpeg', '.jpg'))])
brightness_list = []
rgb_means = []
saturation_means = []
valid_files = []

if not frame_files:
    raise FileNotFoundError(f"No JPEG files found in {input_dir}")

# 1. Analyze frames
for file in frame_files:
    img_path = os.path.join(input_dir, file)
    img = cv2.imread(img_path)

    if img is None:
        print(f"⚠️ Skipping unreadable image: {file}")
        continue

    img_float = img.astype(np.float32)

    # Brightness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness_list.append(np.mean(gray))

    # Color
    mean_per_channel = np.mean(img_float, axis=(0, 1))  # BGR order
    rgb_means.append(mean_per_channel[::-1])  # Convert to RGB

    # Saturation
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mean_saturation = np.mean(hsv[:, :, 1])  # S channel
    saturation_means.append(mean_saturation)

    valid_files.append(file)

if not brightness_list:
    raise RuntimeError("No valid images could be read. Check file integrity or formats.")

# 2. Build target linear curves
num_frames = len(valid_files)
brightness_target = np.linspace(min(brightness_list), max(brightness_list), num_frames)
r_target = np.linspace(min(r[0] for r in rgb_means), max(r[0] for r in rgb_means), num_frames)
g_target = np.linspace(min(r[1] for r in rgb_means), max(r[1] for r in rgb_means), num_frames)
b_target = np.linspace(min(r[2] for r in rgb_means), max(r[2] for r in rgb_means), num_frames)
s_target = np.linspace(min(saturation_means), max(saturation_means), num_frames)

# 3. Normalize
for i, file in enumerate(valid_files):
    img_path = os.path.join(input_dir, file)
    img = cv2.imread(img_path).astype(np.float32)

    # Brightness normalization
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    current_brightness = np.mean(gray)
    brightness_factor = brightness_target[i] / current_brightness if current_brightness else 1.0
    img *= brightness_factor

    # Color normalization (match to RGB curve)
    current_rgb = np.mean(img, axis=(0, 1))  # BGR
    target_rgb = np.array([b_target[i], g_target[i], r_target[i]])  # BGR order

    color_factors = np.divide(target_rgb, current_rgb, out=np.ones_like(current_rgb), where=current_rgb != 0)
    img *= color_factors.reshape((1, 1, 3))

    # Optional: Saturation normalization (via HSV)
    img_uint8 = np.clip(img, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2HSV).astype(np.float32)
    current_sat = np.mean(hsv[:, :, 1])
    target_sat = s_target[i]
    sat_factor = target_sat / current_sat if current_sat else 1.0
    hsv[:, :, 1] *= sat_factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)

    # Convert back
    final_img = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    out_path = os.path.join(output_dir, file)
    cv2.imwrite(out_path, final_img)

print(f"✅ Normalization complete. {len(valid_files)} images processed.")
