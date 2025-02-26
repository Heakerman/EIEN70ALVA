import time
import pygame
from Graphics import Graphics

def handle_events(graphics):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphics.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_0:
                graphics.stop()

def main():
    graphics = Graphics()
    graphics.start()

    while graphics.running:
        handle_events(graphics)
        time.sleep(0.01)  # Prevents CPU overload

    graphics.join()  # Ensure graphics thread stops before quitting
    print("Main thread exiting")

if __name__ == "__main__":
    main()
