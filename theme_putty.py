"""

theme_putty.py

Apply a PuTTY theme to all PuTTY profiles.

"""

import os
import winreg

PUTTY_PATH = "Software\\SimonTatham\\PuTTY\\Sessions"

def parse_file(stream):
    """Get colors from a theme file."""
    obj = {
        "key": None,
        "subkey": {}
    }
    for line in stream:
        if line.startswith("\""):
            pair = (x.replace('"', '') for x in line.split("="))
            key, val = pair
            obj["subkey"][key] = val
        if line.startswith("[") and obj["key"] is None:
            obj["key"] = line.replace("[", "").replace("]", "")
    return obj


def parse_session(session_name):
    """Get colors from another PuTTY session."""

    values = (
        "Colour21", "Colour20", "Colour19", "Colour18",
        "Colour17", "Colour16", "Colour15", "Colour14",
        "Colour13", "Colour12", "Colour11", "Colour10",
        "Colour9", "Colour8", "Colour7", "Colour6",
        "Colour5", "Colour4", "Colour3", "Colour2",
        "Colour1", "Colour0",
    )

    new_path = os.path.join(PUTTY_PATH, session_name)
    colors = { "key": new_path, "subkey": {} }

    for v in values:
        handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, new_path)
        with handle:
            value, _ = winreg.QueryValueEx(handle, v)
            colors["subkey"][v] = value

    return colors


def get_profiles(handle=None):
    """Return a list of putty profiles."""
    if handle is None:
        handle = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, PUTTY_PATH)

    index = 0
    try:
        while True:
            subkey_name = winreg.EnumKey(handle, index)
            index += 1
            yield subkey_name
    except OSError:
        winreg.CloseKey(handle)
        return


def theme_profiles(colors, profiles=None):
    """Apply a theme to some profiles."""

    for profile in profiles:
        new_path = os.path.join(PUTTY_PATH, profile)
        handle = winreg.OpenKeyEx(
            winreg.HKEY_CURRENT_USER, new_path,
            access = (winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY)
        )

        with handle:
            for key, value in colors["subkey"].items():
                winreg.SetValueEx(handle, key, 0, winreg.REG_SZ, value)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("theme", help="File to read colors from OR session to read from.")
    parser.add_argument("profiles", nargs='*', help="Profiles to change; by default an empty list means 'all profiles'.")
    parser.add_argument("-b", "--blacklist", help="Make the passed list of profiles a blacklist.", action="store_true")

    args = parser.parse_args()
    colors = parse_file(args.theme)

    colors = None
    if args.theme.endswith(".reg"):
        with open(args.theme, "r") as fobj:
            colors = parse_file(fobj)
    else:
        colors = parse_session(args.theme)

    if args.blacklist:
        profiles = [
            p for p in get_profiles()
            if p not in args.profiles
        ]
    elif args.profiles is None or args.profiles == []:
        profiles = [p for p in get_profiles()]
    else:
        profiles = [p for p in get_profiles() if p in args.profiles]

    theme_profiles(colors, profiles)


if __name__ == "__main__":
    main()
