from gpiozero import DigitalOutputDevice
from time import sleep, time

# Setup pins
DIR = DigitalOutputDevice(27)   # GPIO27 for direction
STEP = DigitalOutputDevice(17)  # GPIO17 for step

# Wake up the driver (SLP and RST must be wired HIGH externally or tied together to 3.3V)
DIR.on()  # or DIR.off() depending on direction

step_delay = 0.001  # 1 ms delay = ~500 steps/sec

# Step for 5 seconds
start = time()
while time() - start < 5:
    STEP.on()
    sleep(step_delay)
    STEP.off()
    sleep(step_delay)
