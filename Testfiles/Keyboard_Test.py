from pynput import keyboard

counter = 0

def on_key_event(key):
    global counter
    try:
        if key.char == "2":  # Check for Numpad 2
            counter += 1
            print(f"Counter: {counter}")
        elif key.char == "1":  # Check for Numpad 1
            counter -= 1
            print(f"Counter: {counter}")
    except AttributeError:
        pass  # Ignore special keys

print("Press Numpad 2 to count up, Numpad 1 to count down. Press ESC to exit.")

with keyboard.Listener(on_press=on_key_event) as listener:
    listener.join()