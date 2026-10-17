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