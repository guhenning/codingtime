from reportlab.pdfgen import canvas
import os

# Create a PDF
pdf = canvas.Canvas("file.pdf")

# Set the line color to blue (0, 0, 1 represents RGB color values)
pdf.setStrokeColorRGB(0, 0, 1)

# Set the line thickness to create a ticker line (adjust the value as needed)
line_thickness = 20  # Adjust this value for the desired line thickness

# Set the line thickness
pdf.setLineWidth(line_thickness)

# Draw a horizontal line at the top of the page with a height of 2cm
line_x1 = 50  # Starting x-coordinate
line_x2 = 560  # Ending x-coordinate
line_y = 798  # Y-coordinate of the line

pdf.line(
    line_x1, line_y, line_x2, line_y
)  # Adjust coordinates as needed for a larger line

# Reset the line thickness and color to their defaults (optional)
pdf.setLineWidth(1)  # Reset line thickness to the default
pdf.setStrokeColorRGB(0, 0, 0)  # Reset line color to black

# Add text to the PDF
pdf.setFont("Helvetica", 14)
pdf.drawString(50, 750, "Hello World")
pdf.drawString(50, 720, "Gustavo")

# Get the user's download directory based on the platform
if os.name == "posix":  # Linux and macOS
    download_dir = os.path.expanduser("~/Downloads")
elif os.name == "nt":  # Windows
    download_dir = os.path.expanduser("~\\Downloads")
else:
    raise RuntimeError("Unsupported operating system")

# Construct the full path to the PDF file in the download directory
pdf_file_path = os.path.join(download_dir, "file.pdf")

# Save the PDF to the user's download directory
pdf.save()

# Move the PDF to the download directory
os.rename("file.pdf", pdf_file_path)

print(f"PDF file saved to {pdf_file_path}")
