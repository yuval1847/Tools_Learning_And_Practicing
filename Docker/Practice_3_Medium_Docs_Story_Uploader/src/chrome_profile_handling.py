import os
import json
from pathlib import Path
import platform

def find_chrome_user_data_paths():
    """
    A function which returns a list of existing Chrome/Chromium user-data directory paths."""
    system = platform.system()
    paths = []
    if system == "Windows":
        local_app = os.environ.get("LOCALAPPDATA")
        if local_app:
            paths.append(Path(local_app) / "Google" / "Chrome" / "User Data")
            paths.append(Path(local_app) / "Chromium" / "User Data")
    elif system == "Darwin":  # macOS
        home = Path.home()
        paths.append(home / "Library" / "Application Support" / "Google" / "Chrome")
        paths.append(home / "Library" / "Application Support" / "Chromium")
    else:  # assume Linux
        home = Path.home()
        paths.append(home / ".config" / "google-chrome")
        paths.append(home / ".config" / "chrome")
        paths.append(home / ".config" / "chromium")
        # some distros use /opt or other custom locations, but these cover most installs
    # filter only existing
    existing = [p for p in paths if p.exists()]
    return existing

def read_profile_info(user_data_dir: Path):
    """
    A function which returns dict mapping profile_dir_name -> friendly_name (if available).
    """
    profiles = {}
    local_state = user_data_dir / "Local State"
    if local_state.exists():
        try:
            data = json.loads(local_state.read_text(encoding="utf-8"))
            # path in Local State: data["profile"]["info_cache"]
            info_cache = data.get("profile", {}).get("info_cache", {})
            for prof_dir, info in info_cache.items():
                name = info.get("name") or prof_dir
                profiles[prof_dir] = name
        except Exception:
            pass

    # fallback: enumerate directories named "Default", "Profile X", ...
    for child in sorted(user_data_dir.iterdir()):
        if child.is_dir() and (child.name == "Default" or child.name.startswith("Profile") or child.name.startswith("Person")):
            if child.name not in profiles:
                profiles[child.name] = child.name
    return profiles

def choose_profile():
    candidates = find_chrome_user_data_paths()
    if not candidates:
        print("No Chrome/Chromium user-data directories found on this system.")
        return None

    # If multiple user-data paths exist (Chrome + Chromium), list them
    choice_map = []
    for ud in candidates:
        print(f"\nFound user-data directory: {ud}")
        profiles = read_profile_info(ud)
        if not profiles:
            print("  (no profiles detected inside; the directory may be empty or use a custom install)")
            continue
        entries = list(profiles.items())  # list of (profile_dir_name, friendly_name)
        for idx, (prof_dir, friendly_name) in enumerate(entries, start=1):
            print(f"  [{len(choice_map)+idx}] {friendly_name}  (profile dir: {prof_dir})")
            choice_map.append((ud, prof_dir, friendly_name))

    if not choice_map:
        print("No profiles found inside available user-data directories.")
        return None
    # Print instructions
    while True:
        sel = input(f"\nEnter profile number to use (1..{len(choice_map)}), or 'q' to quit: ").strip()
        if sel.lower() == 'q':
            return None
        if not sel.isdigit():
            print("Please enter a number.")
            continue
        n = int(sel)
        if 1 <= n <= len(choice_map):
            user_data_dir, profile_dir_name, friendly = choice_map[n-1]
            print(f"Selected: {friendly} (profile dir: {profile_dir_name}) in {user_data_dir}")
            return user_data_dir, profile_dir_name
        else:
            print("Number out of range. Try again.")