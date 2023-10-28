from rembg import remove
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os

# Create a Tkinter root window (it won't be visible)
root = tk.Tk()
root.withdraw()

# Open a file dialog to select the input image
input_path = filedialog.askopenfilename()

# Check if the user selected a file
if input_path:
    inp = Image.open(input_path)

    # Extract the directory of the input file
    input_directory = os.path.dirname(input_path)

    # Construct the output path in the same directory as the input
    output_path = os.path.join(input_directory, "removed_background.png")

    # Perform background removal
    output = remove(inp)

    # Save the result in the same directory as the input
    output.save(output_path)
    print(f"Background removed image saved as {output_path}")
else:
    print("No file selected.")

# Close the Tkinter root window
root.destroy()
