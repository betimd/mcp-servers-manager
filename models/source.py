"""
Source data model for the MCP Server Manager
"""

import json
import os


class Source:
    """
    Model representing an MCP source configuration
    """

    def __init__(self, id, name, path, icon_type="purple_dot"):
        """
        Initialize a new Source

        Args:
            id: Unique identifier for the source
            name: Display name for the source
            path: File path for the source configuration
            icon_type: CSS class for the source icon color
        """
        self.id = id
        self.name = name
        self.path = path
        self.icon_type = icon_type
        self.servers = []  # List of associated servers

    def add_server(self, server):
        """Add a server to this source"""
        if server not in self.servers:
            self.servers.append(server)
            return True
        return False

    def remove_server(self, server):
        """Remove a server from this source"""
        if server in self.servers:
            self.servers.remove(server)
            return True
        return False

    def has_server(self, server):
        """Check if this source is connected to the specified server"""
        return server in self.servers

    def load_config(self):
        """
        Load source configuration from file

        Returns:
            Dictionary with source configuration or None if file doesn't exist
        """
        if not os.path.exists(self.path):
            return None

        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def save_config(self, config):
        """
        Save source configuration to file

        Args:
            config: Dictionary with configuration data

        Returns:
            True if save was successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.path), exist_ok=True)

            with open(self.path, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except IOError:
            return False

    def sync_server(self, server):
        """
        Add a server to this source's configuration file

        Args:
            server: Server instance to add

        Returns:
            True if successful, False otherwise
        """
        config = self.load_config() or {"servers": []}

        # Ensure servers key exists
        if "servers" not in config:
            config["servers"] = []

        # Check if server already exists
        for existing in config["servers"]:
            if existing.get("url") == server.url:
                return True  # Already exists

        # Add server to config
        config["servers"].append({"name": server.name, "url": server.url})

        # Save updated config
        return self.save_config(config)

    def remove_server_from_config(self, server):
        """
        Remove a server from this source's configuration file

        Args:
            server: Server instance to remove

        Returns:
            True if successful, False otherwise
        """
        config = self.load_config()
        if not config or "servers" not in config:
            return False

        # Filter out the server to remove
        before_count = len(config["servers"])
        config["servers"] = [s for s in config["servers"] if s.get("url") != server.url]

        # If no changes were made, return early
        if before_count == len(config["servers"]):
            return True  # Server wasn't in config

        # Save updated config
        return self.save_config(config)

    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "icon_type": self.icon_type,
            "servers": [server.id for server in self.servers],
        }

    @classmethod
    def from_dict(cls, data, server_map=None):
        """Create a Source instance from a dictionary

        Args:
            data: Dictionary with source data
            server_map: Optional dictionary mapping server IDs to Server objects

        Returns:
            A new Source instance
        """
        source = cls(
            id=data["id"],
            name=data["name"],
            path=data["path"],
            icon_type=data.get("icon_type", "purple_dot"),
        )

        # Add servers if server_map is provided
        if server_map and "servers" in data:
            for server_id in data["servers"]:
                if server_id in server_map:
                    source.servers.append(server_map[server_id])

        return source
