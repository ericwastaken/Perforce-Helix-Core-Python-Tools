"""
List Streams Tool for Perforce Helix Core Python Tools.

This tool lists all streams in a given depot with an optional pattern filter.
"""

import click
import re
import sys
from perforce_tools.config import get_p4_client, warn_pattern_quoting

@click.command()
@click.option('--profile', required=True, help='Profile name to use for connection')
@click.option('--depot', required=True, help='Depot name to list streams from')
@click.option('--pattern', required=False, 
              help='Regex pattern to filter stream names (enclose in quotes to avoid shell interpretation)')
def main(profile, depot, pattern):
    """
    List all streams in a given depot.

    Connects using the specified profile and runs 'p4 streams //depot/...'.
    If --pattern is supplied, filters the stream names using a Python re.search pattern.
    """
    try:
        p4 = get_p4_client(profile)

        click.echo(f"Connected to {p4.port} as {p4.user}")
        click.echo(f"Listing streams in depot '{depot}'...")

        streams = p4.run("streams", f"//{depot}/...")

        if pattern:
            warn_pattern_quoting(pattern)
            click.echo(f"Filtering streams with pattern: {pattern}")
            streams = [stream for stream in streams if re.search(pattern, stream["Stream"])]

        if not streams:
            click.echo("No streams found.")
            return

        click.echo("\nStreams:")
        for stream in streams:
            click.echo(f"  {stream['Stream']} - {stream.get('Type', 'N/A')} - {stream.get('Description', 'No description')}")

        p4.disconnect()

    except ValueError as e:
        click.echo(f"Error: {e}")
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
