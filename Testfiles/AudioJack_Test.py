import pygame
import time
import os

def play_audio(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found! {file_path}")
        return
    
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(1)

if __name__ == "__main__":
    audio_files = {
        "sound1": "Audio/cow.mp3",
        "sound2": "Audio/oof.mp3",
        "sound3": "Audio/villager.mp3"
    }  # Dictionary of sounds
    
    sound_choice = input("Enter sound name to play (sound1, sound2, sound3): ")
    if sound_choice in audio_files:
        play_audio(audio_files[sound_choice])
    else:
        print("Invalid choice.")
