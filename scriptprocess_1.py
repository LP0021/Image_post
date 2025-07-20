import cv2
import numpy as np
import os

input_dir = r'C:\Users\paule\vsc_local_user\sequator_photography\2025-07-18\script_processing'
output_dir = r'C:\Users\paule\vsc_local_user\sequator_photography\2025-07-18\script_processing\script_processed_output'
os.makedirs(output_dir, exist_ok=True)

frame_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.jpg')])
brightness_list = []

# 1. Measure current brightness per frame
for file in frame_files:
    img = cv2.imread(os.path.join(input_dir, file))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)
    brightness_list.append(brightness)

# 2. Define linear brightness targets
min_brightness = min(brightness_list)
max_brightness = max(brightness_list)
num_frames = len(brightness_list)

# Create a linear brightness ramp (e.g., from dawn to daylight)
linear_targets = np.linspace(min_brightness, max_brightness, num=num_frames)

# 3. Normalize frames toward linear ramp
for i, file in enumerate(frame_files):
    img = cv2.imread(os.path.join(input_dir, file)).astype(np.float32)
    current_brightness = brightness_list[i]
    target_brightness = linear_targets[i]

    if current_brightness == 0:
        factor = 1.0  # avoid divide-by-zero
    else:
        factor = target_brightness / current_brightness

    adjusted = np.clip(img * factor, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(output_dir, file), adjusted)

print("✅ Linear brightness normalization completed.")
