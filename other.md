# other code blocks i may use


### file management!!
```python
try:
    with open("user\\config.txt") as f:
        print("loaded previous txt file")
except FileNotFoundError: # IF FILE NOT FOUND / NOT THERE
    with open("user\\config.txt", "w") as f:
        print("opened new txt file")

with open("user\\config.txt") as f:
    contents = f.read()

    if username in contents: # FINDING STRINGS WITHIN FILE
        print(f"found {username}")
    else:
        print(f"did not find ")


configtxt = open("user\\test.txt", "x") # ADDING NEW TXT FILES
os.remove("user\\test.txt") # REMOVING TXT FILES
```

settings:
* having a checkmark button that can be toggled on / off
- * this will then activate a one-time thing that turns that selected thing into reality

what i want in the settings:
### --- video & audio --- ###
[ ] fullscreen? (y/n) [auto on yes]
[ ] aspect ratio (selection of presets) [only available on no fullscreen, just grayed out]
[ ] sound slider

### --- gameplay --- ###
[ ] amount of tiles [2 text boxes separated by an 'x'] (num rows by num columns)
[ ] controls (for clicking tile, placing a flag, reseting board)
[ ] free blank tile (symbol on random blank tile so you don't have to guess where to click first)
[ ] score streak (y/n) [auto on yes]

### --- visual/misc --- ###
[ ] face skins (normal, weird, classic)
[ ] tile skins (normal, low qual, classic)
[ ] bg color (enter in RGB values lmao, 3 input boxes separated by commas and inside parenthesis)
[ ] reset all settings and data to nothing (sadness)