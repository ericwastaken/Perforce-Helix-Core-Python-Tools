"""
List Depots Tool for Perforce Helix Core Python Tools.

This tool lists all depots on the server with an optional pattern filter.
"""

import click
import re
import sys
from perforce_tools.config import get_p4_client, warn_pattern_quoting

@click.command()
@click.option('--profile', required=True, help='Profile name to use for connection')
@click.option('--pattern', required=False, 
              help='Regex pattern to filter depot names (enclose in quotes to avoid shell interpretation)')
def main(profile, pattern):
    """
    List all depots on the server.

    Connects using the specified profile and runs 'p4 depots'.
    If --pattern is supplied, filters the depot names using a Python re.search pattern.
    """
    try:
        p4 = get_p4_client(profile)

        click.echo(f"Connected to {p4.port} as {p4.user}")
        click.echo("Listing depots...")

        depots = p4.run("depots")

        if pattern:
            warn_pattern_quoting(pattern)
            click.echo(f"Filtering depots with pattern: {pattern}")
            depots = [depot for depot in depots if re.search(pattern, depot["name"])]

        if not depots:
            click.echo("No depots found.")
            return

        click.echo("\nDepots:")
        for depot in depots:
            click.echo(f"  {depot['name']} - {depot['desc']}")

        p4.disconnect()

    except ValueError as e:
        click.echo(f"Error: {e}")
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
