import cv2
import os

def convert_images_to_webp(input_folder=".", quality=95):
    """
    Convert all images in a folder to WebP format using OpenCV.

    Args:
        input_folder (str): Path to the folder containing input images. Defaults to current folder.
        quality (int, optional): WebP quality (0-100). Default is 95.
    """
    # Supported formats OpenCV can read
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            if img is None:
                print(f"Skipping {filename} (unable to read).")
                continue

            # Create new filename with .webp extension
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(input_folder, f"{name}.webp")

            # Save as WebP
            cv2.imwrite(output_path, img, [int(cv2.IMWRITE_WEBP_QUALITY), quality])
            print(f"Converted: {filename} -> {output_path}")

def main():
    convert_images_to_webp(".", quality=95)

if __name__ == "__main__":
    main()
