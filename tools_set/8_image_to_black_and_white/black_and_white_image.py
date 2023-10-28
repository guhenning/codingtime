import tkinter as tk
from tkinter import filedialog
from PIL import Image


# Function to convert an image to black and white
def convert_to_black_and_white(input_file, output_file):
    img = Image.open(input_file)
    img = img.convert("L")
    img.save(output_file)


# Create a file dialog to select an image file
root = tk.Tk()
root.withdraw()  # Hide the main tkinter window

file_path = filedialog.askopenfilename(
    title="Select an image file",
    filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff *.ppm *.pgm")],
)

if not file_path:
    print("No file selected. Exiting.")
else:
    # Modify the filename for the black and white image
    output_file = file_path.split(".")
    output_file = output_file[0] + "_black_and_white." + output_file[1]

    # Convert the image to black and white and save it
    convert_to_black_and_white(file_path, output_file)
    print(f"Image converted to black and white and saved as {output_file}")

# Close the tkinter window
root.destroy()
