from gpiozero import Servo
from time import sleep
from servo import Servo

# Initialize the servo on GPIO17
# Adjust min_pulse_width and max_pulse_width if needed to match your servo's range
servo = Servo(17, min_pulse_width=0.0005, max_pulse_width=0.0025)

def grip(duration=0.5):
    print("Gripping...")
    servo.max()  # Rotate to one end
    sleep(duration)
    servo.detach()  # Stop signal to prevent jitter

def release(duration=0.5):
    print("Releasing...")
    servo.min()  # Rotate to the other end
    sleep(duration)
    servo.detach()

# Example usage:
if __name__ == '__main__':
    grip()
    sleep(1)
    release()
