import pygame
import time
import os

def play_audio(file_path): # Function to play audio file
    if not os.path.exists(file_path): # Check if file exists
        print(f"Error: File not found! {file_path}")
        return
    
    pygame.mixer.init() # Initialize the mixer
    pygame.mixer.music.load(file_path) # Load the audio file
    pygame.mixer.music.play() # Play the audio file
    
    while pygame.mixer.music.get_busy(): # Wait for the audio to finish playing
        time.sleep(1)

if __name__ == "__main__": # Main function
    audio_files = { # Dictionary of audio files
        "sound1": "Audio/cow.mp3",
        "sound2": "Audio/oof.mp3",
        "sound3": "Audio/villager.mp3"
    }
    
    sound_choice = input("Enter sound name to play (sound1, sound2, sound3): ") 
    if sound_choice in audio_files:
        play_audio(audio_files[sound_choice])
    else:
        print("Invalid choice.")
