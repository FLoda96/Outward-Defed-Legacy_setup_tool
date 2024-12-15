import os
import json
import xml.etree.ElementTree as ET

def extract_mod_items(base_dir, output_file):
    mod_items = []

    # Traverse the folder structure
    for root, dirs, files in os.walk(base_dir):
        # Check if the current directory contains the "SideLoader" folder and an "Items" folder
        if "SideLoader" in root and "Items" in root:
            # Loop through directories in the "Items" folder
            for item_folder in dirs:
                item_dir = os.path.join(root, item_folder)
                for file in os.listdir(item_dir):
                    if file.endswith(".xml"):
                        file_path = os.path.join(item_dir, file)
                        # Parse the XML file
                        try:
                            tree = ET.parse(file_path)
                            xml_root = tree.getroot()  # Renaming to xml_root to avoid conflict

                            # Check if the file contains the desired tags
                            tags = xml_root.find("Tags")
                            if tags is not None and any(
                                tag.text in ["Weapon", "Equipment"] for tag in tags.findall("string")
                            ):
                                # Extract Name and New_ItemID
                                new_item_id = xml_root.find("New_ItemID")
                                name = xml_root.find("Name")
                                if new_item_id is not None and name is not None:
                                    mod_items.append({
                                        "m_name": name.text,
                                        "ItemID": new_item_id.text
                                    })
                        except ET.ParseError as e:
                            print(f"Error parsing {file_path}: {e}")

    # Load the existing weapons_and_armors.json file
    try:
        with open(output_file, "r", encoding="utf-8") as file:
            existing_items = json.load(file)
    except (IOError, json.JSONDecodeError):
        existing_items = []

    # Merge the mod items with the existing items, avoiding duplicates
    existing_ids = {item["ItemID"] for item in existing_items}
    for mod_item in mod_items:
        if mod_item["ItemID"] not in existing_ids:
            existing_items.append(mod_item)

    # Save the updated weapons_and_armors.json file
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(existing_items, file, indent=4, ensure_ascii=False)
        print(f"Updated {output_file} with mod items.")
    except IOError as e:
        print(f"Error saving {output_file}: {e}")

if __name__ == "__main__":
    # Base directory for mods
    base_mod_dir = r"BepInEx/plugins"
    # Output file
    output_json = "weapons_and_armors.json"

    extract_mod_items(base_mod_dir, output_json)
