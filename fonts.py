import pygame

fonts_in_system = pygame.font.get_default_font()


font_name = []

for font in fonts_in_system:
    font_name.append(font)
    sysFont = ''.join(map(str,font_name))
print(sysFont)