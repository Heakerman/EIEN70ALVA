import evdev

# Replace with the correct device path after testing
DEVICE_PATH = "/dev/input/by-id/usb-Logitech_USB_Keyboard-event-kbd"

device = evdev.InputDevice(DEVICE_PATH)
print(f"Listening to {device.name}...")

counter = 0

for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY and event.value == 1:  # Key press event
        key = evdev.ecodes.KEY[event.code]

        if key == "KEY_KP2":  # Numpad 2
            counter += 1
            print(f"Counter: {counter}")
        elif key == "KEY_KP1":  # Numpad 1
            counter -= 1
            print(f"Counter: {counter}")
        elif key == "KEY_ESC":  # Exit on ESC key
            print("Exiting...")
            break
