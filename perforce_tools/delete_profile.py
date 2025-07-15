"""
Delete Profile Tool for Perforce Helix Core Python Tools.

This tool deletes a profile from the configuration file after confirmation.
"""

import click
from perforce_tools.config import load_config, save_config, get_profile

@click.command()
@click.option('--profile', required=True, help='Profile name to delete')
def main(profile):
    """
    Delete a profile from the configuration file.
    
    Asks for confirmation before deleting the profile.
    """
    try:
        # Check if profile exists
        try:
            profile_data = get_profile(profile)
        except ValueError as e:
            click.echo(f"Error: {e}")
            exit(1)
        
        # Show profile details and ask for confirmation
        click.echo(f"Profile: {profile}")
        click.echo(f"Host: {profile_data['host']}")
        click.echo(f"Username: {profile_data['username']}")
        
        if not click.confirm("Are you sure you want to delete this profile?"):
            click.echo("Profile deletion cancelled.")
            return
        
        # Delete profile
        config = load_config()
        del config["profiles"][profile]
        save_config(config)
        
        click.echo(f"Profile '{profile}' deleted successfully.")
        
    except Exception as e:
        click.echo(f"Unexpected error: {e}")
        exit(1)

if __name__ == '__main__':
    main()