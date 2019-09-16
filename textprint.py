# TextPrint

import pygame


# This is a simple class that will help us print to the screen
class TextPrint:
    def __init__(self, font_size):
        self.line_height = font_size * 1.1
        self.font = pygame.font.Font("hack-fonts/Hack-Regular.ttf",
                                     int(font_size * 0.8))
        self.fontB = pygame.font.Font("hack-fonts/Hack-Bold.ttf",
                                      font_size)
        self.reset()

    def printS(self, screen, text_color, textString):
        textBitmap = self.font.render(textString, True, text_color)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def printSB(self, screen, text_color, textString):
        textBitmap = self.fontB.render(textString, True, text_color)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = self.line_height / 2
        self.y = self.line_height / 2

    def indent(self):
        self.x += self.line_height * 2

    def unindent(self):
        self.x -= self.line_height * 2

    def move_right(self):
        self.x += self.line_height * 18
        self.y = self.line_height * 1.5
