import pygame
import random
import os
import time
from datetime import datetime

# folder = same folder as the code
image_folder = "."

# initialize pygame
pygame.init()
font = pygame.font.Font(None, 245)  # for the clock

# full screen mode
scrn = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = scrn.get_size()

# show boot image for 5 seconds
bootimg = pygame.image.load("giggleOS.webp")
bootimg = pygame.transform.scale(bootimg, (screen_width, screen_height))
scrn.blit(bootimg, (0, 0))
pygame.display.flip()
time.sleep(5)

pygame.display.set_caption('h')

current_image_surface = None
current_image_pos = (0, 0)

# get list of images from current folder (excluding the boot image)
images = [f for f in os.listdir(image_folder) if f.lower().endswith((".png", ".jpg", ".jpeg")) and f != "giggleOS.webp"]

if not images:
    print("No images found in the current folder!")
    pygame.quit()
    exit()

def show_random_image():
    """Load, zoom if possible, and prepare a random image without flipping display."""
    global current_image_surface, current_image_pos

    chosen_image = random.choice(images)
    img_path = os.path.join(image_folder, chosen_image)

    try:
        imp = pygame.image.load(img_path).convert()
    except pygame.error:
        print(f"Could not load {chosen_image}, skipping...")
        return

    img_width, img_height = imp.get_size()

    # Zoom factor (but keep aspect ratio)
    zoom_factor = 1.5
    new_width = int(img_width * zoom_factor)
    new_height = int(img_height * zoom_factor)

    # If new size is too big, scale down to fit screen
    if new_width > screen_width or new_height > screen_height:
        scale_factor = min(screen_width / img_width, screen_height / img_height)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

    # Only scale if scaling won't hurt quality
    if img_width < screen_width and img_height < screen_height:
        imp = pygame.transform.smoothscale(imp, (new_width, new_height))

    # Center image
    x_pos = (screen_width - imp.get_width()) // 2
    y_pos = (screen_height - imp.get_height()) // 2

    # Save image and position for later blitting in main loop
    current_image_surface = imp
    current_image_pos = (x_pos, y_pos)

# show first image
show_random_image()
last_change = time.time()

status = True
while status:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False
        elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
            status = False

    # change image every 5 seconds
    if time.time() - last_change >= 5:
        show_random_image()
        last_change = time.time()

    # draw current image
    if current_image_surface:
        scrn.fill((0, 0, 0))
        scrn.blit(current_image_surface, current_image_pos)

    # draw live clock in top-right corner (12-hour format)
    current_time = datetime.now().strftime("%I:%M %p")  # 12-hour format with AM/PM
    time_surface = font.render(current_time, True, (255, 255, 255))
    scrn.blit(time_surface, (screen_width - time_surface.get_width() - 10, 10))

    pygame.display.flip()

pygame.quit()
