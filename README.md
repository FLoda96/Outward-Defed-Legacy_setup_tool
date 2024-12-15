# Outward-Defed-Legacy_setup_tool
A tool to create a custom legacy for your Outward Character

How to use this tool :
- Install Python : https://www.python.org/downloads/
- Run "Generate_Legacy.py" (with a double click)
- You should see an interface with a search bar, search there for the item you want to put into legacy, the search is by name and you have to click the button to refresh the searched items
- Once you see the item you want, select it and then click on the "Select Cierzo/Emercar/Moonsoon/Levant" based on which legacy chest you want the item to be
- Once finished (you don't need to fill all the chests) click to "Export to Xml and defedc"
- You'll get a "LegacyChests.defedc" file that you have to put under "<SteamPath>\steamapps\common\Outward\Outward_Defed\SaveGames\<randomic_number>\Save_<randomic_number>\<randomic number with the latest modified date>" and overwrite the previous file, you can do this directly on the caracter you want to play, no need to create another to then set it as legacy
- Enjoy ;)

If you are playing with Mods and you want to have access to items from mods you have to run the "Parse_Mods_Items.py" from the folder of your profile "OutwardDe\profiles\<Profile_Name>", you can access that with the "Browse Profile Folder" option on R2ModMan
- Paste the "Parse_Mods_Items.py" and "weapons_and_armors.json" into the profile folder
- Run "Parse_Mods_Items.py"
- You should see that now the weapons and armors from your mods are inside the "weapons_and_armors.json"
- Overwrite the "weapons_and_armors.json" on the folder where you use "Generate_Legacy.py" and follow the normal steps, now you can also select the items from the mods on your profile, note that i only parse for the "Weapon" and "Equipment" Tags, in that list there could also be objects not intended for use by the player