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