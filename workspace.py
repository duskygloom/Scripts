#!/usr/bin/python3

import sys
import json
import subprocess

def get_workspaces():
    workspace_raw = subprocess.run(["swaymsg", "--raw", "-t", "get_workspaces"], stdout=subprocess.PIPE)
    return json.loads(workspace_raw.stdout)

def get_nearby_workspaces():
    nearby = {"prev": None, "curr": None, "next": None}
    workspaces = get_workspaces()
    for i in range(len(workspaces)):
        if workspaces[i]["focused"]:
            nearby["curr"] = workspaces[i]
            if i > 0:
                nearby["prev"] = workspaces[i-1]
            if i < len(workspaces)-1:
                nearby["next"] = workspaces[i+1]
    return nearby

def next_workspace():
    subprocess.run(["swaymsg", "workspace next"])
    
def prev_workspace():
    subprocess.run(["swaymsg", "workspace prev"])
    

def print_help():
    print("Workspace switching script using swaymsg.")
    print()
    print("Options:")
    for option in options:
        print(f"{option:<10} {options[option][1]}")

options = {
    "next": (next_workspace, "Switches to the next workspace."),
    "prev": (prev_workspace, "Switches to the previous workspace."),
    "--help": (print_help, "Prints this message.")
}
        
def main():
    if len(sys.argv) > 1 and sys.argv[1] in options:
        options[sys.argv[1]][0]()
    else:
        print_help()
        

if __name__ == "__main__":
    main()
    


