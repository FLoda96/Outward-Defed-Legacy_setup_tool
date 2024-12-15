import json
import gzip
import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Load data directly from weapons_and_armors.json
try:
    with open("weapons_and_armors.json", "r", encoding="utf-8") as file:
        extracted_data = json.load(file)
except (IOError, json.JSONDecodeError) as e:
    print(f"Error loading weapons_and_armors.json: {e}")
    extracted_data = []

# GUI Application
def create_gui():
    selected_items = {"Cierzo": None, "Emercar": None, "Moonsoon": None, "Levant": None}

    def search_items():
        query = search_var.get().lower()
        results = [item for item in extracted_data if query in item["m_name"].lower()]
        results_list.delete(0, tk.END)
        for item in results:
            results_list.insert(tk.END, f"{item['m_name']} (ID: {item['ItemID']})")

    def select_item(label_name):
        selected_index = results_list.curselection()
        if not selected_index:
            messagebox.showerror("Selection Error", "No item selected!")
            return
        selected_text = results_list.get(selected_index)
        item_id = selected_text.split("ID: ")[1][:-1]  # Extract ItemID from the string
        selected_items[label_name] = item_id
        labels[label_name].config(text=f"{label_name}: {selected_text}")

    def export_to_xml():
        root = ET.Element("LegacyChestSave", {
            "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        })
        chest_list = ET.SubElement(root, "LegacyChestList")

        mapping = {
            "Cierzo": "Chersonese_Dungeon8",
            "Emercar": "EmercarDungeonsSmall",
            "Moonsoon": "Hallowed_Dungeon5",
            "Levant": "Abrassar_Dungeon3"
        }
        identifiers = {
            "Cierzo": "x3IKXVgO4UelahGzFRJDXw",
            "Emercar": "5DyToBXtuE2Q-58tDP9U6Q",
            "Moonsoon": "cgLEtE9XI0qg8yMj_lI3zw",
            "Levant": "4jgUGOcE4kSC39l_xjJ_PQ"
        }

        for label, id_value in selected_items.items():
            if id_value is None:
                # Skip creating an entry for this label if no item is selected
                continue

            basic_save = ET.SubElement(chest_list, "BasicSaveData")
            ET.SubElement(basic_save, "Identifier", {"xsi:type": "xsd:string"}).text = identifiers[label]
            ET.SubElement(basic_save, "SyncData").text = f"{mapping[label]}~{id_value}~~~0"

        # Format the XML with proper indentation
        xml_str = ET.tostring(root, encoding="utf-8")
        parsed_xml = minidom.parseString(xml_str)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")

        try:
            # Save the XML file
            with open("legacy_chest_save.xml", "w", encoding="utf-8") as xml_file:
                xml_file.write(pretty_xml)

            # Compress the XML file using GZIP and save as LegacyChests.defedc
            with open("legacy_chest_save.xml", "rb") as xml_file:
                with gzip.open("LegacyChests.defedc", "wb") as compressed_file:
                    compressed_file.writelines(xml_file)

            messagebox.showinfo("Success", "Exported and compressed to LegacyChests.defedc")
        except IOError as e:
            messagebox.showerror("File Error", f"Error during file export: {e}")



    # Create main window
    root = tk.Tk()
    root.title("Weapon and Armor Selector")

    # Search bar
    search_var = tk.StringVar()
    tk.Label(root, text="Search:").pack()
    search_entry = tk.Entry(root, textvariable=search_var)
    search_entry.pack()
    tk.Button(root, text="Search", command=search_items).pack()

    # Results list
    results_list = tk.Listbox(root, width=50, height=15)
    results_list.pack()

    # Selection buttons
    frame = tk.Frame(root)
    frame.pack()

    labels = {}
    for label_name in ["Cierzo", "Emercar", "Moonsoon", "Levant"]:
        tk.Label(frame, text=label_name + ":").grid(row=0, column=["Cierzo", "Emercar", "Moonsoon", "Levant"].index(label_name))
        labels[label_name] = tk.Label(frame, text=f"{label_name}: None")
        labels[label_name].grid(row=1, column=["Cierzo", "Emercar", "Moonsoon", "Levant"].index(label_name))
        tk.Button(frame, text=f"Select {label_name}", command=lambda l=label_name: select_item(l)).grid(row=2, column=["Cierzo", "Emercar", "Moonsoon", "Levant"].index(label_name))

    # Export button
    tk.Button(root, text="Export to XML and defedc", command=export_to_xml).pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()
