from gpiozero import Button
from signal import pause

# Set up 5 buttons on GPIO pins 17, 18, 27, 22, 23
buttons = [
    Button(17, bounce_time=0.1),
    Button(18, bounce_time=0.1),
    Button(27, bounce_time=0.1),
    Button(22, bounce_time=0.1),
    Button(23, bounce_time=0.1)
]

def make_say_hi(n):
    def say_hi():
        print(f"HI from button {n}")
    return say_hi

# Attach handlers to each button
for i, button in enumerate(buttons):
    button.when_pressed = make_say_hi(i + 1)

pause()
