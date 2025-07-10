import pygame
import sys
import urllib.request
import os
import time
import math

# Initialize Pygame
pygame.init()
pygame.font.init()
click_sound = pygame.mixer.Sound("click.wav")

# Window settings
WIDTH, HEIGHT = 960, 540
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

button_x = WIDTH - 279  # aligned right with some padding
button_y = desc_y + app_desc.get_height() + 53  # right under the description
button_width = 160
button_height = 40

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_color = (255, 182, 193)  # light pastel pink
button_hover_color = (255, 155, 180)
button_text = button_font.render("Get started!", True, (80, 35, 60))
button_shadow = button_font.render("Get started!", True, (255, 200, 210))  # light pink shadow

# Function to open retro window
def open_retro_window():
    retro_width, retro_height = 640, 400
    retro_screen = pygame.display.set_mode((retro_width, retro_height))
    pygame.display.set_caption("🕹️ Retro Mode")

    retro_font = pygame.font.Font(custom_font_path, 28)
    heading = retro_font.render("Welcome to Retro Mode!", True, (255, 255, 255))

    bg_color = (31, 20, 41)  # Deep purple retro vibe
    border_color = (255, 102, 178)

    running_retro = True
    while running_retro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_retro = False

        retro_screen.fill(bg_color)
        pygame.draw.rect(retro_screen, border_color, retro_screen.get_rect(), 8)

        retro_screen.blit(heading, (retro_width//2 - heading.get_width()//2, 160))
        pygame.display.update()

    pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SignSpeak 🌸")

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

    # --- RETRO KEY BUTTON SECTION STARTS ---
    is_hover = button_rect.collidepoint(mouse_pos)
    is_pressed = is_hover and mouse_click[0]

    # Colors
    base_shadow = (180, 130, 150)
    key_top = (255, 182, 193)
    key_face_hover = (255, 200, 210)
    key_face_click = (240, 160, 180)

    # Button Y offset if pressed
    offset = 3 if is_pressed else 0

    # Draw shadow layer (bottom layer)
    pygame.draw.rect(screen, base_shadow, button_rect.move(3, 3), border_radius=6)

    # Draw button face
    face_color = key_face_click if is_pressed else (key_face_hover if is_hover else key_top)
    pygame.draw.rect(screen, face_color, button_rect.move(0, offset), border_radius=6)

    # Optional border
    pygame.draw.rect(screen, (90, 60, 80), button_rect.move(0, offset), 2, border_radius=6)

    # Update text to match shifted key
    text_x = button_rect.x + 20
    text_y = button_rect.y + 8 + offset

    # Default shadowed text
    if not is_pressed:
        screen.blit(button_shadow, (text_x + 2, text_y + 2))
        screen.blit(button_text, (text_x, text_y))

    # --- Add this before the event loop ---
    button_clicked = False

    # --- Inside event loop ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                button_clicked = True

    # --- After drawing button, add this sink + sound on click ---
    if button_clicked:
        # Deeper sink animation
        pygame.draw.rect(screen, (200, 100, 120), button_rect.move(0, offset + 2), border_radius=6)
        pygame.draw.rect(screen, (90, 60, 80), button_rect.move(0, offset + 2), 2, border_radius=6)

        button_shadow_pressed = button_font.render("Get started!", True, (150, 90, 110))
        screen.blit(button_shadow_pressed, (text_x + 2, text_y + 4))
        screen.blit(button_text, (text_x, text_y + 2))

        pygame.display.update()
        click_sound.play()
        pygame.time.wait(120)

        # open_retro_window()  # Uncomment when you're ready
        button_clicked = False  # Reset click flag

    # --- RETRO KEY BUTTON SECTION ENDS ---


    pygame.display.update()

pygame.quit()
sys.exit()
