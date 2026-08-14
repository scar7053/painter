import pygame
import colorsys
from tkinter import messagebox
pygame.init()

HELP_TEXT = """
Made with ❤ by scar1405
github.com/scar1405/painter

H = Open this help window

P = Export

Z = Draw
Ctrl + Z = Undo

A = Decrease color
Q = Increase color

S = Decrease saturation
W = Increase saturation

D = Decrease brightness
E = Increase brightness

F = Decrease width
R = Decrease width
V = Reset width to default
"""

WIDTH,HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Painter")
clock = pygame.time.Clock()

drawing = []

color = [0,100,100] # in hsv
draw_width = 10

font = pygame.font.Font(None, 20)
open_help_text = font.render("Press H for Help", True, (0,0,0))

def color_rgb():
    # normalize hsv to 0.0 - 1.0
    h_norm = color[0] / 360.0
    s_norm = color[1] / 100.0
    v_norm = color[2] / 100.0
    
    # colorsys returns floats from 0.0 to 1.0
    r, g, b = colorsys.hsv_to_rgb(h_norm, s_norm, v_norm)
    
    # scale it up to bytes
    return (int(r * 255), int(g * 255), int(b * 255))

screenshot_mode = False
currently_drawing = False
current_segment = []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if len(drawing) > 0:
                        del drawing[-1]
                else:
                    currently_drawing = True
                    current_segment = []
                    current_segment.append(color_rgb())
                    current_segment.append(draw_width)
                    current_segment.append([])
            if event.key == pygame.K_v:
                draw_width = 10
            if event.key == pygame.K_h:
                messagebox.showinfo("Painter Help", HELP_TEXT)
            if event.key == pygame.K_p:
                screenshot_mode = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                currently_drawing = False
                drawing.append(current_segment)
    
    if not currently_drawing:
        clock.tick(60)
    
    screen.fill((255,255,255))

    if not screenshot_mode:
        pygame.draw.circle(screen, color_rgb(), pygame.mouse.get_pos(), draw_width)

        pygame.draw.rect(screen, color_rgb(), pygame.rect.Rect(0, HEIGHT-20, WIDTH, 20))
        screen.blit(open_help_text, (WIDTH // 2 - (open_help_text.get_width()//2), HEIGHT-15))
    for segment in drawing:
        pygame.draw.lines(screen, segment[0], False, segment[2], segment[1])
    if screenshot_mode:
        pygame.image.save(screen, "export.png")
        screenshot_mode = False

    pressed = pygame.key.get_pressed()

    if currently_drawing:
        if len(current_segment[2]) != 0:
            if (pos := pygame.mouse.get_pos()) != current_segment[2][-1]:
                current_segment[2].append(pos)
                continue
        current_segment[2].append(pygame.mouse.get_pos())

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