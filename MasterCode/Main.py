import time
import pygame
import threading
from Monitor import Monitor
from Graphics import Graphics
from Ethernet_Thread import Ethernet_Thread
from GPIO_thread import GPIO_thread

def handle_events(graphics, monitor, gpio_thread, ethernet_thread):
    """Handles events from the graphics and GPIO threads."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            graphics.stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_0:
                graphics.stop()
                gpio_thread.stop()
                ethernet_thread.stop()
            elif event.key == pygame.K_RIGHT:
                monitor.nextQandA()  # Move to the next question
            elif event.key == pygame.K_g:
                monitor.try_send_to_robot(10)  # Send the integer 10 to the robot

def main():
    condition = threading.Condition()
    monitor = Monitor(condition)

    graphics = Graphics(monitor)  # Now runs in main thread

    # Threads for other components
    
    gpio_thread = GPIO_thread(monitor)
    ethernet_thread = Ethernet_Thread(monitor, condition, gpio_thread)

    
    gpio_thread.start()
    ethernet_thread.start()

    while graphics.running:
        graphics.render()                # Drawing + LCD
        handle_events(graphics, monitor, gpio_thread, ethernet_thread)  # Event handling
        time.sleep(0.01)                 # Light sleep to reduce CPU load

    # Wait for threads to finish
    ethernet_thread.join()
    gpio_thread.join()

    print("Main thread exiting")

if __name__ == "__main__":
    main()
