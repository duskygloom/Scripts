#!/usr/bin/python3

import re
import sys
import subprocess
from typing import Literal
from functools import partial

device_t = Literal["source", "sink"]


def set_volume(device: device_t, value: int):
    subprocess.run(["pactl", f"set-{device}-volume", f"@DEFAULT_{device.upper()}@", f"{value}%"])
    print(value)

def get_volume(device: device_t) -> int:
    output = subprocess.run(["pactl", f"get-{device}-volume", f"@DEFAULT_{device.upper()}@"], stdout=subprocess.PIPE, text=True).stdout
    matches = re.compile(r"\S\d*%").findall(output)
    if len(matches) == 0:
        return 0
    elif device == "source":
        return int(matches[0].rstrip("%"))
    else:
        return int(matches[0].rstrip("%"))

def set_mute(device: device_t, value: int):
    subprocess.run(["pactl", f"set-{device}-mute", f"@DEFAULT_{device.upper()}@", str(value)])
    print((not value) * get_volume(device))

def is_mute(device: device_t) -> int:
    output = subprocess.run(["pactl", f"get-{device}-mute", f"@DEFAULT_{device.upper()}@"], stdout=subprocess.PIPE, text=True).stdout
    return int(output.rstrip().endswith("yes"))


def toggle_input_mute():
    set_mute("source", not is_mute("source"))

def toggle_output_mute():
    set_mute("sink", not is_mute("sink"))

def increase_volume(device: device_t):
    if is_mute(device):
        set_mute(0)
    volume = get_volume(device)
    if volume+5 <= 200:
        set_volume(device, volume+5)
    else:
        set_volume(device, 200)

def decrease_volume(device: device_t):
    if is_mute(device):
        return
    volume = get_volume(device)
    if volume-5 >= 0:
        set_volume(device, volume-5)
    else:
        set_volume(device, 0)


def print_help():
    print("Audio control script using pactl.")
    print()
    print("Options:")
    for option in options:
        print(f"{option:<12} {options[option][1]}")

options = {
    "in_mute": (toggle_input_mute, "Toggle default microphone mute."),
    "out_mute": (toggle_output_mute, "Toggle default speaker mute."),
    "in_plus": (partial(increase_volume, "source"), "+5% default microphone volume."),
    "in_minus": (partial(decrease_volume, "source"), "-5% default microphone volume."),
    "out_plus": (partial(increase_volume, "sink"), "+5% default speaker volume."),
    "out_minus": (partial(decrease_volume, "sink"), "-5% default speaker volume."),
    "--help": (print_help, "Prints this message.")
}

def main():
    if len(sys.argv) > 1 and sys.argv[1] in options:
        options[sys.argv[1]][0]()
    else:
        print_help()


if __name__ == "__main__":
    main()

