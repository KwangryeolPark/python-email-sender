import re
from typing import List

def extract_version_from_setup(setup_path: str) -> str:
    """Extract version from setup.py."""
    with open(setup_path, "r") as f:
        content = f.read()
    
    # Version format: version='x.x.x' or version="x.x.x.yyy where yyy is a string suffix"
    match = re.search(r"version=['\"]([0-9]+\.[0-9]+\.[0-9]+(?:\.[a-zA-Z]+)?)['\"]", content, re.IGNORECASE)
    
    if match:
        return match.group(1)
    raise ValueError("Version not found in setup.py")

def extract_version_from_readme(readme_path: str) -> str:
    """Extract version from README.md."""
    with open(readme_path, "r") as f:
        content = f.read()
    
    # Version format: version='x.x.x' or version="x.x.x.y where y is a suffix"
    match = re.search(r"version=['\"]([0-9]+\.[0-9]+\.[0-9]+(?:\.[a-zA-Z]+)?)['\"]", content, re.IGNORECASE)
    if match:
        return match.group(1)
    raise ValueError("Version not found in README.md")

def extract_version_from_init(init_path: str) -> str:
    """Extract version from __init__.py."""
    with open(init_path, "r") as f:
        content = f.read()
    
    # Search for the pattern "__version__ = 'x.x.x' or 'x.x.x.yyy'"
    match = re.search(r"__version__\s*=\s*['\"]([0-9]+\.[0-9]+\.[0-9]+(?:\.[a-zA-Z]+)?)['\"]", content, re.IGNORECASE)
    
    if match:
        return match.group(1)
    raise ValueError("Version not found in __init__.py")

def get_latest_version(versions: List[str]) -> str:
    """Get the latest version from a list of versions."""
    if not versions:
        raise ValueError("No versions found")
    
    def version_key(version):
        def suffix_key(suffix):
            """
            Convert a suffix like 'a', 'z', 'aa', 'ab', ... into an equivalent numeric value for comparison.
            'a' -> 1, 'b' -> 2, ..., 'z' -> 26, 'aa' -> 27, ..., 'az' -> 52, and so on.
            """
            value = 0
            for char in suffix:
                value = value * 26 + (ord(char) - ord('a') + 1)
            return value
        parts = version.split(".")
        major, minor, patch = map(int, parts[:3])
        if len(parts) == 3:
            suffix = "a"
        else:
            suffix = parts[3]
        return (major, minor, patch, suffix_key(suffix))
    
    return max(versions, key=version_key)
def increment_suffix(suffix: str) -> str:
    """
    Increment the suffix string (e.g., 'a' -> 'b', 'z' -> 'aa', ..., 'az' -> 'ba').
    """
    if not suffix:
        return "a"
    
    suffix_list = list(suffix)
    i = len(suffix_list) - 1
    
    while i >= 0:
        if suffix_list[i] == 'z':
            suffix_list[i] = 'a'
            i -= 1
        else:
            suffix_list[i] = chr(ord(suffix_list[i]) + 1)
            break
    else:
        # If all characters were 'z', add an extra 'a' at the front
        suffix_list.insert(0, 'a')
    
    return ''.join(suffix_list)

def update_version(current_version: str, major: bool = False, minor: bool = False, patch: bool = False, commit: bool = False) -> str:
    """
    Update the current version based on the specified flags.
    
    Args:
        current_version (str): The current version string in the format xx.xx.xx.yy.
        major (bool): If True, increment the major version and reset minor, patch, and suffix.
        minor (bool): If True, increment the minor version and reset patch and suffix.
        patch (bool): If True, increment the patch version and reset suffix.
        commit (bool): If True, increment the suffix only.
    
    Returns:
        str: The updated version string.
    """
    # Split the current version into its components
    parts = current_version.split(".")
    if len(parts) == 3:
        parts.append("a")
        
    if len(parts) != 4:
        raise ValueError("current_version must be in the format xx.xx.xx.yy")
    
    major_ver, minor_ver, patch_ver = map(int, parts[:3])
    suffix = parts[3]
    
    # Update the version based on the flags
    if major:
        major_ver += 1
        minor_ver = 0
        patch_ver = 0
    elif minor:
        minor_ver += 1
        patch_ver = 0
    elif patch:
        patch_ver += 1
    
    if commit:
        suffix = increment_suffix(suffix)
    else:
        raise ValueError("At least one of major, minor, patch, or commit must be True")
    
    # Construct the new version string
    return f"{major_ver}.{minor_ver}.{patch_ver}.{suffix}"

def compare_versions(setup_version, init_version):
    """Compare versions from all files."""
    if setup_version == init_version:
        print("All versions are the same")
    else:
        print("Versions are different")
        print(f"setup.py: {setup_version}")
        print(f"__init__.py: {init_version}")        
        
def update_version_in_setup(setup_path="setup.py", old_version=None, new_version=None):
    assert old_version is not None, "old_version must be provided"
    assert new_version is not None, "new_version must be provided"
    """Update version in setup.py."""
    with open(setup_path, "r") as f:
        content = f.read()
    content = content.replace(f"version='{old_version}'", f"version='{new_version}'")
    with open(setup_path, "w") as f:
        f.write(content)
    
def update_version_in_init(init_path="__init__.py", old_version=None, new_version=None):
    assert new_version is not None, "new_version must be provided"
    """Update version in __init__.py."""
    with open(init_path, "r") as f:
        content = f.read()
    content = content.replace(f"__version__ = '{old_version}'", f"__version__ = '{new_version}'")
    with open(init_path, "w") as f:
        f.write(content)
        
        
def main():
    # File paths
    setup_path = "setup.py"
    init_path = "python_email_sender/__init__.py"
    
    # Extract versions
    setup_version = extract_version_from_setup(setup_path)
    init_version = extract_version_from_init(init_path)
    
    # Compare versions
    compare_versions(setup_version, init_version)
    
    # Get latest version
    latest_version = get_latest_version([setup_version, init_version])
    print(f"Latest version: {latest_version}")
    
    # Update version
    major = input("Increment major version? (if not compatible with the previous version) (y/n): ").lower() == "y"
    minor = input("Increment minor version? (if you add functionality in a backwards-compatible manner) (y/n): ").lower() == "y"
    patch = input("Increment patch version? (if you make backwards-compatible bug fixes) (y/n): ").lower() == "y"
    commit = input("Increment commit version? (if you commit changes without changing the functionality) (y/n): ").lower() == "y"

    new_version = update_version(latest_version, major, minor, patch, commit)
    print(f"New version: {new_version}")
    
    # Update version in setup.py
    update_version_in_setup(setup_path, latest_version, new_version)
    
    # Update version in __init__.py
    update_version_in_init(init_path, latest_version, new_version)

if __name__ == "__main__":
    main()

