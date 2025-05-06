import time
import pygame
from Monitor import Monitor
from Graphics import Graphics

def handle_events(graphics, monitor):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphics.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_0:
                graphics.stop()
            elif event.key == pygame.K_RIGHT:
                monitor.nextQandA()

def main():
    monitor = Monitor()
    graphics = Graphics(monitor)

    while graphics.running:
        graphics.render()  # Draw the current frame
        handle_events(graphics, monitor)

    print("Main thread exiting")

if __name__ == "__main__":
    main()
