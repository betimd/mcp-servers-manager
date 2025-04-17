"""
Server data model for the MCP Server
"""

from .utils import SERVER_SOURCE, SERVER_TYPE


class Server:
    """
    Model representing an MCP server configuration
    """

    def __init__(
        self,
        id,
        name,
        url,
        server_type=SERVER_TYPE.LOCAL,
        cmd: str = "",
        cmd_args: list = None,
        server_source: SERVER_SOURCE = None,
    ):
        """
        Initialize a new Server

        Args:
            id: Unique identifier for the server
            name: Display name for the server
            url: URL endpoint for the server
            icon_type: CSS class for the server icon color
            subtitle: Optional subtitle or description
        """
        self.id = id
        self.name = name
        self.url = url
        self.server_type = server_type
        self.cmd = cmd
        self.cmd_args = cmd_args
        self.server_source = server_source

    # review this stuff later ====

    def add_source(self, source):
        """Add a source to this server"""
        if source not in self.sources:
            self.sources.append(source)
            return True
        return False

    def remove_source(self, source):
        """Remove a source from this server"""
        if source in self.sources:
            self.sources.remove(source)
            return True
        return False

    def has_source(self, source):
        """Check if this server has the specified source"""
        return source in self.sources

    def add_tool(self, tool):
        """Add a tool to this server"""
        if tool not in self.tools:
            self.tools.append(tool)
            return True
        return False

    def to_dict(self):
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "icon_type": self.icon_type,
            "subtitle": self.subtitle,
            "sources": [source.id for source in self.sources],
            "tools": self.tools,
        }

    @classmethod
    def from_dict(cls, data, source_map=None):
        """Create a Server instance from a dictionary

        Args:
            data: Dictionary with server data
            source_map: Optional dictionary mapping source IDs to Source objects

        Returns:
            A new Server instance
        """
        server = cls(
            id=data["id"],
            name=data["name"],
            url=data["url"],
            icon_type=data.get("icon_type", "green_dot"),
            subtitle=data.get("subtitle", ""),
        )

        server.tools = data.get("tools", [])

        # Add sources if source_map is provided
        if source_map and "sources" in data:
            for source_id in data["sources"]:
                if source_id in source_map:
                    server.sources.append(source_map[source_id])

        return server
