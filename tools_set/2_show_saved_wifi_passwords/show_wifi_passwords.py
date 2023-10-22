import subprocess  # Module to run system commands
import re  # Module to use regular expressions (str)


# Save the content of terminal response and decote it
command_response = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], capture_output=True
).stdout.decode()


# Save all wifi names from the command_response
wifi_names = re.findall("All User Profile     : (.*)\r", command_response)

# Create empty list to use it in the loop saving wifi name and passwords
wifi_list = []

if len(wifi_names) != 0:
    for name in wifi_names:
        # Create new dictionary for every network name
        wifi = {}

        # For this name look for the wifi info that contains password
        # Checking if Security key is not absent so we can get the password
        wifi_info = subprocess.run(
            ["netsh", "wlan", "show", "profile", name], capture_output=True
        ).stdout.decode()
        # If Security Key is Absent try next wifi name
        if re.search("Security key           : Absent", wifi_info):
            continue
        else:
            # Save name to dictionary
            wifi["ssid"] = name
            # Run command that shows wifi password "key=clear"
            wifi_info_with_key = subprocess.run(
                ["netsh", "wlan", "show", "profile", name, "key=clear"],
                capture_output=True,
            ).stdout.decode()
            # Find the password in the saved wifi_info_with_key
            password = re.search("Key Content            : (.*)\r", wifi_info_with_key)
        if password == None:
            wifi["password"] = None
        else:
            # Save password to dictionary
            wifi["password"] = password[1]
        # Save dictionary to wifi_list
        wifi_list.append(wifi)

for x in range(len(wifi_list)):
    print(wifi_list[x])
