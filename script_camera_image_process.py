import os
from PIL import Image

input_folder = "csv/screenshot"
output_folder = "csv/screenshot/greyscale/"

os.makedirs(output_folder, exist_ok=True)

supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif')

# Process each image in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(supported_formats):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"grey_{filename}")

        try:
            with Image.open(input_path) as img:
                # Convert to greyscale
                grey_img = img.convert("L")
                grey_img.save(output_path)
                print(f"Processed and saved: {output_path}")
                
        except Exception as e:
            print(f"Failed to process {filename}: {e}")
