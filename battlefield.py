import os
import pdb
import time
import sys
import pygame
from pygame.locals import *
import pygame
from pygame.locals import *
from pygame import mixer
from collections import OrderedDict

BattleFieldDefinitions = [
    ['PantherTank', 'p', 'PantherTank.wav'],
    ['MP40', 'm', 'MP40.wav'],
    ['6PDR_AntiTankGun', 'a', '6PDR_AntiTankGun.wav'],
    ['LeeEnfield303', 'l', 'LeeEnfield303.wav'],
    ['CHARGE !!!', 'c',   'Charge.wav'],
    ['Bang!', 'b',  'Bang.wav'],
    ['Kaboom!', 'k', 'KaBoom.wav'],
    ['The Last Post', 't',  None],
    ['Quit', 'q', None]
]

WHITE = (255, 255, 255)
BLACK = (0,0,0)
# light shade of the button
LIGHT = (170, 170, 170)
# dark shade of the button
DARK = (100, 100, 100)
FONT_FOREGROUND = (50,50,255)

class BattleFieldElement:

    sounds_dir = os.path.join(os.path.abspath('.'), 'sounds')
    n_of_sounds = 0

    def __init__(self, description, key, filename, label_text = None, colour = LIGHT, logfh = None):
        BattleFieldElement.n_of_sounds+=1
        self.logfh = logfh
        self.channel = BattleFieldElement.n_of_sounds
        self.description = description
        self.key = key
        self.label_text = label_text
        self.sound = None
        if filename is None:
            self.filename = "None"
            self.filepath = "None"
        else:
            self.filepath = filepath = os.path.join(self.sounds_dir, filename)
            if os.path.exists(filepath):
                self.sound = mixer.Sound(filepath)
        self.active = False
        self.button = None

    def log(self, line):
        if self.logfh is not None:
            self.logfh.write(f"{line}\n")
            self.logfh.flush()

    def register_button(self, button, text):
        """
        Connect the element to a UI button
        """
        self.button = button
        self.text = text

    def toggle_sound(self):
        if self.sound is None:
            self.log(f"Toggle. No sound for {self.text}")
            if self.text == "Quit":
                self.log(f"Quitting")
                pygame.quit()
                sys.exit(0)
            return
        if self.active:
            self.stopped = self.started - time.time()
            self.log(f"Toggle OFF for {self.text} after {self.stopped}")
            self.active = False
            mixer.Channel(self.channel).pause()
        else:
            self.started = time.time()
            self.log(f"Toggle ON for {self.text} at {self.started}")
            self.active = True
            mixer.Channel(self.channel).play(self.sound)

    def __repr__(self):
        return f"BattleFieldSound {self.key} = {self.description} on channel {self.channel}"


class GUI:
    """
    Container for the pygame geometry
    """
    def __init__(self, definitions = BattleFieldDefinitions, logfh = None):
        self.logfh = logfh
        self.log("GUI init 3.14159")
        self.setup()
        self.elements = OrderedDict()
        for (description, key, filename) in definitions:
            self.elements[description] = BattleFieldElement(description, key, filename, logfh = logfh)
        self.n_elements = len(self.elements)
        mixer.set_num_channels(self.n_elements)
        self.compute_geometry()

    def log(self, line):
        if self.logfh is not None:
            self.logfh.write(f"{line}\n")
            self.logfh.flush()

    def setup(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.width = 640
        self.height = 480
        #self.screen = screen = pygame.display.set_mode((self.width, self.height), flags = pygame.SCALED)
        self.screen = screen = pygame.display.set_mode((0,0))
        self.desktop_sizes = pygame.display.get_desktop_sizes()
        (self.width, self.height) = self.desktop_sizes[0]
        self.log(f"{self.desktop_sizes} desktops of which first is {self.width} x {self.height}")
        screen.fill(BLACK)
        self.smallfont = pygame.font.SysFont('Corbel', 140)
        mixer.init()
        mixer.music.set_volume(0.7)

    def compute_geometry(self, h_margin_pc=5, v_margin_pc=2.5):
        """
        Simple layout of one button per sound.
        Labels are pygame.Rect(angles) (left, top), (width, height)
        """
        self.h_margin = (h_margin_pc * 0.01 * self.width) / 2
        self.v_margin = (v_margin_pc * 0.01 * self.height) / 2
        self.label_height = label_height = (self.height - (2 * self.v_margin) - (self.n_elements * self.v_margin)) / (1 + self.n_elements)
        self.label_width = label_width = self.width - (2 * self.h_margin)
        self.buttons = OrderedDict()
        for (label, element) in self.elements.items():
            idx = element.channel
            left = self.h_margin
            top = self.v_margin + (idx - 1) * (label_height + self.v_margin)
            button = pygame.Rect( (left, top), (label_width, label_height) )
            self.log(f"button of size {label_width} x {label_height} at {left} {top}")
            text = self.smallfont.render(label, True, FONT_FOREGROUND)
            (text_width, text_height) = text.get_size()
            self.log(f"label {label} of size {text_width} x {text_height}")
            element.register_button(button, label)
            self.screen.fill(LIGHT, button)
            left_offset = (self.width - text_width)/2
            top_offset = (text_height - self.v_margin/2)
            self.log(f"text {label} at {left_offset} {top} {top_offset} \n")
            self.screen.blit(text, (left_offset, top + top_offset))

    def run(self):
        """Main event loop including logic"""
        while True:
            for ev in pygame.event.get():
                if ev.type == QUIT:
                    pygame.quit()
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for (label, element) in self.elements.items():
                        if element.button.collidepoint(ev.pos):
                            element.toggle_sound()
            self.clock.tick(10)
            #time.sleep(1)

            # if mouse is hovered on a button it
            # changes to lighter shade
            #if width / 2 <= mouse[0] <= width / 2 + 140 and height / 2 <= mouse[1] <= height / 2 + 40:
            #    pygame.draw.rect(screen, color_light, [width / 2, height / 2, 140, 40])
            #else:
            #    pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 140, 40])
            # superimposing the text onto our button
            pygame.display.flip()

    def draw(self):
        """
        Update the screen.
        """
        pass

    def __repr__(self):
        r = []
        r.append("UI: WIP")
        for s in self.sounds:
            r.append(f"{s}")

def main():
    with open("./battlefield.log", "w") as logfh:
        gui = GUI(logfh = logfh)
        gui.run()

if __name__ == '__main__':
    main()
