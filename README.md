# Perforce Helix Core Python Tools

A suite of command-line tools for interacting with Perforce Helix Core server using the official P4Python SDK. These tools are profile-driven, support simple authentication, and offer essential read-only operations like listing depots and streams.

## Features

- Profile-based configuration for multiple Helix Core servers
- Simple authentication mechanism
- Essential operations:
  - List depots
  - List streams
  - List profiles
  - Delete profiles
  - Sync streams to local workspace
- Consistent authentication and configuration mechanism across all tools

## Quick Start

1. Install the phc package (see [Installation](#installation))

2. Save a profile with your credentials:
   ```bash
   phc save-profile --profile myprofile --host ssl:your-p4-server:1666 --username your-username
   # You will be prompted to enter your password securely
   ```

3. Now you're ready to run any of the commands:
   ```bash
   phc list-depots --profile myprofile
   phc list-streams --profile myprofile --depot your-depot
   phc sync-stream --profile myprofile --depot your-depot --stream your-stream --workspace-path /path/to/workspace
   ```

## Installation

### Prerequisites

- Python 3.6 or higher
- Internet access for installing dependencies

### Install from source

```bash
git clone https://github.com/yourusername/perforce-helix-core-python-tools.git
cd perforce-helix-core-python-tools
pip install -e .
```

## Configuration

All tools use a shared configuration file. The location is platform-dependent:

- On Windows: `%APPDATA%\perforce-helix-core-python-tools\config.yml` (typically `C:\Users\<username>\AppData\Roaming\perforce-helix-core-python-tools\config.yml`)
- On Unix-like systems (Linux, macOS): `~/.perforce-helix-core-python-tools/config.yml`

The configuration file has the following structure:

```yaml
profiles:
  mylocal:
    host: ssl:localhost:1666
    username: super
    password: mypassword

  prod:
    host: ssl:p4.prod.company.com:1666
    username: automation
    password: securepass
```

## Tools

All tools are accessed through the `phc` command followed by a subcommand.

### phc save-profile

Adds a new named profile to the config file. If the default config directory or file do not exist when this runs, 
the base of the config is created by this script.

```bash
phc save-profile --profile dev --host ssl:localhost:1666 --username super
```

The command will prompt you to enter your password securely. This approach ensures that passwords with special 
characters (like `!`, `$`, `*`, etc.) are handled correctly and avoids issues with shell interpretation of special 
characters.

### phc list-depots

Lists all depots on the server.

```bash
phc list-depots --profile dev [--pattern "^project.*"]
```

If `--pattern` is supplied, filters the depot names using a Python `re.search` pattern. 

**Important**: Always enclose the pattern in quotes (e.g., `--pattern "^project.*"`) to avoid shell interpretation of 
special characters like `*`, `?`, `[`, `]`, etc. If you don't use quotes, these characters might be processed by your 
shell before they reach the application, leading to unexpected results.

### phc list-streams

Lists all streams in a given depot.

```bash
phc list-streams --profile dev --depot project-x [--pattern "main"]
```

If `--pattern` is supplied, filters the stream names using a Python `re.search` pattern.

**Important**: Always enclose the pattern in quotes (e.g., `--pattern "main"`) to avoid shell interpretation of 
special characters like `*`, `?`, `[`, `]`, etc. If you don't use quotes, these characters might be processed by your 
shell before they reach the application, leading to unexpected results.

### phc list-profiles

Lists all profiles in the configuration file, showing host and username but not password.

```bash
phc list-profiles [--pattern "dev.*"]
```

If `--pattern` is supplied, filters the profile names using a Python `re.search` pattern.

**Important**: Always enclose the pattern in quotes (e.g., `--pattern "dev.*"`) to avoid shell interpretation of 
special characters like `*`, `?`, `[`, `]`, etc. If you don't use quotes, these characters might be processed by your 
shell before they reach the application, leading to unexpected results.

### phc delete-profile

Deletes a profile from the configuration file after confirmation.

```bash
phc delete-profile --profile dev
```

The command will show the profile details and ask for confirmation before deleting the profile.

### phc sync-stream

Syncs a specified stream to a local workspace path.

```bash
phc sync-stream --profile dev --depot project-x --stream main --workspace-path /path/to/workspace [--force] [--writable]
```

This command creates a temporary client workspace, syncs the specified stream to the given workspace path, and then 
deletes the temporary client workspace, leaving the files behind in the workspace path.

The command handles the workspace directory as follows:
- If the workspace directory does not exist, it will be created automatically
- If the workspace directory is not empty and `--force` is not specified, a warning will be displayed and the script will exit
- If the `--force` option is specified and the workspace directory is not empty, the directory will be cleared before syncing
- If the `--writable` option is specified, files in the workspace will be made writable after sync
- All files will be synced with the following helix core options:
  - 'clobber' - files are overwritten from the Helix Core stream
  - 'modtime' - file modification times are preserved from the Helix Core stream
  - 'unlocked' - Files in the client are not locked for editing. Multiple users can sync/edit the same file concurrently

#### What is a Temporary Client Workspace?

A temporary client workspace (or "client" in Perforce terminology) is a mapping between files in the Perforce repository 
and files on your local machine. When you sync files from Perforce, the system needs to know where to place those files 
on your local filesystem.

In the context of the `sync-stream` command, a temporary client workspace is created with the following characteristics:

1. **Temporary Nature**: It's created solely for the purpose of the current sync operation and is automatically deleted once the operation completes.
2. **Unique Naming**: It's given a unique name based on the current hostname + process ID to avoid conflicts with existing workspaces.
3. **Stream Association**: It's associated with the specified stream, which determines which files are included.
4. **Root Directory**: It's configured to use the specified workspace path as its root directory, which is where the files will be synced to.
5. **Configuration Options**: It's set up with specific options like 'noallwrite' (unless `--writable` is specified), 'clobber', etc., which control how files are handled during sync.

The temporary client workspace approach offers several advantages:
- It doesn't require you to manually create and manage Perforce client workspaces
- It ensures a clean sync operation without interference from existing workspace configurations
- It automatically cleans up after itself, leaving no residual configuration on the Perforce server

This approach is particularly useful for automation scenarios where you need to quickly sync files without setting up 
permanent client workspaces.

## Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/perforce-helix-core-python-tools.git
cd perforce-helix-core-python-tools
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

## Package Structure

### setup.py

The `setup.py` file is a standard Python packaging script that enables the installation of this project as a Python 
package. It serves several important purposes:

1. **Package Metadata**: Defines the package name, version, description, author information, and other metadata.
2. **Dependencies Management**: Lists all required dependencies (`p4python`, `pyyaml`, `click`) that will be automatically installed when the package is installed.
3. **Command-Line Entry Points**: Creates the command-line tool (`phc`) with subcommands (`save-profile`, `list-depots`, `list-streams`, `list-profiles`, `delete-profile`, `sync-stream`) by mapping them to their respective Python functions.
4. **Package Discovery**: Uses `find_packages()` to automatically discover and include all Python packages in the project.

When you run `pip install -e .` during development or installation, `setup.py` is processed to:

- Install the package in development mode (changes to the code are immediately reflected)
- Install all required dependencies
- Create the command-line entry points so you can run the tools directly from your terminal

The version number is automatically extracted from the `__version__` variable in the package's `__init__.py` file, 
and the long description is pulled from this README.md file.
