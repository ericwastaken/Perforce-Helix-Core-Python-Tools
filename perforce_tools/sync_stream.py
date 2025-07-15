"""
Sync Stream Tool for Perforce Helix Core Python Tools.

This tool syncs a specified stream to a local workspace path.

It creates a temporary client workspace for the sync operation and then deletes it after completion.
A temporary client workspace is a mapping between files in the Perforce repository and files on the
local machine that exists only for the duration of the sync operation. This approach offers several advantages:
- It doesn't require manual creation and management of Perforce client workspaces
- It ensures a clean sync operation without interference from existing workspace configurations
- It automatically cleans up after itself, leaving no residual configuration on the Perforce server
"""

import click
import os
import sys
import socket
from perforce_tools.config import get_p4_client

@click.command()
@click.option('--profile', required=True, help='Profile name to use for connection')
@click.option('--depot', required=True, help='Depot name containing the stream')
@click.option('--stream', required=True, help='Stream name to sync')
@click.option('--workspace-path', required=True, help='Full path of the location to sync the stream into')
@click.option('--force', is_flag=True, help='Force sync even if workspace directory is not empty')
@click.option('--writable', is_flag=True, help='Make files in the workspace writable after sync')
def main(profile, depot, stream, workspace_path, force, writable):
    """
    Sync a stream to a local workspace path.

    Connects using the specified profile and syncs the specified stream to the given workspace path.
    Creates a temporary client workspace for the sync operation and deletes it after completion.

    The command handles the workspace directory as follows:
    - If the workspace directory does not exist, it will be created automatically
    - If the workspace directory is not empty and --force is not specified, a warning will be displayed and the script will exit
    - If the --force option is specified and the workspace directory is not empty, the directory will be cleared before syncing
    - If the --writable option is specified, files in the workspace will be made writable after sync
    """
    try:
        # Validate workspace path
        if not os.path.exists(workspace_path):
            # Create the directory if it doesn't exist
            os.makedirs(workspace_path, exist_ok=True)
            click.echo(f"Created workspace directory '{workspace_path}'")
        elif not os.path.isdir(workspace_path):
            click.echo(f"Error: Workspace path '{workspace_path}' exists but is not a directory")
            exit(1)
        else:
            # Check if directory is empty
            if os.listdir(workspace_path):
                if force:
                    click.echo(f"Workspace directory '{workspace_path}' is not empty. Clearing it...")
                    # Remove all files and directories in the workspace path
                    for item in os.listdir(workspace_path):
                        item_path = os.path.join(workspace_path, item)
                        if os.path.isdir(item_path):
                            import shutil
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    click.echo(f"Workspace directory '{workspace_path}' has been cleared")
                else:
                    click.echo(f"Warning: Workspace directory '{workspace_path}' is not empty. Use --force to clear it before syncing.")
                    exit(1)

        # Connect to Perforce
        p4 = get_p4_client(profile)
        click.echo(f"Connected to {p4.port} as {p4.user}")

        # Construct the full stream path
        stream_path = f"//{depot}/{stream}"
        click.echo(f"Syncing stream '{stream_path}' to '{workspace_path}'...")

        # Create a temporary client workspace
        # Get hostname and sanitize it for use in client name
        hostname = socket.gethostname().replace('.', '_')
        client_name = f"temp_sync_{hostname}_{os.getpid()}"
        # Set client options based on writable flag
        if writable:
            client_options = 'allwrite clobber compress unlocked modtime normdir'
            click.echo("Files will be made writable after sync")
        else:
            client_options = 'noallwrite clobber compress unlocked modtime normdir'

        client_spec = {
            'Client': client_name,
            'Owner': p4.user,
            'Root': workspace_path,
            'Options': client_options,
            'LineEnd': 'local',
            'Stream': stream_path
        }

        # Create the client
        p4.client = client_name
        p4.save_client(client_spec)
        click.echo(f"Created temporary client workspace '{client_name}'")

        try:
            # Sync the files
            click.echo("Syncing files...")
            result = p4.run_sync()
            click.echo(f"Synced {len(result)} files")

        finally:
            # Clean up the temporary client
            click.echo(f"Deleting temporary client workspace '{client_name}'...")
            p4.delete_client(client_name)

        click.echo(f"Stream sync completed successfully to '{workspace_path}'")
        p4.disconnect()

    except ValueError as e:
        click.echo(f"Error: {e}")
        exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        exit(1)

if __name__ == '__main__':
    main()
