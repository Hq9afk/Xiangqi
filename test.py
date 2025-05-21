# Save this as batch_resave_png.py
from PIL import Image
import os

sub_dirs = ["buttons", "pieces", "misc"]


for sub_dir in sub_dirs:
    input = f"asset\images\{sub_dir}"
    output = f"image_fixed\{sub_dir}"

    os.makedirs(output, exist_ok=True)

    for filename in os.listdir(input):
        if filename.lower().endswith(".png"):
            img_path = os.path.join(input, filename)
            img = Image.open(img_path)
            img.save(os.path.join(output, filename))
            print(f"Re-saved: {filename}")
