import pygame
import random
import os
import time
from datetime import datetime

image_folder = "."

pygame.init()
font = pygame.font.Font(None, 245)

# Fullscreen mode
scrn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = scrn.get_size()

# Show boot image for 5 seconds
bootimg = pygame.image.load("giggleOS.webp")
bootimg = pygame.transform.smoothscale(bootimg, (screen_width, screen_height))
scrn.blit(bootimg, (0, 0))
pygame.display.flip()
time.sleep(5)

pygame.display.set_caption('h')

current_image_surface = None
current_image_pos = (0, 0)

# Load images from folder excluding boot image
images = [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg")) and f != "giggleOS.webp"]
if not images:
    print("No images found!")
    pygame.quit()
    exit()

def show_random_image():
    global current_image_surface, current_image_pos

    chosen_image = random.choice(images)
    img_path = os.path.join(image_folder, chosen_image)

    try:
        imp = pygame.image.load(img_path).convert()
    except pygame.error:
        print(f"Could not load {chosen_image}, skipping...")
        return

    img_width, img_height = imp.get_size()

    # Calculate scale factor to fill screen without distortion
    scale_factor = max(screen_width / img_width, screen_height / img_height)
    new_width = int(img_width * scale_factor)
    new_height = int(img_height * scale_factor)

    # Smooth scale to new size
    imp = pygame.transform.smoothscale(imp, (new_width, new_height))

    # Center the image
    x_pos = (screen_width - new_width) // 2
    y_pos = (screen_height - new_height) // 2

    current_image_surface = imp
    current_image_pos = (x_pos, y_pos)

# Show first image
show_random_image()
last_change = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Change image every 5 seconds
    if time.time() - last_change >= 5:
        show_random_image()
        last_change = time.time()

    # Draw current image
    if current_image_surface:
        scrn.fill((0, 0, 0))
        scrn.blit(current_image_surface, current_image_pos)

    # Draw 12-hour clock
    current_time = datetime.now().strftime("%I:%M %p")
    time_surface = font.render(current_time, True, (255, 255, 255))
    scrn.blit(time_surface, (screen_width - time_surface.get_width() - 10, 10))

    pygame.display.flip()

pygame.quit()
