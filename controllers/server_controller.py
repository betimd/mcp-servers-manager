"""
Server controller for managing MCP servers
"""

import json
import os

from models.server import Server


class ServerController:
    """
    Controller for managing MCP servers
    Handles CRUD operations and persistence
    """

    def __init__(self, config_path=None):
        """
        Initialize the ServerController

        Args:
            config_path: Path to the configuration file
        """
        self.servers = {}  # Dictionary of servers keyed by ID
        self.selected_server_id = None

        # Set default config path if not provided
        if config_path is None:
            home_dir = os.path.expanduser("~")
            self.config_path = os.path.join(
                home_dir, ".mcp_server_manager", "servers.json"
            )
        else:
            self.config_path = config_path

        # Load servers from config file
        self.load_servers()

    def create_server(self, name, url, icon_type="green_dot", subtitle=""):
        """
        Create a new server

        Args:
            name: Display name for the server
            url: URL endpoint for the server
            icon_type: CSS class for the server icon color
            subtitle: Optional subtitle or description

        Returns:
            The created Server instance
        """
        # Generate a unique ID
        server_id = self._generate_unique_id(name)

        # Create a new server
        server = Server(server_id, name, url, icon_type, subtitle)

        # Add the server to the dictionary
        self.servers[server_id] = server

        # Save changes
        self.save_servers()

        return server

    def update_server(self, server_id, **kwargs):
        """
        Update an existing server

        Args:
            server_id: ID of the server to update
            **kwargs: Attributes to update (name, url, icon_type, subtitle)

        Returns:
            True if the server was updated, False if it doesn't exist
        """
        if server_id not in self.servers:
            return False

        server = self.servers[server_id]

        # Update attributes
        if "name" in kwargs:
            server.name = kwargs["name"]
        if "url" in kwargs:
            server.url = kwargs["url"]
        if "icon_type" in kwargs:
            server.icon_type = kwargs["icon_type"]
        if "subtitle" in kwargs:
            server.subtitle = kwargs["subtitle"]

        # Save changes
        self.save_servers()

        return True

    def delete_server(self, server_id):
        """
        Delete a server

        Args:
            server_id: ID of the server to delete

        Returns:
            True if the server was deleted, False if it doesn't exist
        """
        if server_id not in self.servers:
            return False

        # Remove the server
        del self.servers[server_id]

        # If the selected server was deleted, clear the selection
        if self.selected_server_id == server_id:
            self.selected_server_id = None

        # Save changes
        self.save_servers()

        return True

    def get_server(self, server_id):
        """
        Get a server by ID

        Args:
            server_id: ID of the server to get

        Returns:
            The Server instance or None if it doesn't exist
        """
        return self.servers.get(server_id)

    def get_all_servers(self):
        """
        Get all servers

        Returns:
            List of all Server instances
        """
        return list(self.servers.values())

    def select_server(self, server_id):
        """
        Select a server

        Args:
            server_id: ID of the server to select

        Returns:
            True if the server was selected, False if it doesn't exist
        """
        if server_id not in self.servers and server_id is not None:
            return False

        self.selected_server_id = server_id
        return True

    def get_selected_server(self):
        """
        Get the currently selected server

        Returns:
            The selected Server instance or None if no server is selected
        """
        if self.selected_server_id is None:
            return None

        return self.servers.get(self.selected_server_id)

    def add_source_to_server(self, server_id, source):
        """
        Add a source to a server

        Args:
            server_id: ID of the server
            source: Source instance to add

        Returns:
            True if the source was added, False if the server doesn't exist
        """
        server = self.get_server(server_id)
        if server is None:
            return False

        # Add source to server
        result = server.add_source(source)

        # Add server to source
        if result:
            source.add_server(server)

        # Save changes
        self.save_servers()

        return result

    def remove_source_from_server(self, server_id, source):
        """
        Remove a source from a server

        Args:
            server_id: ID of the server
            source: Source instance to remove

        Returns:
            True if the source was removed, False if the server doesn't exist
        """
        server = self.get_server(server_id)
        if server is None:
            return False

        # Remove source from server
        result = server.remove_source(source)

        # Remove server from source
        if result:
            source.remove_server(server)

        # Save changes
        self.save_servers()

        return result

    def add_tool_to_server(self, server_id, tool):
        """
        Add a tool to a server

        Args:
            server_id: ID of the server
            tool: Tool name to add

        Returns:
            True if the tool was added, False if the server doesn't exist
        """
        server = self.get_server(server_id)
        if server is None:
            return False

        # Add tool to server
        result = server.add_tool(tool)

        # Save changes
        self.save_servers()

        return result

    def load_servers(self):
        """
        Load servers from the configuration file
        """
        if not os.path.exists(self.config_path):
            return

        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)

            # Clear existing servers
            self.servers = {}

            # Load servers
            for server_data in data.get("servers", []):
                server = Server.from_dict(server_data)
                self.servers[server.id] = server

            # Load selected server
            self.selected_server_id = data.get("selected_server_id")

        except (json.JSONDecodeError, IOError):
            # If there's an error, start with an empty set of servers
            self.servers = {}
            self.selected_server_id = None

    def save_servers(self):
        """
        Save servers to the configuration file
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)

        # Prepare data
        data = {
            "servers": [server.to_dict() for server in self.servers.values()],
            "selected_server_id": self.selected_server_id,
        }

        # Write to file
        try:
            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)
        except IOError:
            # Handle IO errors
            print(f"Error saving servers to {self.config_path}")

    def _generate_unique_id(self, name):
        """
        Generate a unique ID based on the name

        Args:
            name: Server name

        Returns:
            A unique ID string
        """
        # Convert name to lowercase and replace spaces with underscores
        base_id = name.lower().replace(" ", "_")

        # If the ID is already used, append a number
        if base_id in self.servers:
            counter = 1
            while f"{base_id}_{counter}" in self.servers:
                counter += 1
            return f"{base_id}_{counter}"

        return base_id
