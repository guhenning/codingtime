import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog


def change_color(image_path, target_color_hash, new_color_hash):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the target color hash to BGR format
    target_color = tuple(int(target_color_hash[i : i + 2], 16) for i in (0, 2, 4))

    # Convert the new color hash to BGR format
    new_color = tuple(int(new_color_hash[i : i + 2], 16) for i in (0, 2, 4))

    # Define a tolerance for color matching
    color_tolerance = 30

    # Create a mask for the target color within the specified tolerance
    lower_bound = np.array(
        [max(0, c - color_tolerance) for c in target_color], dtype=np.uint8
    )
    upper_bound = np.array(
        [min(255, c + color_tolerance) for c in target_color], dtype=np.uint8
    )
    mask = cv2.inRange(image, lower_bound, upper_bound)

    # Create a new color image with the specified new_color
    new_color_image = np.full_like(image, new_color, dtype=np.uint8)

    # Replace the target color with the new_color using the mask
    result_image = np.where(mask[:, :, None] > 0, new_color_image, image)

    return result_image


def select_image():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(title="Select an image")

    if not file_path:
        print("No image selected.")
        return

    target_color_hash = input("Enter the hex code of the target color (e.g., FF5733): ")
    new_color_hash = input("Enter the hex code of the new color (e.g., 00FF00): ")

    result = change_color(file_path, target_color_hash, new_color_hash)

    result_path = "result_image.jpg"
    cv2.imwrite(result_path, result)
    print(f"Image with the specified color change saved as {result_path}")


if __name__ == "__main__":
    select_image()
