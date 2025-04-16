"""
Source controller for managing MCP sources
"""

import json
import os

from models.source import Source


class SourceController:
    """
    Controller for managing MCP sources
    Handles CRUD operations and persistence
    """

    def __init__(self, config_path=None):
        """
        Initialize the SourceController

        Args:
            config_path: Path to the configuration file
        """
        self.sources = {}  # Dictionary of sources keyed by ID

        # Set default config path if not provided
        if config_path is None:
            home_dir = os.path.expanduser("~")
            self.config_path = os.path.join(
                home_dir, ".mcp_server_manager", "sources.json"
            )
        else:
            self.config_path = config_path

        # Load sources from config file
        self.load_sources()

    def create_source(self, name, path, icon_type="purple_dot"):
        """
        Create a new source

        Args:
            name: Display name for the source
            path: File path for the source configuration
            icon_type: CSS class for the source icon color

        Returns:
            The created Source instance
        """
        # Generate a unique ID
        source_id = self._generate_unique_id(name)

        # Create a new source
        source = Source(source_id, name, path, icon_type)

        # Add the source to the dictionary
        self.sources[source_id] = source

        # Save changes
        self.save_sources()

        return source

    def update_source(self, source_id, **kwargs):
        """
        Update an existing source

        Args:
            source_id: ID of the source to update
            **kwargs: Attributes to update (name, path, icon_type)

        Returns:
            True if the source was updated, False if it doesn't exist
        """
        if source_id not in self.sources:
            return False

        source = self.sources[source_id]

        # Update attributes
        if "name" in kwargs:
            source.name = kwargs["name"]
        if "path" in kwargs:
            source.path = kwargs["path"]
        if "icon_type" in kwargs:
            source.icon_type = kwargs["icon_type"]

        # Save changes
        self.save_sources()

        return True

    def delete_source(self, source_id):
        """
        Delete a source

        Args:
            source_id: ID of the source to delete

        Returns:
            True if the source was deleted, False if it doesn't exist
        """
        if source_id not in self.sources:
            return False

        # Remove the source
        del self.sources[source_id]

        # Save changes
        self.save_sources()

        return True

    def get_source(self, source_id):
        """
        Get a source by ID

        Args:
            source_id: ID of the source to get

        Returns:
            The Source instance or None if it doesn't exist
        """
        return self.sources.get(source_id)

    def get_all_sources(self):
        """
        Get all sources

        Returns:
            List of all Source instances
        """
        return list(self.sources.values())

    def sync_source_to_server(self, source_id, server):
        """
        Sync a source to a server

        Args:
            source_id: ID of the source
            server: Server instance to sync with

        Returns:
            True if the source was synced, False if the source doesn't exist
        """
        source = self.get_source(source_id)
        if source is None:
            return False

        # Sync source to server configuration file
        result = source.sync_server(server)

        # Update relationships in memory
        if result:
            source.add_server(server)
            server.add_source(source)

        # Save changes
        self.save_sources()

        return result

    def remove_source_from_server_config(self, source_id, server):
        """
        Remove a source from a server's configuration

        Args:
            source_id: ID of the source
            server: Server instance to remove from

        Returns:
            True if the source was removed, False if the source doesn't exist
        """
        source = self.get_source(source_id)
        if source is None:
            return False

        # Remove server from source configuration file
        result = source.remove_server_from_config(server)

        # Update relationships in memory
        if result:
            source.remove_server(server)
            server.remove_source(source)

        # Save changes
        self.save_sources()

        return result

    def sync_source_to_all_servers(self, source_id, servers):
        """
        Sync a source to all servers

        Args:
            source_id: ID of the source
            servers: List of Server instances to sync with

        Returns:
            Dictionary mapping server IDs to success/failure
        """
        results = {}

        for server in servers:
            results[server.id] = self.sync_source_to_server(source_id, server)

        return results

    def remove_source_from_all_servers(self, source_id, servers):
        """
        Remove a source from all servers

        Args:
            source_id: ID of the source
            servers: List of Server instances to remove from

        Returns:
            Dictionary mapping server IDs to success/failure
        """
        results = {}

        for server in servers:
            results[server.id] = self.remove_source_from_server_config(
                source_id, server
            )

        return results

    def detect_sources(self):
        """
        Auto-detect MCP sources in standard locations

        Returns:
            List of detected sources
        """
        detected = []
        home_dir = os.path.expanduser("~")

        # Common locations to check
        paths_to_check = [
            # VS Code
            os.path.join(
                home_dir, ".vscode", "extensions", "anthropic.claude-1.0.0", "mcp.json"
            ),
            # Claude Desktop
            os.path.join(home_dir, ".config", "claude-desktop", "mcp.json"),
            # Cursor
            os.path.join(
                "/Applications", "Cursor.app", "Contents", "Resources", "mcp.json"
            ),
            # Windsurf
            os.path.join(home_dir, ".windsurf", "mcp.json"),
        ]

        # Check each path
        for path in paths_to_check:
            if os.path.exists(path):
                # Determine source name from path
                if "claude-desktop" in path:
                    name = "Claude Desktop"
                    icon = "purple_dot"
                elif "vscode" in path:
                    name = "VS Code"
                    icon = "blue_dot"
                elif "Cursor.app" in path:
                    name = "Cursor"
                    icon = "green_dot"
                elif "windsurf" in path:
                    name = "Windsurf"
                    icon = "orange_dot"
                else:
                    # Extract name from directory
                    name = os.path.basename(os.path.dirname(path))
                    icon = "purple_dot"

                # Create source if it doesn't exist
                source_id = self._generate_unique_id(name)
                if source_id not in self.sources:
                    source = self.create_source(name, path, icon)
                    detected.append(source)

        return detected

    def load_sources(self):
        """
        Load sources from the configuration file
        """
        if not os.path.exists(self.config_path):
            return

        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)

            # Clear existing sources
            self.sources = {}

            # Load sources
            for source_data in data.get("sources", []):
                source = Source.from_dict(source_data)
                self.sources[source.id] = source

        except (json.JSONDecodeError, IOError):
            # If there's an error, start with an empty set of sources
            self.sources = {}

    def save_sources(self):
        """
        Save sources to the configuration file
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # Prepare data
        data = {"sources": [source.to_dict() for source in self.sources.values()]}

        # Write to file
        try:
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError:
            # Handle IO errors
            print(f"Error saving sources to {self.config_path}")

    def _generate_unique_id(self, name):
        """
        Generate a unique ID based on the name

        Args:
            name: Source name

        Returns:
            A unique ID string
        """
        # Convert name to lowercase and replace spaces with underscores
        base_id = name.lower().replace(" ", "_")

        # If the ID is already used, append a number
        if base_id in self.sources:
            counter = 1
            while f"{base_id}_{counter}" in self.sources:
                counter += 1
            return f"{base_id}_{counter}"

        return base_id
