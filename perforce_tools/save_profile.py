"""
Save Profile Tool for Perforce Helix Core Python Tools.

This tool adds a new named profile to the config file.
"""

import click
from perforce_tools.config import save_profile

@click.command()
@click.option('--profile', required=True, help='Profile name to save')
@click.option('--host', required=True, help='Perforce server host (e.g., ssl:localhost:1666)')
@click.option('--username', required=True, help='Perforce username')
def main(profile, host, username):
    """
    Add a new named profile to the config file.

    Tests connectivity to the Helix Core server using the provided host and credentials.
    On success, updates (or creates) ~/.perforce-helix-core-python-tools/config.yml and adds the profile.
    """

    password = click.prompt('Enter Perforce password', hide_input=True)

    click.echo(f"Testing connection to {host} with username {username}...")

    if save_profile(profile, host, username, password):
        click.echo(f"Profile '{profile}' saved successfully.")
    else:
        click.echo(f"Failed to save profile '{profile}'. Please check your connection details.")
        exit(1)

if __name__ == '__main__':
    main()
