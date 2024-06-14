#!/usr/bin/python3

import sys
import subprocess


def pause_music():
    subprocess.run(["playerctl", "pause"])

def resume_music():
    subprocess.run(["playerctl", "play"])

def toggle_music():
    subprocess.run(["playerctl", "play-pause"])

def next_music():
    subprocess.run(["playerctl", "next"])

def prev_music():
    subprocess.run(["playerctl", "previous"])


options = {
    "pause": (pause_music, "Pauses music playback."),
    "resume": (resume_music, "Resumes music playback."),
    "toggle": (toggle_music, "Toggle music playback status."),
    "next": (next_music, "Plays the next music in queue."),
    "prev": (prev_music, "Plays the previous music in queue.")
}

def print_help():
    print("Music playback control script using playerctl.")
    print()
    print("Options:");
    for option in options:
        print(f"{option:<10} {options[option][1]}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in options:
        options[sys.argv[1]][0]()
    else:
        print_help()

if __name__ == "__main__":
    main()

