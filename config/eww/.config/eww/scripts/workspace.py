#!/usr/bin/python

import json
import subprocess
import sys


def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)


def names(data):
    return gen_dict_extract(data, "className")


def get_icons(workspace):
    output = ""
    try:
        output = subprocess.check_output(
            ["bspc", "query", "-T", "-d", workspace, "-n", ".window.!hidden"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pass

    icons = {
        "firefox": "󰈹",
        "Alacritty": "",
        "discord": "󰙯",
        "Chromium": "",
        "Emacs": "",
    }

    output = json.loads(output)

    icons = list(map(lambda x: icons.get(x, "?"), names(output)))
    return icons


def selected():
    out = ""
    try:
        out = subprocess.check_output(["bspc", "query", "-D", "-d", "focused", "--names"])\
            .decode("utf-8")\
            .split("\n")[0]
    except subprocess.CalledProcessError:
        pass

    return out


if __name__ == "__main__":
    while True:
        output = ""
        try:
            output = subprocess.check_output(
                ["bspc", "query", "-D", "--names"]).decode("utf-8")
        except subprocess.CalledProcessError:
            pass

        workspaces = output.split("\n")[:-1]

        out_workspaces = []
        selected_workspace = selected()
        for workspace in workspaces:
            icons = get_icons(workspace)
            out_workspaces.append({
                "name": workspace,
                "icons": icons,
                "selected": workspace == selected_workspace
            })

        out = json.dumps(out_workspaces)

        subprocess.run(["eww", "update", f"workspacelist={out}"])
        sys.stdin.readline()
