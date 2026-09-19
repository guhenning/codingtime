import json
import os
import plyvel  # plyvel-ci exposes itself under the normal name 'plyvel'

# Path to your extension settings directory
db_path = r"C:\Users\gusta\AppData\Local\Microsoft\Edge\User Data\Default\Local Extension Settings\ddijhlpnokdnogjedjpemidaoicflael"




def extract_data_from_extension_file(db_path):
    # TRAP 1: Edge locks the LevelDB engine if it's running in the background.
    # This forcefully stops Edge so Python can read the file.
    print("Ensuring Microsoft Edge is closed...")
    os.system("taskkill /f /im msedge.exe >nul 2>&1")

    try:
        # Open the database in read-only mode
        db = plyvel.DB(db_path, create_if_missing=False)
        
        target_key = b"scraping.option.posts"
        raw_value = db.get(target_key)
        
        if raw_value:
            # TRAP 2: Chromium adds a 1-to-5 byte header prefix to Local Extension values.
            # We search for the first bracket '{' or '[' to cleanly isolate the JSON payload.
            json_start = raw_value.find(b'{') if b'{' in raw_value else raw_value.find(b'[')
            
            if json_start != -1:
                clean_bytes = raw_value[json_start:]
                decoded_value = clean_bytes.decode('utf-8', errors='ignore')
                json_data = json.loads(decoded_value)
                
                # Save as an indented, easy-to-read .json file
                with open("instagram_scraped_data.json", "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=4, ensure_ascii=False)
                    
                print("Success! The data has been saved cleanly to 'instagram_scraped_data.json'.")
            else:
                print("Found the key, but the data does not appear to be valid JSON text.")
        else:
            print("Key 'scraping.option.posts' was not found in this database instance.")
            
        db.close()

    except Exception as e:
        print(f"An error occurred: {e}")

json_path = r"tools_set\14_extension_extractor\instagram_scraped_data.json"
def write_urls_to_txt(json_path):

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    export = data.get("export")

    urls = []

    print(f"Processing total of {len(export)}")
    for post in export:

        post_data = post.get("formatted")       
        

        if post_data.get("Post Author URL") != "https://www.instagram.com/gu.henning/":
            urls.append(post_data.get("Post URL"))

    
    print(f"Found total of {len(urls)}")


    with open("intagram_urls.txt", 'w') as f:
        for url in urls:
            f.write(f'{url}\n')

write_urls_to_txt(json_path)