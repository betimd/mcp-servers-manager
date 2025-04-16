"""
Server Sources view for the MCP Server Manager
"""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from ui.custom_widgets.source_item import SourceItem
from ui.styles import apply_server_sources_styles


class ServerSourcesView(QWidget):
    """Server Sources view with list of all sources"""

    def __init__(self):
        super().__init__()

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        self.layout.setSpacing(20)

        # Create content
        self.create_header()
        self.create_sources_list()

        # Apply styles
        apply_server_sources_styles(self)

    def create_header(self):
        """Create the view header with title and add button"""
        # Title and subtitle
        self.sources_title = QLabel("Server Sources")
        self.sources_title.setObjectName("page_title")

        self.sources_subtitle = QLabel(
            "Manage MCP server sources from different applications"
        )
        self.sources_subtitle.setObjectName("page_subtitle")

        # Header widget with title/subtitle and add button
        self.sources_header = QWidget()
        self.sources_header_layout = QHBoxLayout(self.sources_header)
        self.sources_header_layout.setContentsMargins(0, 0, 0, 30)

        # Title and subtitle container
        self.sources_title_container = QWidget()
        self.sources_title_layout = QVBoxLayout(self.sources_title_container)
        self.sources_title_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_title_layout.setSpacing(5)
        self.sources_title_layout.addWidget(self.sources_title)
        self.sources_title_layout.addWidget(self.sources_subtitle)

        # Add source button
        self.add_source_button = QPushButton("+ Add Source")
        self.add_source_button.setObjectName("add_button")
        self.add_source_button.clicked.connect(self.add_source)

        # Add to header layout
        self.sources_header_layout.addWidget(self.sources_title_container)
        self.sources_header_layout.addStretch()
        self.sources_header_layout.addWidget(self.add_source_button)

        # Add header to main layout
        self.layout.addWidget(self.sources_header)

    def create_sources_list(self):
        """Create the scrollable list of source items"""
        # Create scrollable area for source list
        self.sources_scroll = QScrollArea()
        self.sources_scroll.setWidgetResizable(True)
        self.sources_scroll.setFrameShape(QScrollArea.NoFrame)

        # Scroll content widget and layout
        self.sources_scroll_content = QWidget()
        self.sources_scroll_layout = QVBoxLayout(self.sources_scroll_content)
        self.sources_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_scroll_layout.setSpacing(16)

        # Add source items
        self.add_source_items()

        # Add stretch to push items to the top
        self.sources_scroll_layout.addStretch()

        # Set scroll content and add to layout
        self.sources_scroll.setWidget(self.sources_scroll_content)
        self.layout.addWidget(self.sources_scroll, 1)  # 1 is stretch factor

    def add_source_items(self):
        """Add sample source items to the list"""
        # Add sample items
        self.claude_item = SourceItem(
            icon_text="●",
            name="Claude Desktop",
            path="/Users/user/.config/claude-desktop/mcp.json",
            icon_class="purple_dot",
            on_edit=lambda: print("Edit Claude Desktop clicked"),
            on_delete=lambda: print("Delete Claude Desktop clicked"),
        )

        self.vscode_item = SourceItem(
            icon_text="✓",
            name="VS Code",
            path="/Users/user/.vscode/extensions/anthropic.claude-1.0.0/mcp.json",
            icon_class="blue_dot",
            on_edit=lambda: print("Edit VS Code clicked"),
            on_delete=lambda: print("Delete VS Code clicked"),
        )

        self.cursor_item = SourceItem(
            icon_text="►",
            name="Cursor",
            path="/Applications/Cursor.app/Contents/Resources/mcp.json",
            icon_class="green_dot",
            on_edit=lambda: print("Edit Cursor clicked"),
            on_delete=lambda: print("Delete Cursor clicked"),
        )

        self.windsurf_item = SourceItem(
            icon_text="♦",
            name="Windsurf",
            path="/Users/user/.windsurf/mcp.json",
            icon_class="orange_dot",
            on_edit=lambda: print("Edit Windsurf clicked"),
            on_delete=lambda: print("Delete Windsurf clicked"),
        )

        # Add items to layout
        self.sources_scroll_layout.addWidget(self.claude_item)
        self.sources_scroll_layout.addWidget(self.vscode_item)
        self.sources_scroll_layout.addWidget(self.cursor_item)
        self.sources_scroll_layout.addWidget(self.windsurf_item)

    def add_source(self):
        """Handle the Add Source button click"""
        print("Add Source clicked")
        # In a real app, this would open a dialog to add a new source
