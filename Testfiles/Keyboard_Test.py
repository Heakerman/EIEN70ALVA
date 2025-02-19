import keyboard

counter = 0

def on_key_event(event):
    global counter
    if event.name == "num 2":
        counter += 1
        print(f"Counter: {counter}")
    elif event.name == "num 1":
        counter -= 1
        print(f"Counter: {counter}")

print("Press Numpad 2 to count up, Numpad 1 to count down. Press Ctrl+C to exit.")
keyboard.hook(on_key_event)

try:
    keyboard.wait("esc")  # Wait until ESC is pressed to exit
except KeyboardInterrupt:
    print("\nExiting...")
