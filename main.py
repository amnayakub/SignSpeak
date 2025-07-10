import pygame
import sys
import urllib.request
import os
import time
import math
import cv2
import numpy as np

# Initialize Pygame
pygame.init()
pygame.font.init()
click_sound = pygame.mixer.Sound("click.wav")

# Window settings
WIDTH, HEIGHT = 960, 540
retro_width, retro_height = 670, 440
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SignSpeak 🌸")

# Background image
bg_url = "https://wallpapers.com/images/hd/cute-aesthetic-japanese-pixel-art-q6y02ismgybk67ob.jpg"
bg_path = "background.jpg"
if not os.path.exists(bg_path):
    urllib.request.urlretrieve(bg_url, bg_path)
background = pygame.image.load(bg_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Fonts
custom_font_path = "SUPER-VCR_MONO.ttf"
if not os.path.exists(custom_font_path):
    print("Font file SUPER-VCR_MONO.ttf not found!")
    sys.exit()

emoji_font_path = "EmojiFont.ttf"
if not os.path.exists(emoji_font_path):
    print("Font file EmojiFont.ttf not found!")
    sys.exit()

emoji_font = pygame.font.Font(emoji_font_path, 25)
title_font = pygame.font.Font(custom_font_path, 50)
desc_font = pygame.font.SysFont("Arial Rounded MT Bold", 23)
button_font = pygame.font.Font(custom_font_path, 14)

# Text surfaces
app_title = title_font.render("SignSpeak", True, (21, 67, 96))
app_desc = desc_font.render("Real-time ASL-to-text translator", True, (21, 67, 96))

# Calculate positions
title_x = WIDTH - app_title.get_width() - 30
title_y = 50

desc_x = WIDTH - app_desc.get_width() - 87
desc_y = 110

button_x = WIDTH - 279 
button_y = desc_y + app_desc.get_height() + 53 
button_width = 165
button_height = 40

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_color = (255, 182, 193) 
button_hover_color = (255, 155, 180)
button_text = button_font.render("Get started!", True, (80, 35, 60))
button_shadow = button_font.render("Get started!", True, (255, 200, 210))  

def open_retro_window():
    pygame.display.set_mode((retro_width, retro_height))
    pygame.display.set_caption("🕹️ How SignSpeak Works")

    retro_font = pygame.font.Font(custom_font_path, 12)
    heading_font = pygame.font.Font(custom_font_path, 20)

    bg_color = (31, 20, 41)
    text_color = (255, 240, 245)
    border_color = (255, 102, 178)

    instructions = [
        "    Welcome to SignSpeak!",
        "",
        "  How to use:",
        "     Hold up ASL hand signs in front of your webcam",
        "     We will translate signs into letters",
        "     You can type *anywhere* using Type-Anywhere Mode",
        "",
        "  To continue, press [ENTER]",
        "  To return to the main menu, press [ESC]"
    ]

    running_retro = True
    while running_retro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_retro = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running_retro = False
                elif event.key == pygame.K_RETURN:
                    open_webcam()
                    # 🪄 After webcam closes, restore retro window
                    pygame.display.set_mode((retro_width, retro_height))
                    pygame.display.set_caption("🕹️ How SignSpeak Works")

        screen.fill(bg_color)
        pygame.draw.rect(screen, border_color, screen.get_rect(), 5)
        emoji_symbol = emoji_font.render("QG", True, text_color)
        screen.blit(emoji_symbol, (52, 60))

        y_offset = 60
        for i, line in enumerate(instructions):
            font_to_use = heading_font if i == 0 else retro_font
            text_surface = font_to_use.render(line, True, text_color)
            screen.blit(text_surface, (40, y_offset))
            y_offset += 38

        pygame.display.update()

    # ✅ Clean exit to main menu
    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SignSpeak 🌸")


def open_webcam():
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Could not open webcam.")
        return "error"

    CAM_W, CAM_H = 500, 500
    pygame.display.set_mode((CAM_W, CAM_H))
    pygame.display.set_caption("webcam.exe")

    title_font = pygame.font.Font(custom_font_path, 16)
    title_text = title_font.render("webcam.exe", True, (255, 255, 255))

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (CAM_W, CAM_H))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.flip(frame, axis=1))
        screen.blit(frame_surface, (0, 0))

        border_color = (245, 175, 200)     
        inner_border_color = (30, 30, 80)   
        title_bar_color = (255, 160, 190)

        pygame.draw.rect(screen, border_color, (0, 0, CAM_W, CAM_H), width=6)
        pygame.draw.rect(screen, inner_border_color, (6, 10, CAM_W - 12, CAM_H - 12), width=4)
        pygame.draw.rect(screen, title_bar_color, (0, 0, CAM_W, 30))
        screen.blit(title_text, (10, 6))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                cam.release()
                return "back_to_retro"
            elif event.type == pygame.QUIT:
                cam.release()
                pygame.quit()
                sys.exit()

# Main game loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    screen.blit(background, (0, 0))

    # Draw heading and description
    screen.blit(app_title, (title_x, title_y))
    screen.blit(app_desc, (desc_x, desc_y))

    is_hover = button_rect.collidepoint(mouse_pos)
    is_pressed = is_hover and mouse_click[0]

    base_shadow = (180, 130, 150)
    key_top = (255, 182, 193)
    key_face_hover = (255, 200, 210)
    key_face_click = (240, 160, 180)

    offset = 3 if is_pressed else 0

    pygame.draw.rect(screen, base_shadow, button_rect.move(3, 3), border_radius=6)

    face_color = key_face_click if is_pressed else (key_face_hover if is_hover else key_top)
    pygame.draw.rect(screen, face_color, button_rect.move(0, offset), border_radius=6)

    pygame.draw.rect(screen, (90, 60, 80), button_rect.move(0, offset), 2, border_radius=6)

    text_x = button_rect.x + 20
    text_y = button_rect.y + 8 + offset

    if not is_pressed:
        screen.blit(button_shadow, (text_x + 2, text_y + 2))
        screen.blit(button_text, (text_x, text_y))

    button_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_clicked = True

    if button_clicked:
        pygame.draw.rect(screen, (200, 100, 120), button_rect.move(0, offset + 2), border_radius=6)
        pygame.draw.rect(screen, (90, 60, 80), button_rect.move(0, offset + 2), 2, border_radius=6)

        button_shadow_pressed = button_font.render("Get started!", True, (150, 90, 110))
        screen.blit(button_shadow_pressed, (text_x + 2, text_y + 4))
        screen.blit(button_text, (text_x, text_y + 2))

        pygame.display.update()
        click_sound.play()
        pygame.time.wait(120)

        open_retro_window() 
        button_clicked = False  

    pygame.display.update()

pygame.quit()
sys.exit()