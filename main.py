import pygame
import colorsys
from tkinter import messagebox
from pathlib import Path
import sys, os
pygame.init()

HELP_TEXT = """
Made with ❤ by scar7053
github.com/scar7053/painter

H = Open this help window

P = Export

Z / Left Click = Draw
Ctrl + Z = Undo

L = Toggle low detail mode

A = Decrease color
Q = Increase color

S = Decrease saturation
W = Increase saturation

D = Decrease brightness
E = Increase brightness

F = Decrease width
R = Increase width
V = Reset width to default

G = Decrease transparency
T = Increase transparency
"""

WIDTH,HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Painter")
clock = pygame.time.Clock()

def file_path():
    try:
        path = sys._MEIPASS # pyinstaller detected!
        path = Path(sys.executable).parent # set path to the .exe's folder
    except AttributeError:
        path = os.path.abspath(".")

    return path

drawing = []

color = [0,100,100,100] # in hsv, alpha
draw_width = 10

font = pygame.font.Font(None, 20)
open_help_text = font.render("Press H for Help", True, (0,0,0))

def color_rgba():
    # normalize hsv to 0.0 - 1.0
    h_norm = color[0] / 360.0
    s_norm = color[1] / 100.0
    v_norm = color[2] / 100.0
    
    # colorsys returns floats from 0.0 to 1.0
    r, g, b = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)
    
    # scale it up to bytes, and alpha
    return (int(r * 255), int(g * 255), int(b * 255), color[3])

screenshot_mode = False
low_performance = False
currently_drawing = False
current_segment = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                currently_drawing = True
                current_segment = []
                current_segment.append(color_rgba())
                current_segment.append(draw_width)
                current_segment.append([])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if len(drawing) > 0:
                        del drawing[-1]
                else:
                    currently_drawing = True
                    current_segment = []
                    current_segment.append(color_rgba())
                    current_segment.append(draw_width)
                    current_segment.append([])
            if event.key == pygame.K_v:
                draw_width = 10
            if event.key == pygame.K_h:
                messagebox.showinfo("Painter Help", HELP_TEXT)
            if event.key == pygame.K_p:
                screenshot_mode = True
            if event.key == pygame.K_l:
                low_performance ^= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                currently_drawing = False
                if not (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    drawing.append(current_segment)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                currently_drawing = False
                drawing.append(current_segment)
    
    if not currently_drawing:
        clock.tick(60)
    
    screen.fill((255,255,255))

    for segment in drawing:
        pygame.draw.lines(screen, segment[0], False, segment[2], segment[1]*2)
        if not low_performance:
            for i in segment[2]:
                pygame.draw.circle(screen, segment[0], i, segment[1])
    if screenshot_mode:
        counter = 1
        filename = f"export_{counter:04d}.png"
        listdir = [
            file.name
            for file
            in Path(file_path()).iterdir()
            if file.is_file()
        ]
        while filename in listdir:
            filename = f"export_{counter:04d}.png"
            counter += 1
        pygame.image.save(
            screen, 
            os.path.join(Path(file_path()), filename))
        screenshot_mode = False

    pressed = pygame.key.get_pressed()

    if currently_drawing:
        if len(current_segment[2]) == 0:
            current_segment[2].append(pygame.mouse.get_pos())
        if (pos := pygame.mouse.get_pos()) != current_segment[2][-1]:
            current_segment[2].append(pos)
        if len(current_segment[2]) >= 2:
            pygame.draw.lines(screen, color_rgba(), False, current_segment[2], draw_width*2)
            if not low_performance:
                for i in current_segment[2]:
                    pygame.draw.circle(screen, current_segment[0], i, current_segment[1])

    if not screenshot_mode:
        pygame.draw.circle(screen, color_rgba(), pygame.mouse.get_pos(), draw_width)

        pygame.draw.rect(screen, color_rgba(), pygame.rect.Rect(0, HEIGHT-20, WIDTH, 20))
        screen.blit(open_help_text, (WIDTH // 2 - (open_help_text.get_width()//2), HEIGHT-15))

    if (colord := pressed[pygame.K_q] - pressed[pygame.K_a]):
        color[0] += colord
        if color[0] < 0:
            color[0] = 0
        elif color[0] > 360:
            color[0] = 360
    if (saturationd := pressed[pygame.K_w] - pressed[pygame.K_s]):
        color[1] += saturationd
        if color[1] < 0:
            color[1] = 0
        elif color[1] > 100:
            color[1] = 100
    if (brightnessd := pressed[pygame.K_e] - pressed[pygame.K_d]):
        color[2] += brightnessd
        if color[2] < 0:
            color[2] = 0
        elif color[2] > 100:
            color[2] = 100
    if (widthd := pressed[pygame.K_r] - pressed[pygame.K_f]):
        draw_width += widthd
        if draw_width < 0:
            draw_width = 0
    #print(color)

    pygame.display.flip()

pygame.quit()