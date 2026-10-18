# other code blocks i may use

### detecting player.rect if it collides with the mouse_ps

```python
   mouse_pos = pygame.mouse.get_pos()
    if player.rect.collidepoint(mouse_pos): # collided with mouse. event.pos gets mouse coords
        color = (255, 255, 255)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
    else:
        color = (255, 0, 0)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
```

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