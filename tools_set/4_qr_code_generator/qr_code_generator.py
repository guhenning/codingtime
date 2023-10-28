import qrcode
import os

from PIL import Image

# Data to be in QR Code
data = input(
    "Type the data you want to add to QR Code Ex.: https://gustavohenning.com : "
)

# Generate QR Code
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(data)
qr.make(fit=True)

# Generate image from QR Code
image = qr.make_image(fill="black", back_color="white")


# Save image to download path
download_folder = os.path.expanduser("~")  # Default home directory

if os.name == "posix":  # macOS or Linux
    download_folder = os.path.join(download_folder, "Downloads")
elif os.name == "nt":  # Windows
    download_folder = os.path.join(download_folder, "Downloads")
else:
    print("Unsupported operating system. Download folder not set.")

# Create the download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

image.save(download_folder + "/qr_code.png")

print(f"QR Code has been downloaded to {download_folder}")
