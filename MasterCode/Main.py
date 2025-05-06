import time
import pygame
import threading
from Monitor import Monitor
from Graphics import Graphics
#from Ethernet_Thread import Ethernet_Thread
#from GPIO_thread import GPIO_thread


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
    
    monitor = Monitor(condition)  # Initialize the monitor
    graphics = Graphics(monitor)
    #ethernet_thread = Ethernet_Thread(monitor,condition)
    #gpio_thread = GPIO_thread(monitor)

    graphics.start()
    #ethernet_thread.start()
    #gpio_thread.start()

    while graphics.running:
        handle_events(graphics, monitor)  # Handle Pygame events
        time.sleep(0.01)  # Prevents CPU overload

    graphics.join()  # Ensure graphics thread stops before quitting
    #ethernet_thread.join()  # Ensure ethernet thread stops before quitting
    #gpio_thread.join()  # Ensure GPIO thread stops before quitting

    print("Main thread exiting")

if __name__ == "__main__":  
    main()
