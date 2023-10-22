from gtts import gTTS
from playsound import playsound
import json
import os


language_info = {}

with open("./3_text_to_audio/languages.json", "r", encoding="utf-8") as file:
    language_info = json.load(file)

text_to_convert = input("Enter the text to convert to speech: ")

for key, info in language_info.items():
    print(f"{key} - {info['language_name']}")


print("Choose the speech language!")


while True:
    # User input to select language
    language_option = input("Enter the number for your preferred language: ")

    # Check if the selected key is valid
    if language_option in language_info:
        # Take the dictionary key and values
        selected_language_info = language_info[language_option]
        # Extract language value
        language = selected_language_info["language_code"]
        # Extract domain value
        domain = selected_language_info["domain"]
        break
    else:
        print("Invalid language selection. Please choose a valid number.")


text_to_convert = gTTS(text=text_to_convert, lang=language, tld=domain, slow=False)


# Determine the download folder based on the operating system
download_folder = os.path.expanduser("~")  # Default home directory

if os.name == "posix":  # macOS or Linux
    download_folder = os.path.join(download_folder, "Downloads")
elif os.name == "nt":  # Windows
    download_folder = os.path.join(download_folder, "Downloads")
else:
    print("Unsupported operating system. Download folder not set.")

# Create the download folder if it doesn't exist
os.makedirs(download_folder, exist_ok=True)

audio_output = "speech.mp3"

# Save Audio in the Download folder
download_path = os.path.join(download_folder, audio_output)
text_to_convert.save(download_path)

playsound(download_path)
