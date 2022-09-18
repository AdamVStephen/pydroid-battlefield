import os
import pdb
import time
import sys
import pygame
from pygame.locals import *
import pygame
from pygame.locals import *
from pygame import mixer

def register_sound_bites():
    sounds_dir = os.path.join(os.path.abspath('.'), 'sounds')
    all_sounds = {
        'PantherTank': mixer.Sound(os.path.join(sounds_dir, 'PantherTank.wav')),
        'MP40': mixer.Sound(os.path.join(sounds_dir, 'MP40.wav')),
        '6PDR_AntiTankGun': mixer.Sound(os.path.join(sounds_dir, '6PDR_AntiTankGun.wav')),
        'LeeEnfield303': mixer.Sound(os.path.join(sounds_dir, 'LeeEnfield303.wav')),
        'charge': mixer.Sound(os.path.join(sounds_dir, 'Charge.wav')),
        'bang': mixer.Sound(os.path.join(sounds_dir, 'Bang.wav')),
        'kaboom': mixer.Sound(os.path.join(sounds_dir, 'KaBoom.wav')),
        'TheLastPost': mixer.Sound(os.path.join(sounds_dir, 'TheLastPost.wav')),
    }
    return all_sounds

def select_sound(all_sounds):
    msg = """
    Battlefield sound effects (q = quit)
        p = PantherTank
        m = MP40
        a = 6PDR_AntiTankGun
        l = LeeEnfield303
        c = CHARGE!!!! (Derek)
        b = bang! (Derek)
        k = kaboom! (Dad)
        r = TheLastPost (rememberance)
        
        etc.
    > 
    """
    print(msg)
    controller = assign_hotkeys(sounds)
    pygame.init()
    screen = surface = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    surfrect = surface.get_rect()
    rect = pygame.Rect((0, 0), (256, 256))
    rect.center = (surfrect.w / 2, surfrect.h / 2)
    # defining a font
    smallfont = pygame.font.SysFont('Corbel', 35)
    # white color
    color = (255, 255, 255)
    # light shade of the button
    color_light = (170, 170, 170)
    # dark shade of the button
    color_dark = (100, 100, 100)
    width = screen.get_width()
    height = screen.get_height()
    text = smallfont.render('quit', True, color)
    touched = False
    mixer.init()
    mixer.music.set_volume(0.7)
    mixer.set_num_channels(10)

    while True:
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pygame.quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
                    pygame.quit()
                if rect.collidepoint(ev.pos):
                    touched = True
                    # This is the starting point
                    pygame.mouse.get_rel()
                    mixer.Channel(0).play(mixer.Sound(sounds['PantherTank']))
                    time.sleep(1)
                    mixer.Channel(1).play(mixer.Sound(sounds['kaboom']))
            elif ev.type == pygame.MOUSEBUTTONUP:
                touched = False
        clock.tick(60)
        surface.fill((0, 0, 0))
        if touched:
            rect.move_ip(pygame.mouse.get_rel())
            rect.clamp_ip(surfrect)
        surface.fill((255, 100, 255), rect)
        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        # if mouse is hovered on a button it
        # changes to lighter shade
        if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])
        else:
            pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])

        # superimposing the text onto our button
        screen.blit(text, (width / 2 + 50, height / 2))
        pygame.display.flip()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mixer.init()
    sounds = register_sound_bites()
    select_sound(sounds)
