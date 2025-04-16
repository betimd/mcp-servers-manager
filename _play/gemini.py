import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


# --- Placeholder Icon Generation ---
# In a real app, use QIcon.fromTheme or load from files/resources
def create_placeholder_icon(color, size=16):
    """Creates a square QPixmap filled with a specified color."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)  # Start with transparency
    painter = QPainter(pixmap)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.PenStyle.NoPen)
    # Draw a circle instead of square for dots
    if size <= 20:  # Assume small sizes are dots
        painter.drawEllipse(0, 0, size - 1, size - 1)
    else:
        painter.drawRect(0, 0, size, size)

    # Simple text initials for some icons if color isn't enough
    if color == "gray":  # Placeholder for Copy/Edit/Delete etc.
        painter.setPen(QColor("black"))
        font = QFont()
        font.setPointSize(size * 0.6)
        painter.setFont(font)
        # Could add text based on context, but hard here. Let's skip for generic gray.
        pass  # Keep it simple: just a colored shape
    elif isinstance(color, str) and color.startswith(
        "#"
    ):  # Hex colors often used for specific items
        pass  # Just use the color

    painter.end()
    return QIcon(pixmap)


def create_text_icon(text, size=16):
    """Creates a QIcon with simple text (for placeholders like GitHub link)."""
    pixmap = QPixmap(size * len(text), size)  # Adjust width roughly based on text
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    font = QFont()
    font.setPointSize(size * 5)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text)
    painter.end()
    return QIcon(pixmap)


# --- Custom Widgets ---


class ServerListItemWidget(QWidget):
    """Custom widget for server list items."""

    def __init__(self, icon_color, name, sources_info, is_selected=False):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(
            create_placeholder_icon(icon_color, 12).pixmap(QSize(12, 12))
        )
        layout.addWidget(icon_label)

        # Text Info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(0)
        name_label = QLabel(name)
        font = name_label.font()
        font.setBold(True)
        name_label.setFont(font)
        sources_label = QLabel(sources_info)
        font = sources_label.font()
        font.setPointSize(font.pointSize() - 1)
        sources_label.setFont(font)
        sources_label.setStyleSheet("color: gray;")

        text_layout.addWidget(name_label)
        text_layout.addWidget(sources_label)
        layout.addLayout(text_layout)

        layout.addStretch()

        # Selection Indicator (simple > character)
        self.selection_indicator = QLabel(">" if is_selected else "")
        self.selection_indicator.setFixedWidth(15)
        self.selection_indicator.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.selection_indicator.setStyleSheet("color: gray; font-weight: bold;")
        layout.addWidget(self.selection_indicator)

        # Background color handled by QListWidget's selection model + stylesheet

    def set_selected(self, selected):
        self.selection_indicator.setText(">" if selected else "")
        # Update background/style if needed, though usually handled by list view selection
        # self.setStyleSheet("background-color: #e0e0e0;" if selected else "background-color: none;")


class SourceCardWidget(QWidget):
    """Card for displaying a source in the Server View."""

    def __init__(self, icon_color_or_char, name, status, is_added):
        super().__init__()
        self.setAutoFillBackground(True)  # Important for background color styling
        self.setMinimumHeight(60)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Icon
        icon_label = QLabel()
        if (
            isinstance(icon_color_or_char, str) and len(icon_color_or_char) > 1
        ):  # Check if it's a color string
            icon_label.setPixmap(
                create_placeholder_icon(icon_color_or_char, 12).pixmap(QSize(12, 12))
            )
        else:  # Assume it's a character/symbol
            icon_label.setText(icon_color_or_char)  # Example: using checkmark symbol
            icon_label.setStyleSheet(
                "color: blue; font-size: 16px; font-weight: bold;"
            )  # Style checkmark

        icon_label.setFixedSize(QSize(16, 16))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        # Name
        name_label = QLabel(name)
        layout.addWidget(name_label)

        layout.addStretch()

        # Status
        status_label = QLabel(status)
        status_style = (
            "color: green; font-weight: bold;" if is_added else "color: gray;"
        )
        status_label.setStyleSheet(status_style)
        layout.addWidget(status_label)

        self.setObjectName("SourceCard")  # For styling


class SourceConfigCardWidget(QWidget):
    """Card for displaying a source configuration in the Server Sources View."""

    def __init__(self, icon_color, name, path):
        super().__init__()
        self.setAutoFillBackground(True)
        self.setObjectName("ConfigCard")  # For styling

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(
            create_placeholder_icon(icon_color, 20).pixmap(QSize(20, 20))
        )
        layout.addWidget(icon_label)

        # Info (Name + Path)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        name_label = QLabel(name)
        font = name_label.font()
        font.setPointSize(font.pointSize() + 1)
        font.setBold(True)
        name_label.setFont(font)
        path_label = QLabel(path)
        path_label.setStyleSheet("color: gray;")
        path_label.setWordWrap(True)  # Allow path wrapping

        info_layout.addWidget(name_label)
        info_layout.addWidget(path_label)
        layout.addLayout(info_layout)

        layout.addStretch()

        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        edit_button = QPushButton("Edit")  # Placeholder text, use icons in real app
        edit_button.setIcon(create_text_icon("✏️"))  # Placeholder icon
        edit_button.setObjectName("IconButton")
        edit_button.setFlat(True)
        edit_button.setToolTip("Edit Source")
        edit_button.clicked.connect(lambda: print(f"Edit {name}"))

        delete_button = QPushButton("Delete")  # Placeholder text
        delete_button.setIcon(create_text_icon("🗑️"))  # Placeholder icon
        delete_button.setObjectName("IconButton")
        delete_button.setFlat(True)
        delete_button.setToolTip("Delete Source")
        delete_button.setStyleSheet(
            "QPushButton#IconButton { color: red; }"
        )  # Style delete distinctly
        delete_button.clicked.connect(lambda: print(f"Delete {name}"))

        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)


# --- Main Application Window ---


class MCPManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCP Server Manager")
        self.setGeometry(100, 100, 1000, 700)  # Adjusted size

        self.current_server_list_item = None  # To track selected item widget

        # --- Central Widget and Layout ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # --- Create UI Sections ---
        self.create_header()
        self.create_main_content_area()
        self.create_footer()

        # --- Add Sections to Main Layout ---
        self.main_layout.addWidget(self.header_widget)
        self.main_layout.addWidget(self.stacked_widget, 1)  # Make content area stretch
        self.main_layout.addWidget(self.footer_widget)

        # --- Apply Stylesheet ---
        self.apply_styles()

        # --- Initial State ---
        self.show_server_view()  # Start with the server view

    def create_header(self):
        self.header_widget = QWidget()
        self.header_widget.setObjectName("Header")
        header_layout = QHBoxLayout(self.header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)

        title_label = QLabel("MCP Server Manager")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        dashboard_button = QPushButton("Dashboard")
        dashboard_button.setFlat(True)
        dashboard_button.clicked.connect(self.show_server_view)

        sources_button = QPushButton("Server Sources")
        sources_button.setFlat(True)
        sources_button.clicked.connect(self.show_server_sources_view)

        github_button = QPushButton("GitHub")
        github_button.setFlat(True)
        github_button.setIcon(create_text_icon("↗"))  # Placeholder external link icon
        github_button.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft
        )  # Icon on right
        github_button.clicked.connect(lambda: print("Open GitHub link"))

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(dashboard_button)
        header_layout.addWidget(sources_button)
        header_layout.addWidget(github_button)

    def create_footer(self):
        self.footer_widget = QWidget()
        self.footer_widget.setObjectName("Footer")
        footer_layout = QHBoxLayout(self.footer_widget)
        footer_layout.setContentsMargins(20, 10, 20, 10)

        copyright_label = QLabel("© 2025 MCP Server Manager. All rights reserved.")
        copyright_label.setStyleSheet("color: gray;")

        doc_button = QPushButton("Documentation")
        doc_button.setFlat(True)
        doc_button.clicked.connect(lambda: print("Open Documentation"))

        github_button = QPushButton("GitHub")
        github_button.setFlat(True)
        github_button.clicked.connect(lambda: print("Open GitHub link"))

        support_button = QPushButton("Support")
        support_button.setFlat(True)
        support_button.clicked.connect(lambda: print("Open Support"))

        footer_layout.addWidget(copyright_label)
        footer_layout.addStretch()
        footer_layout.addWidget(doc_button)
        footer_layout.addWidget(github_button)
        footer_layout.addWidget(support_button)

    def create_main_content_area(self):
        self.stacked_widget = QStackedLayout()
        self.stacked_widget.setContentsMargins(
            0, 0, 0, 0
        )  # No margins for the stack itself

        # --- Page 1: Server View ---
        self.server_view_page = QWidget()
        server_view_layout = QHBoxLayout(self.server_view_page)
        server_view_layout.setContentsMargins(0, 0, 0, 0)
        server_view_layout.setSpacing(0)

        self.create_sidebar()
        self.create_server_content_area()  # Initially for "Neon MCP Server"

        server_view_layout.addWidget(self.sidebar_widget)
        server_view_layout.addWidget(
            self.server_content_area_widget, 1
        )  # Content area takes more space

        # --- Page 2: Server Sources View ---
        self.server_sources_page = QWidget()
        self.server_sources_page.setObjectName("ServerSourcesPage")
        server_sources_layout = QVBoxLayout(self.server_sources_page)
        server_sources_layout.setContentsMargins(
            20, 20, 20, 20
        )  # Padding for this page content
        server_sources_layout.setSpacing(15)
        self.create_server_sources_content()  # Create the content for this page
        server_sources_layout.addWidget(self.server_sources_content_widget)

        # --- Add pages to stack ---
        self.stacked_widget.addWidget(self.server_view_page)
        self.stacked_widget.addWidget(self.server_sources_page)

    def create_sidebar(self):
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setObjectName("Sidebar")
        self.sidebar_widget.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        sidebar_layout.setContentsMargins(10, 15, 10, 15)
        sidebar_layout.setSpacing(10)

        search_box = QLineEdit()
        search_box.setPlaceholderText("Search servers...")
        sidebar_layout.addWidget(search_box)

        servers_label = QLabel("SERVERS")
        servers_label.setStyleSheet(
            "color: gray; font-size: 10px; font-weight: bold; margin-top: 10px;"
        )
        sidebar_layout.addWidget(servers_label)

        self.server_list = QListWidget()
        self.server_list.setObjectName("ServerList")
        self.server_list.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )  # As per design
        self.server_list.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.server_list.setSpacing(2)

        # --- Populate Server List (using custom widgets) ---
        servers_data = [
            {
                "color": "#66CC66",
                "name": "Neon MCP Server",
                "info": "2 sources",
                "selected": True,
            },  # Neon Greenish
            {
                "color": "#3399FF",
                "name": "Local Development MCP",
                "info": "VS Code",
                "selected": False,
            },  # Blueish
            {
                "color": "#CC66FF",
                "name": "OpenAI Tools Server",
                "info": "3 sources",
                "selected": False,
            },  # Purpleish
            {
                "color": "#FF6666",
                "name": "Custom MCP Server",
                "info": "Claude Desktop",
                "selected": False,
            },  # Reddish
        ]

        for i, server in enumerate(servers_data):
            item = QListWidgetItem(self.server_list)
            widget = ServerListItemWidget(
                server["color"], server["name"], server["info"], server["selected"]
            )
            item.setSizeHint(widget.sizeHint())
            self.server_list.addItem(item)
            self.server_list.setItemWidget(item, widget)
            if server["selected"]:
                self.server_list.setCurrentRow(i)
                self.current_server_list_item = item  # Track initially selected

        self.server_list.currentItemChanged.connect(self.on_server_selected)
        sidebar_layout.addWidget(self.server_list)
        sidebar_layout.addStretch()  # Pushes list up if space allows

    def on_server_selected(self, current_item, previous_item):
        if previous_item:
            prev_widget = self.server_list.itemWidget(previous_item)
            if isinstance(prev_widget, ServerListItemWidget):
                prev_widget.set_selected(False)

        if current_item:
            current_widget = self.server_list.itemWidget(current_item)
            if isinstance(current_widget, ServerListItemWidget):
                current_widget.set_selected(True)
                # --- Update Content Area ---
                # In a real app, load data for the selected server here.
                # For now, just change the title and maybe icon color.
                server_name = current_widget.findChild(
                    QLabel
                ).text()  # Simple way to get name back
                self.update_server_content_title(
                    server_name, current_widget.icon_label.pixmap()
                )  # Pass pixmap
                print(f"Selected server: {server_name}")
                # Ensure we are on the server view page when a server is clicked
                self.show_server_view()

            self.current_server_list_item = current_item

    def create_server_content_area(self):
        """Creates the right panel content for the selected server view."""
        self.server_content_area_widget = QWidget()
        self.server_content_area_widget.setObjectName("ContentArea")
        main_layout = QVBoxLayout(self.server_content_area_widget)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(20)

        # --- Title Section ---
        title_layout = QHBoxLayout()
        title_layout.setSpacing(10)
        self.server_icon_label = QLabel()
        self.server_icon_label.setPixmap(
            create_placeholder_icon("#66CC66", 16).pixmap(QSize(16, 16))
        )  # Initial: Neon Green
        self.server_title_label = QLabel("Neon MCP Server")
        font = self.server_title_label.font()
        font.setPointSize(font.pointSize() + 4)
        font.setBold(True)
        self.server_title_label.setFont(font)
        edit_button = QPushButton("Edit")
        edit_button.setIcon(create_text_icon("✏️"))  # Placeholder icon
        edit_button.setObjectName("OutlineButton")  # Style as less prominent button
        edit_button.clicked.connect(lambda: print("Edit Server clicked"))

        title_layout.addWidget(self.server_icon_label)
        title_layout.addWidget(self.server_title_label)
        title_layout.addStretch()
        title_layout.addWidget(edit_button)
        main_layout.addLayout(title_layout)

        # --- Server Link Section ---
        link_frame = QFrame()
        link_frame.setObjectName("InfoFrame")
        link_layout = QVBoxLayout(link_frame)
        link_layout.setSpacing(8)
        link_label = QLabel("Server Link:")
        link_content_layout = QHBoxLayout()
        link_input = QLineEdit("https://mcp.neon.tech/sse")
        link_input.setReadOnly(True)
        link_input.setObjectName("ReadOnlyInput")
        copy_link_button = QPushButton()
        copy_link_button.setIcon(create_text_icon("[C]"))  # Placeholder icon
        copy_link_button.setToolTip("Copy Link")
        copy_link_button.setObjectName("IconButton")
        copy_link_button.setFlat(True)
        copy_link_button.clicked.connect(lambda: print("Copy Link clicked"))
        link_content_layout.addWidget(link_input, 1)
        link_content_layout.addWidget(copy_link_button)
        link_layout.addWidget(link_label)
        link_layout.addLayout(link_content_layout)
        main_layout.addWidget(link_frame)

        # --- Command Section ---
        cmd_frame = QFrame()
        cmd_frame.setObjectName("InfoFrame")
        cmd_layout = QVBoxLayout(cmd_frame)
        cmd_layout.setSpacing(8)
        cmd_label = QLabel("Command:")
        cmd_content_layout = QHBoxLayout()
        cmd_input = QLineEdit("npx -y mcp-remote https://mcp.neon.tech/sse")
        cmd_input.setReadOnly(True)
        cmd_input.setObjectName("ReadOnlyInput")
        copy_cmd_button = QPushButton()
        copy_cmd_button.setIcon(create_text_icon("[C]"))  # Placeholder icon
        copy_cmd_button.setToolTip("Copy Command")
        copy_cmd_button.setObjectName("IconButton")
        copy_cmd_button.setFlat(True)
        copy_cmd_button.clicked.connect(lambda: print("Copy Command clicked"))
        cmd_content_layout.addWidget(cmd_input, 1)
        cmd_content_layout.addWidget(copy_cmd_button)
        cmd_layout.addWidget(cmd_label)
        cmd_layout.addLayout(cmd_content_layout)
        main_layout.addWidget(cmd_frame)

        # --- Tools Section ---
        tools_frame = QFrame()
        tools_frame.setObjectName("InfoFrame")
        tools_layout = QVBoxLayout(tools_frame)
        tools_layout.setSpacing(10)
        tools_label = QLabel("Tools:")
        tools_button_layout = QHBoxLayout()
        tools_button_layout.setSpacing(10)
        tools = ["listProjects", "createDatabase", "runQuery"]
        for tool in tools:
            btn = QPushButton(tool)
            btn.setObjectName("ToolButton")
            btn.clicked.connect(
                lambda checked=False, t=tool: print(f"Tool '{t}' clicked")
            )
            tools_button_layout.addWidget(btn)
        tools_button_layout.addStretch()  # Align buttons left

        tools_layout.addWidget(tools_label)
        tools_layout.addLayout(tools_button_layout)
        main_layout.addWidget(tools_frame)

        # --- Sources Section ---
        sources_frame = QFrame()
        sources_frame.setObjectName("InfoFrame")
        sources_main_layout = QVBoxLayout(sources_frame)
        sources_main_layout.setSpacing(10)

        # Header: Label + Control Buttons
        sources_header_layout = QHBoxLayout()
        sources_label = QLabel("Sources:")
        remove_all_button = QPushButton("Remove from all")
        remove_all_button.setIcon(create_text_icon("🗑️"))  # Placeholder
        remove_all_button.setStyleSheet("color: red;")  # Destructive action
        remove_all_button.clicked.connect(lambda: print("Remove from all clicked"))

        sync_all_button = QPushButton("Sync to all")
        sync_all_button.setIcon(create_text_icon("🔄"))  # Placeholder
        sync_all_button.clicked.connect(lambda: print("Sync to all clicked"))

        sources_header_layout.addWidget(sources_label)
        sources_header_layout.addStretch()
        sources_header_layout.addWidget(remove_all_button)
        sources_header_layout.addWidget(sync_all_button)
        sources_main_layout.addLayout(sources_header_layout)

        # Grid for Source Cards
        self.sources_grid_layout = QGridLayout()
        self.sources_grid_layout.setSpacing(15)
        sources_main_layout.addLayout(self.sources_grid_layout)

        self.populate_sources_grid()  # Add placeholder sources

        main_layout.addWidget(sources_frame)
        main_layout.addStretch()  # Push content up

    def update_server_content_title(self, name, icon_pixmap):
        """Updates the title section of the server content area."""
        self.server_title_label.setText(name)
        if icon_pixmap:
            self.server_icon_label.setPixmap(
                icon_pixmap.scaled(
                    16,
                    16,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        # Here you would also reload link, command, tools, sources based on the server 'name'

    def populate_sources_grid(self):
        """Populates the sources grid with placeholder cards."""
        # Clear existing widgets if necessary (important for updates)
        while self.sources_grid_layout.count():
            item = self.sources_grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add new source cards (example data)
        # Data should be fetched based on the *currently selected server*
        # For this example, we'll use static data simulating the "Neon MCP Server" view
        sources = [
            {
                "icon": "#CC66FF",
                "name": "Claude Desktop",
                "status": "Added",
                "added": True,
            },
            {
                "icon": "✓",
                "name": "VS Code",
                "status": "Not Added",
                "added": False,
            },  # Using checkmark symbol placeholder
            {
                "icon": "#33CC99",
                "name": "Cursor",
                "status": "Added",
                "added": True,
            },  # Teal-ish for Cursor
            {
                "icon": "#FFA500",
                "name": "Windsurf",
                "status": "Not Added",
                "added": False,
            },  # Orange for Windsurf
        ]

        row, col = 0, 0
        max_cols = 2  # As shown in mockup
        for src in sources:
            card = SourceCardWidget(
                src["icon"], src["name"], src["status"], src["added"]
            )
            self.sources_grid_layout.addWidget(card, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        self.sources_grid_layout.setRowStretch(row + 1, 1)  # Add stretch to the bottom
        self.sources_grid_layout.setColumnStretch(
            max_cols, 1
        )  # Add stretch to the right

    def create_server_sources_content(self):
        """Creates the content widget for the Server Sources page."""
        self.server_sources_content_widget = QWidget()
        layout = QVBoxLayout(self.server_sources_content_widget)
        layout.setContentsMargins(
            0, 0, 0, 0
        )  # Margins controlled by parent page layout
        layout.setSpacing(15)

        # --- Title and Add Button ---
        header_layout = QHBoxLayout()
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        title = QLabel("Server Sources")
        font = title.font()
        font.setPointSize(font.pointSize() + 4)
        font.setBold(True)
        title.setFont(font)
        subtitle = QLabel("Manage MCP server sources from different applications")
        subtitle.setStyleSheet("color: gray;")
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        add_source_button = QPushButton("Add Source")
        add_source_button.setIcon(create_text_icon("+"))  # Placeholder
        add_source_button.setObjectName("PrimaryButton")  # Style as primary action
        add_source_button.clicked.connect(lambda: print("Add Source clicked"))

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(add_source_button)
        layout.addLayout(header_layout)

        # --- Scroll Area for Source Cards ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("ScrollArea")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.sources_list_layout = QVBoxLayout(scroll_content)
        self.sources_list_layout.setContentsMargins(
            0, 0, 0, 0
        )  # Let cards handle padding
        self.sources_list_layout.setSpacing(10)

        # Add source config cards (placeholder data)
        sources_data = [
            {
                "icon": "#CC66FF",
                "name": "Claude Desktop",
                "path": "/Users/user/.config/claude-desktop/mcp.json",
            },
            {
                "icon": "#3399FF",
                "name": "VS Code",
                "path": "/Users/user/.vscode/extensions/anthropic.claude-1.0.0/mcp.json",
            },
            {
                "icon": "#33CC99",
                "name": "Cursor",
                "path": "/Applications/Cursor.app/Contents/Resources/mcp.json",
            },
            {
                "icon": "#FFA500",
                "name": "Windsurf",
                "path": "(No config file found - Built-in?)",
            },  # Example
        ]
        for src in sources_data:
            card = SourceConfigCardWidget(src["icon"], src["name"], src["path"])
            self.sources_list_layout.addWidget(card)

        self.sources_list_layout.addStretch()  # Push cards up

        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area, 1)  # Make scroll area take remaining space

    # --- Navigation Methods ---
    def show_server_view(self):
        self.stacked_widget.setCurrentIndex(0)
        print("Navigated to Server View")

    def show_server_sources_view(self):
        self.stacked_widget.setCurrentIndex(1)
        print("Navigated to Server Sources View")

    # --- Styling ---
    def apply_styles(self):
        style = """
            QMainWindow {{
                background-color: #f8f9fa; /* Light background */
            }}
            QWidget#Header {{
                background-color: white;
                border-bottom: 1px solid #dee2e6;
            }}
            QWidget#Footer {{
                background-color: white;
                border-top: 1px solid #dee2e6;
            }}
            QWidget#Sidebar {{
                background-color: #f1f3f5; /* Slightly darker than main bg */
                border-right: 1px solid #dee2e6;
            }}
            QWidget#ContentArea {{
                background-color: #f8f9fa; /* Match main bg */
            }}
            QWidget#ServerSourcesPage {{
                background-color: #f8f9fa; /* Match main bg */
            }}

            /* Server List in Sidebar */
            QListWidget#ServerList {{
                border: none;
                background-color: transparent; /* Inherit sidebar bg */
            }}
            QListWidget#ServerList::item {{
                 /* Padding/margin handled by custom widget */
                 border-radius: 4px;
                 margin-bottom: 2px; /* Spacing between items */
            }}
             QListWidget#ServerList::item:selected {{
                 background-color: #e9ecef; /* Highlight selection */
             }}
            QListWidget#ServerList::item:hover {{
                 background-color: #f1f3f5; /* Hover effect */
             }}


            /* General Button Styles */
            QPushButton {{
                border: 1px solid #ced4da;
                padding: 5px 10px;
                background-color: white;
                border-radius: 4px;
                min-height: 20px; /* Ensure buttons have some height */
            }}
            QPushButton:hover {{
                background-color: #f8f9fa;
            }}
            QPushButton:pressed {{
                background-color: #e9ecef;
            }}
            QPushButton:flat {{
                border: none;
                background-color: transparent;
            }}
            QPushButton:flat:hover {{
                background-color: #e9ecef;
            }}

            /* Specific Button Styles */
            QPushButton#PrimaryButton {{
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 15px;
            }}
            QPushButton#PrimaryButton:hover {{
                background-color: #0056b3;
            }}
            QPushButton#OutlineButton {{
                border: 1px solid #ced4da;
                background-color: transparent;
            }}
             QPushButton#OutlineButton:hover {{
                 background-color: #f1f3f5;
             }}
            QPushButton#ToolButton {{
                 background-color: #e9ecef; /* Light gray background for tools */
                 border: none;
            }}
            QPushButton#ToolButton:hover {{
                 background-color: #dee2e6;
            }}
            QPushButton#IconButton {{ /* Buttons that are mainly icons */
                border: none;
                background-color: transparent;
                padding: 2px;
                min-width: 24px; /* Ensure space for icon */
                max-width: 24px;
                min-height: 24px;
                max-height: 24px;
                color: #6c757d; /* Default icon color */
            }}
            QPushButton#IconButton:hover {{
                background-color: #e9ecef;
            }}


            /* Input Fields */
            QLineEdit {{
                border: 1px solid #ced4da;
                padding: 5px 8px;
                border-radius: 4px;
                background-color: white;
            }}
            QLineEdit#ReadOnlyInput {{
                background-color: #e9ecef; /* Gray out read-only fields */
                border: 1px solid #ced4da;
            }}

            /* Section Frames */
            QFrame#InfoFrame {{
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 15px;
            }}

             /* Source Cards in Server View */
            QWidget#SourceCard {{
                background-color: #f1f3f5; /* Light gray background */
                border-radius: 6px;
                border: 1px solid #e9ecef; /* Subtle border */
            }}

             /* Source Config Cards in Server Sources View */
            QWidget#ConfigCard {{
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                min-height: 70px; /* Ensure decent height */
            }}
            QWidget#ConfigCard QPushButton#IconButton {{ /* Specific icon button style for these cards */
                 color: #6c757d;
             }}
            QWidget#ConfigCard QPushButton#IconButton:hover {{
                 color: #212529; /* Darken icon on hover */
                 background-color: #f1f3f5;
            }}


            /* Labels */
            QLabel {{
                background-color: transparent; /* Ensure labels don't obscure background */
            }}

            /* Scroll Area */
            QScrollArea {{
                border: none; /* Remove border from scroll area itself */
            }}
            QScrollArea > QWidget > QWidget {{ /* Target the scroll content widget */
                 background-color: transparent; /* Make background of scroll content transparent */
            }}
        """
        self.setStyleSheet(style)


# --- Run the Application ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # You might need to adjust font sizes globally depending on OS/scaling
    # font = QFont()
    # font.setPointSize(10) # Example: Set default font size
    # app.setFont(font)
    window = MCPManagerApp()
    window.show()
    sys.exit(app.exec())
