"""
Main CLI entry point for Perforce Helix Core Python Tools.

This module defines the main 'phc' command group and imports the existing commands as subcommands.
"""

import click
from perforce_tools.save_profile import main as save_profile_cmd
from perforce_tools.list_depots import main as list_depots_cmd
from perforce_tools.list_streams import main as list_streams_cmd
from perforce_tools.list_profiles import main as list_profiles_cmd
from perforce_tools.delete_profile import main as delete_profile_cmd
from perforce_tools.sync_stream import main as sync_stream_cmd

@click.group()
def cli():
    """
    Perforce Helix Core Python Tools.

    A suite of command-line tools for interacting with Perforce Helix Core server.
    """
    pass

# Add commands to the group
cli.add_command(save_profile_cmd, name='save-profile')
cli.add_command(list_depots_cmd, name='list-depots')
cli.add_command(list_streams_cmd, name='list-streams')
cli.add_command(list_profiles_cmd, name='list-profiles')
cli.add_command(delete_profile_cmd, name='delete-profile')
cli.add_command(sync_stream_cmd, name='sync-stream')

if __name__ == '__main__':
    cli()
