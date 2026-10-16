import pygame
import defining


pygame.init() # initialization


# game window
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Small Test")


running = True
clock = pygame.time.Clock()


# things
info_text = defining.make_text("Good morning!", (SCREEN_WIDTH // 2), 20)
button = defining.make_rect(0, 0, 100, 50, "Click me!")
button["rect"].center = screen.get_rect().center
button["text center"].center = screen.get_rect().center
player = defining.make_rect(175, 175, 50, 50, "")


gamestate = 0

while running:
    screen.fill((0, 0, 0))


    if gamestate >= 1:
        screen.blit(info_text["text"], info_text["text rect"]) # text


        match gamestate:
            case 2:
                info_text["text"] = defining.fontrendering("test")


    defining.movements(player["rect"])


    for event in pygame.event.get(): # event handler
        if event.type == pygame.QUIT: # allows quitting of the window
           running = False

        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left, 2 middle, 3 right
                if player["rect"].collidepoint(event.pos): # collided with mouse. event.pos gets mouse coords
                    color = (255, 0, 255)
                    gamestate += 1

    if player["rect"].collidepoint(mouse_pos): # collided with mouse. event.pos gets mouse coords
        color = (255, 255, 255)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_NO)
    else:
        color = (255, 0, 0)
        pygame.mouse.set_cursor(*pygame.cursors.arrow)
    
    

    pygame.draw.rect(screen, (0, 175, 0), button["rect"], 0) # drawing green button
    screen.blit(button["text"], button["text center"]) # blitting button text
    pygame.draw.rect(screen, color, player["rect"]) # drawing red player
    pygame.display.flip() # always updating
    clock.tick(60) # fps


pygame.quit()