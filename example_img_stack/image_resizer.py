import cv2
import os

input_dir = r'C:\path\to\your\images'
output_dir = os.path.join(input_dir, 'compressed_output')
os.makedirs(output_dir, exist_ok=True)

MAX_SIZE_MB = 1.0
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
TARGET_QUALITY = 85  # Initial guess (reduce if needed)
MIN_QUALITY = 20

def compress_to_size(image, out_path):
    quality = TARGET_QUALITY
    success = False

    while quality >= MIN_QUALITY:
        result = cv2.imencode('.jpg', image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        if not result[0]:
            print("❌ Failed to encode image.")
            break

        img_bytes = result[1].tobytes()

        if len(img_bytes) <= MAX_SIZE_BYTES:
            with open(out_path, 'wb') as f:
                f.write(img_bytes)
            success = True
            break
        quality -= 5  # Reduce quality until size is under limit

    if not success:
        print(f"⚠️ Could not compress under 1MB: {out_path}")

frame_files = [f for f in os.listdir(input_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

for file in frame_files:
    in_path = os.path.join(input_dir, file)
    img = cv2.imread(in_path)
    if img is None:
        print(f"⚠️ Skipping unreadable file: {file}")
        continue

    # Optional: Resize if you expect large dimensions
    # img = cv2.resize(img, (1920, 1080))  # Example: Resize to 1080p

    out_path = os.path.join(output_dir, os.path.splitext(file)[0] + '.jpg')
    compress_to_size(img, out_path)

print("✅ Batch compression complete.")
