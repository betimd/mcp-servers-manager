"""
Dashboard view for the MCP Server Manager
"""

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from controllers.server_controller import ServerController
from controllers.source_controller import SourceController
from ui.custom_widgets.detail_section import DetailSection
from ui.custom_widgets.server_item import ServerItem
from ui.custom_widgets.source_card import SourceCard
from ui.styles import apply_dashboard_styles


class DashboardView(QWidget):
    """Dashboard view with server list and server details"""

    def __init__(self):
        super().__init__()

        # Initialize controllers
        self.server_controller = ServerController()
        self.source_controller = SourceController()

        # Create main layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create sidebar and content area
        self.create_sidebar()
        self.create_content_area()

        # Add to main layout
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.server_content)

        # Set stretch factors (1:3 ratio)
        self.layout.setStretch(0, 1)  # Sidebar
        self.layout.setStretch(1, 3)  # Content

        # Apply styles
        apply_dashboard_styles(self)

        # Initialize with dummy data if needed
        self.initialize_dummy_data()

        # Load servers in the UI
        self.load_servers()

    def create_sidebar(self):
        """Create the sidebar with server list"""
        # Create sidebar widget and layout
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setMinimumWidth(250)
        self.sidebar.setMaximumWidth(300)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(16, 16, 16, 16)
        self.sidebar_layout.setSpacing(16)

        # Add search box
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search servers...")
        self.search_box.setObjectName("search_box")
        self.search_box.textChanged.connect(self.filter_servers)
        self.sidebar_layout.addWidget(self.search_box)

        # Add servers label
        self.servers_label = QLabel("SERVERS")
        self.servers_label.setObjectName("sidebar_section_label")
        self.sidebar_layout.addWidget(self.servers_label)

        # Add server list
        self.server_list = QListWidget()
        self.server_list.setObjectName("server_list")
        self.server_list.itemClicked.connect(self.on_server_selected)
        self.sidebar_layout.addWidget(self.server_list)

        # Servers will be loaded in load_servers()

    def initialize_dummy_data(self):
        """Initialize with some dummy data if no servers exist"""

        # Only add dummy data if no servers exist
        if self.server_controller.get_all_servers():
            return

        # Create some sample servers
        neon_server = self.server_controller.create_server(
            name="Neon MCP Server",
            url="https://mcp.neon.tech/sse",
            icon_type="green_dot",
            subtitle="2 sources",
        )

        local_server = self.server_controller.create_server(
            name="Local Development MCP",
            url="http://localhost:3000/sse",
            icon_type="blue_dot",
            subtitle="VS Code",
        )

        openai_server = self.server_controller.create_server(
            name="OpenAI Tools Server",
            url="https://mcp.openai.com/sse",
            icon_type="purple_dot",
            subtitle="3 sources",
        )

        custom_server = self.server_controller.create_server(
            name="Custom MCP Server",
            url="https://custom-mcp.example.com/sse",
            icon_type="red_dot",
            subtitle="Claude Desktop",
        )

        # Add some tools to the servers
        self.server_controller.add_tool_to_server(neon_server.id, "listProjects")
        self.server_controller.add_tool_to_server(neon_server.id, "createDatabase")
        self.server_controller.add_tool_to_server(neon_server.id, "runQuery")

        # Create some sample sources
        claude_source = self.source_controller.create_source(
            name="Claude Desktop",
            path="/Users/user/.config/claude-desktop/mcp.json",
            icon_type="purple_dot",
        )

        vscode_source = self.source_controller.create_source(
            name="VS Code",
            path="/Users/user/.vscode/extensions/anthropic.claude-1.0.0/mcp.json",
            icon_type="blue_dot",
        )

        cursor_source = self.source_controller.create_source(
            name="Cursor",
            path="/Applications/Cursor.app/Contents/Resources/mcp.json",
            icon_type="green_dot",
        )

        windsurf_source = self.source_controller.create_source(
            name="Windsurf",
            path="/Users/user/.windsurf/mcp.json",
            icon_type="orange_dot",
        )

        # Connect sources to servers
        self.server_controller.add_source_to_server(neon_server.id, claude_source)
        self.server_controller.add_source_to_server(neon_server.id, cursor_source)
        self.server_controller.add_source_to_server(local_server.id, vscode_source)
        self.server_controller.add_source_to_server(custom_server.id, claude_source)

        # Select the Neon server by default
        self.server_controller.select_server(neon_server.id)

    def load_servers(self):
        """Load servers from the controller into the list widget"""
        # Clear the list first
        self.server_list.clear()

        # Get all servers from the controller
        servers = self.server_controller.get_all_servers()

        # Add each server to the list
        for server in servers:
            ServerItem(self.server_list, server.name, server.subtitle, server.icon_type)

        # Get the selected server or select the first one if none is selected
        selected_server = self.server_controller.get_selected_server()
        if selected_server is None and servers:
            # Select the first server
            self.server_controller.select_server(servers[0].id)
            selected_server = servers[0]

        # Select the corresponding item in the list
        if selected_server:
            # Find the item with the matching name
            for i in range(self.server_list.count()):
                item = self.server_list.item(i)
                if item.text() == selected_server.name:
                    self.server_list.setCurrentItem(item)
                    break

        # Update the server details
        self.update_server_details()

    def filter_servers(self, text):
        """Filter the server list based on search text"""
        for i in range(self.server_list.count()):
            item = self.server_list.item(i)

            # Check if the server name contains the search text
            if text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def on_server_selected(self, item):
        """Handle selection of a server from the list"""
        if not item:
            return

        # Find the server with the matching name
        server_name = item.text()
        for server in self.server_controller.get_all_servers():
            if server.name == server_name:
                # Select the server in the controller
                self.server_controller.select_server(server.id)
                # Update the UI
                self.update_server_details()
                break

    def create_content_area(self):
        """Create the main content area showing server details"""
        # Create content widget and layout
        self.server_content = QWidget()
        self.server_content_layout = QVBoxLayout(self.server_content)
        self.server_content_layout.setContentsMargins(25, 25, 25, 25)
        self.server_content_layout.setSpacing(20)

        # Create server details sections
        self.create_server_details()

    def create_server_details(self):
        """Create all sections of the server details view"""
        # Create server title section
        self.create_server_title()

        # Create server link section - with placeholder values initially
        self.server_link_section = DetailSection(
            parent=self.server_content,
            parent_layout=self.server_content_layout,
            label_text="Server Link:",
            value_text="https://example.com",
            object_name="server_link_section",
            icon_text="🔗",  # Link icon
        )
        self.server_link_field = self.server_link_section.value

        # Create command section - with placeholder values initially
        self.command_section = DetailSection(
            parent=self.server_content,
            parent_layout=self.server_content_layout,
            label_text="Command:",
            value_text="npx -y mcp-remote https://example.com",
            object_name="command_section",
            icon_text="⌘",  # Command icon
        )
        self.command_field = self.command_section.value

        # Create tools section
        self.create_tools_section()

        # Create sources section
        self.create_sources_section()

    def create_server_title(self):
        """Create the server title section"""
        # Title widget and layout
        self.server_title_widget = QWidget()
        self.server_title_layout = QHBoxLayout(self.server_title_widget)
        self.server_title_layout.setContentsMargins(0, 0, 0, 5)

        # Server icon and name
        self.server_icon = QLabel("●")
        self.server_icon.setObjectName("green_dot")  # Default, will be updated

        self.server_name = QLabel("Server Name")  # Default, will be updated
        self.server_name.setObjectName("server_name")

        # Edit button
        self.edit_button = QPushButton("✎ Edit")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.clicked.connect(self.edit_server)

        # Add to layout
        self.server_title_layout.addWidget(self.server_icon)
        self.server_title_layout.addWidget(self.server_name)
        self.server_title_layout.addStretch()
        self.server_title_layout.addWidget(self.edit_button)

        # Add to content layout
        self.server_content_layout.addWidget(self.server_title_widget)

    def edit_server(self):
        """Handle the Edit button click"""
        server = self.server_controller.get_selected_server()
        if not server:
            return

        print(f"Editing server: {server.name}")
        # In a real app, this would open a dialog to edit the server

    def create_tools_section(self):
        """Create the tools section"""
        # Container widget and layout
        self.tools_widget = QWidget()
        self.tools_widget.setObjectName("section_container")
        self.tools_layout = QVBoxLayout(self.tools_widget)

        # Header with icon and label
        self.tools_header = QWidget()
        self.tools_header_layout = QHBoxLayout(self.tools_header)
        self.tools_header_layout.setContentsMargins(0, 0, 0, 10)

        self.tools_icon = QLabel("🔧")  # Tool icon
        self.tools_icon.setObjectName("section_icon")

        self.tools_label = QLabel("Tools:")
        self.tools_label.setObjectName("section_label")

        self.tools_header_layout.addWidget(self.tools_icon)
        self.tools_header_layout.addWidget(self.tools_label)
        self.tools_header_layout.addStretch()

        # Tools buttons
        self.tools_buttons_widget = QWidget()
        self.tools_buttons_layout = QHBoxLayout(self.tools_buttons_widget)
        self.tools_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.tools_buttons_layout.setSpacing(10)

        # Buttons will be added dynamically in update_tools()

        # Add components to tools layout
        self.tools_layout.addWidget(self.tools_header)
        self.tools_layout.addWidget(self.tools_buttons_widget)

        # Add to content layout
        self.server_content_layout.addWidget(self.tools_widget)

    def update_tools(self, server):
        """Update the tools section with the server's tools"""
        # Clear existing tools
        for i in reversed(range(self.tools_buttons_layout.count())):
            item = self.tools_buttons_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        # Add the server's tools
        for tool in server.tools:
            button = QPushButton(tool)
            button.setObjectName("tool_button")
            button.clicked.connect(lambda checked=False, t=tool: self.execute_tool(t))
            self.tools_buttons_layout.addWidget(button)

        # Add stretch at the end
        self.tools_buttons_layout.addStretch()

    def execute_tool(self, tool):
        """Execute a tool on the selected server"""
        print(f"Executing tool: {tool}")
        # In a real app, this would execute the tool via the controller

    def create_sources_section(self):
        """Create the sources section with cards"""
        # Container widget and layout
        self.sources_widget = QWidget()
        self.sources_widget.setObjectName("section_container")
        self.sources_layout = QVBoxLayout(self.sources_widget)

        # Header widget and layout
        self.sources_header = QWidget()
        self.sources_header_layout = QHBoxLayout(self.sources_header)
        self.sources_header_layout.setContentsMargins(0, 0, 0, 20)

        # Header icon and label
        self.sources_icon = QLabel("📱")  # Sources icon
        self.sources_icon.setObjectName("section_icon")

        self.sources_label = QLabel("Sources:")
        self.sources_label.setObjectName("section_label")

        # Action buttons
        self.sources_actions = QWidget()
        self.sources_actions_layout = QHBoxLayout(self.sources_actions)
        self.sources_actions_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_actions_layout.setSpacing(10)

        self.remove_from_all_button = QPushButton("Remove from all")
        self.remove_from_all_button.setObjectName("action_button")
        self.remove_from_all_button.clicked.connect(self.remove_from_all)

        self.sync_to_all_button = QPushButton("Sync to all")
        self.sync_to_all_button.setObjectName("action_button")
        self.sync_to_all_button.clicked.connect(self.sync_to_all)

        # Add buttons to actions layout
        self.sources_actions_layout.addWidget(self.remove_from_all_button)
        self.sources_actions_layout.addWidget(self.sync_to_all_button)

        # Add components to header layout
        self.sources_header_layout.addWidget(self.sources_icon)
        self.sources_header_layout.addWidget(self.sources_label)
        self.sources_header_layout.addStretch()
        self.sources_header_layout.addWidget(self.sources_actions)

        # Sources grid for cards
        self.sources_grid = QWidget()
        self.sources_grid_layout = QGridLayout(self.sources_grid)
        self.sources_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_grid_layout.setSpacing(16)

        # Cards will be added dynamically in update_sources()

        # Add components to sources layout
        self.sources_layout.addWidget(self.sources_header)
        self.sources_layout.addWidget(self.sources_grid)

        # Add to content layout
        self.server_content_layout.addWidget(self.sources_widget)
        self.server_content_layout.addStretch()

    def update_sources(self, server):
        """Update the sources section with the server's sources"""
        # Clear existing sources from the grid
        for i in reversed(range(self.sources_grid_layout.count())):
            item = self.sources_grid_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()

        # Get all sources
        all_sources = self.source_controller.get_all_sources()
        server_sources = server.sources

        # Add source cards
        row, col = 0, 0
        for source in all_sources:
            status = "Added" if source in server_sources else "Not Added"
            card = SourceCard("●", source.name, status, source.icon_type)
            self.sources_grid_layout.addWidget(card, row, col)

            # Move to next column or row
            col += 1
            if col > 1:
                col = 0
                row += 1

    def remove_from_all(self):
        """Remove selected server from all sources"""
        server = self.server_controller.get_selected_server()
        if not server:
            return

        # Get all sources
        sources = server.sources.copy()  # Copy to avoid modification during iteration

        # Remove server from each source
        for source in sources:
            self.source_controller.remove_source_from_server_config(source.id, server)

        # Update the UI
        self.update_server_details()
        print(f"Removed {server.name} from all sources")

    def sync_to_all(self):
        """Sync selected server to all sources"""
        server = self.server_controller.get_selected_server()
        if not server:
            return

        # Get all sources
        all_sources = self.source_controller.get_all_sources()

        # Sync server to each source
        for source in all_sources:
            self.source_controller.sync_source_to_server(source.id, server)

        # Update the UI
        self.update_server_details()
        print(f"Synced {server.name} to all sources")

    def update_server_details(self):
        """Update the UI with the selected server's details"""
        server = self.server_controller.get_selected_server()
        if not server:
            return

        # Update server title
        self.server_name.setText(server.name)

        # Update icon
        old_class = self.server_icon.objectName()
        self.server_icon.setObjectName(server.icon_type)
        if old_class != server.icon_type:
            self.server_icon.style().polish(self.server_icon)

        # Update server link
        self.server_link_field.setText(server.url)

        # Update command
        self.command_field.setText(server.command)

        # Update tools
        self.update_tools(server)

        # Update sources
        self.update_sources(server)
