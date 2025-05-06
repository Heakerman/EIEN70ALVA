import time
import pygame
import threading
from Monitor import Monitor
from Graphics import Graphics
# from Ethernet_Thread import Ethernet_Thread
# from GPIO_thread import GPIO_thread

def handle_events(graphics, monitor):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphics.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_0:
                graphics.stop()
            elif event.key == pygame.K_RIGHT:
                monitor.nextQandA()  # Move to the next question

def main():
    condition = threading.Condition()
    monitor = Monitor(condition)

    graphics = Graphics(monitor)  # Now runs in main thread

    # Threads for other components
    # ethernet_thread = Ethernet_Thread(monitor, condition)
    # gpio_thread = GPIO_thread(monitor)

    # ethernet_thread.start()
    # gpio_thread.start()

    while graphics.running:
        graphics.render()                # Drawing + LCD
        handle_events(graphics, monitor)  # Event handling
        time.sleep(0.01)                 # Light sleep to reduce CPU load

    # Wait for threads to finish
    # ethernet_thread.join()
    # gpio_thread.join()

    print("Main thread exiting")

if __name__ == "__main__":
    main()
