# Workspaces Directory

This directory is intended to be used as a target location for syncing Perforce streams into local workspaces.

## Usage with sync-stream command

When using the `phc sync-stream` command, you can specify this directory (or a subdirectory) as the `--workspace-path` parameter:

```bash
phc sync-stream --profile dev --depot project-x --stream main --workspace-path /path/to/this/directory
```

## About Temporary Client Workspaces

The `sync-stream` command creates a temporary client workspace for the sync operation. This workspace is automatically deleted after the sync completes. For more details about temporary client workspaces, see the main README.md file or the documentation in the sync_stream.py file.
