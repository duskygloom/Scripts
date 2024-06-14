#!/usr/bin/python3

import re
import sys
import subprocess


device = "amdgpu_bl1"
args = ["brightnessctl", "-d", device]

def set_brightness(value: int):
    subprocess.run(args + ["set", f"{value}%"], stdout=subprocess.PIPE)
    print(value)

def nearest_five(n: int) -> int:
    floor_ten = (n // 10) * 10
    if n % 10 < 3:
        return floor_ten
    elif n % 10 < 8:
        return floor_ten + 5
    else:
        return floor_ten + 10

def get_brightness() -> int:
    process = subprocess.run(args + ["get"], stdout=subprocess.PIPE, text=True)
    current = int(process.stdout.strip())
    process = subprocess.run(args + ["max"], stdout=subprocess.PIPE, text=True)
    maximum = int(process.stdout.strip())
    return nearest_five((current * 100) // maximum)


def increase_brightness():
    current = get_brightness()
    if current+5 >= 100:
        set_brightness(100)
    else:
        set_brightness(current+5)

def decrease_brightness():
    current = get_brightness()
    if current-5 <= 0:
        set_brightness(0)
    else:
        set_brightness(current-5)


def print_help():
    print("Brightness control using brightnessctl.")
    print()
    print("Options:")
    for option in options:
        print(f"{option:<12} {options[option][1]}")

options = {
    "plus": (increase_brightness, "+5% brightness."),
    "minus": (decrease_brightness, "-5% brightness."),
    "--help": (print_help, "Prints this message.")
}

def main():
    if len(sys.argv) > 1 and sys.argv[1] in options:
        options[sys.argv[1]][0]()
    else:
        print_help()


if __name__ == "__main__":
    main()

