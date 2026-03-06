# RBXL-to-Polytoria
Converts a .rbxl file or .rbxlx file to .poly (Has to be XML format)

credit to the RTP plugin for some of the code

sorry in advance for messing up the front page even more


Let me know of how I can improve this

# Setup
run `pip install -r requirements.txt` in the directory


# NOTES
this may be buggy. Notify me in the polytoria discord or shoot me a private message on polytoria if you encounter any issues (my polytoria username is humvee)

# Creating a configuration file
This converter has the ability to replace assets with ones you provide in the config file, and also has the ability to do the same with scripts.

To create a configuration file, first create a copy of config-template.json

Next, rename it to whatever you want. After this, open the file in whatever text editor works for you.

Heres a guide for how it should be structured. I added example data to help.

```javascript
{
    "assets": {
        "assetId1": "replacement1",
        "assetId2": "replacement2",
        "assetId3": "replacement3",
        "hash1": "replacement4",
        "hash2": "replacement5",
        "hash3": "replacement6",
    },
    "scriptNames": {
        "hash1": "script1",
        "hash2": "script2",
        "hash3": "script3",
    }
}
```