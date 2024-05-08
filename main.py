import os
import pygame
import random
import importlib
import platform
import subprocess


def import_random_art():
    # Path to the 'resources' submodule, adjust as necessary
    resources_dir = os.path.join(os.path.dirname(__file__), 'art')

    # List all Python files in the 'resources' directory
    files = [f[:-3] for f in os.listdir(resources_dir) if f.endswith('.py') and not f.startswith('__')]

    # Choose a random file from the list
    random_file = random.choice(files)

    # Import the module dynamically
    module = importlib.import_module(f"art.{random_file}")

    # Access the ART attribute from the imported module
    art = getattr(module, 'ART', None)

    return art


def get_os():
    return platform.system()


def set_max_volume(os_type):
    try:
        if os_type == "Linux":
            # Command for Linux to set volume to 100%
            # Checks for PulseAudio or ALSA and uses the appropriate tool
            command = '''
            if command -v pactl >/dev/null 2>&1; then
                pactl set-sink-volume @DEFAULT_SINK@ 100%
            elif command -v amixer >/dev/null 2>&1; then
                amixer sset Master 100%
            else
                echo "No known audio control utility found."
            fi
            '''
            subprocess.run(command, shell=True, executable='/bin/bash')

        elif os_type == "Windows":
            # Command for Windows to set volume to 100%
            # Simulates pressing the "volume up" key several times
            command = '''
            for ($i=0; $i -lt 20; $i++) {
                (New-Object -ComObject WScript.Shell).SendKeys([char]175)
            }
            '''
            subprocess.run(["powershell", "-Command", command], shell=True)

    except Exception as e:
        print(f"Failed to set volume: {e}")


def play_song_at_max_volume(song_path):
    os_type = get_os()
    set_max_volume(os_type)

    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the song
    pygame.mixer.music.load(song_path)
    # Set the volume to maximum
    pygame.mixer.music.set_volume(1.0)  # Volume range is from 0.0 to 1.0
    # Start playing the song
    pygame.mixer.music.play()

    # Keep the program running and playing the song
    try:
        while True:
            # Check if the music stream is playing
            if not pygame.mixer.music.get_busy():
                # If the music is done playing, break the loop
                break
    except KeyboardInterrupt:
        # Stop the music if the user interrupts the program (e.g., with Ctrl+C)
        pygame.mixer.music.stop()
        print("Music playback stopped.")


def print_ascii_art():
    art = import_random_art()

    print(art)


if __name__ == "__main__":
    print_ascii_art()
    play_song_at_max_volume(os.path.join('resources','MARCHA.mp3'))
