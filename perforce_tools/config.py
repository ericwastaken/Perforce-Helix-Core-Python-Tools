"""
Configuration module for Perforce Helix Core Python Tools.

This module handles loading, saving, and validating profiles for connecting to Perforce servers.
"""

import os
import yaml
from pathlib import Path
import P4
import click

# Constants
# Use platform-appropriate config directory
if os.name == 'nt':  # Windows
    CONFIG_DIR = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), "perforce-helix-core-python-tools")
else:  # Unix-like systems (Linux, macOS)
    CONFIG_DIR = os.path.expanduser("~/.perforce-helix-core-python-tools")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.yml")

def ensure_config_dir():
    """
    Ensure the configuration directory exists.

    Returns:
        Path: Path to the configuration directory
    """
    config_path = Path(CONFIG_DIR)
    config_path.mkdir(parents=True, exist_ok=True)
    return config_path

def load_config():
    """
    Load the configuration file.

    Returns:
        dict: The configuration as a dictionary
    """
    ensure_config_dir()

    if not os.path.exists(CONFIG_FILE):
        return {"profiles": {}}

    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f) or {"profiles": {}}

def save_config(config):
    """
    Save the configuration to the config file.

    Args:
        config (dict): The configuration to save
    """
    ensure_config_dir()

    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def get_profile(profile_name):
    """
    Get a specific profile from the configuration.

    Args:
        profile_name (str): The name of the profile to get

    Returns:
        dict: The profile configuration

    Raises:
        ValueError: If the profile does not exist
    """
    config = load_config()

    if profile_name not in config.get("profiles", {}):
        raise ValueError(f"Profile '{profile_name}' does not exist")

    return config["profiles"][profile_name]

def save_profile(profile_name, host, username, password):
    """
    Save a profile to the configuration.

    Args:
        profile_name (str): The name of the profile
        host (str): The Perforce server host
        username (str): The Perforce username
        password (str): The Perforce password

    Returns:
        bool: True if the profile was saved successfully
    """
    # Test connection first
    if not test_connection(host, username, password):
        return False

    config = load_config()

    if "profiles" not in config:
        config["profiles"] = {}

    config["profiles"][profile_name] = {
        "host": host,
        "username": username,
        "password": password
    }

    save_config(config)
    return True

def test_connection(host, username, password):
    """
    Test connection to a Perforce server.

    Args:
        host (str): The Perforce server host
        username (str): The Perforce username
        password (str): The Perforce password

    Returns:
        bool: True if the connection was successful
    """
    p4 = P4.P4()
    p4.port = host
    p4.user = username
    p4.password = password

    try:
        p4.connect()
        p4.disconnect()
        return True
    except P4.P4Exception as e:
        print(f"Error connecting to Perforce server: {e}")
        return False

def get_p4_client(profile_name):
    """
    Get a connected P4 client using the specified profile.

    Args:
        profile_name (str): The name of the profile to use

    Returns:
        P4.P4: A connected P4 client

    Raises:
        ValueError: If the profile does not exist or connection fails
    """
    profile = get_profile(profile_name)

    p4 = P4.P4()
    p4.port = profile["host"]
    p4.user = profile["username"]
    p4.password = profile["password"]

    try:
        p4.connect()
        return p4
    except P4.P4Exception as e:
        raise ValueError(f"Failed to connect to Perforce server: {e}")

def warn_pattern_quoting(pattern):
    """
    Output a warning message about pattern quoting.

    This function should be called whenever a --pattern option is used.
    It reminds users to double quote their patterns to avoid command line character manipulation.

    Args:
        pattern (str): The pattern that was provided
    """
    if pattern:
        click.echo("Note: Patterns should be double quoted to avoid command line character manipulation.")
        click.echo('Example: --pattern "your pattern"')
