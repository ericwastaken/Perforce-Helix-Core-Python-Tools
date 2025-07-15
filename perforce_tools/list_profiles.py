"""
List Profiles Tool for Perforce Helix Core Python Tools.

This tool lists all profiles in the configuration file, showing host and username but not password.
"""

import click
import re
import sys
from perforce_tools.config import load_config, warn_pattern_quoting

@click.command()
@click.option('--pattern', required=False, 
              help='Regex pattern to filter profile names (enclose in quotes to avoid shell interpretation)')
def main(pattern):
    """
    List all profiles in the configuration file.

    Shows the profile name, host, and username for each profile.
    If --pattern is supplied, filters the profile names using a Python re.search pattern.
    """
    try:
        config = load_config()
        profiles = config.get("profiles", {})

        if not profiles:
            click.echo("No profiles found.")
            return

        if pattern:
            warn_pattern_quoting(pattern)
            click.echo(f"Filtering profiles with pattern: {pattern}")
            profiles = {name: profile for name, profile in profiles.items() if re.search(pattern, name)}

        if not profiles:
            click.echo("No profiles found matching the pattern.")
            return

        click.echo("\nProfiles:")
        for name, profile in profiles.items():
            click.echo(f"  {name} - Host: {profile['host']} - Username: {profile['username']}")

    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
