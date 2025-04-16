import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QIcon
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
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class MCPServerManager(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("MCP Server Manager")
        self.setMinimumSize(1200, 700)

        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Add header, content area, and footer
        self.create_header()
        self.create_content_area()
        self.create_footer()

        # Apply styles
        self.apply_styles()

    def create_header(self):
        # Create header widget and layout
        self.header = QWidget()
        self.header.setFixedHeight(60)
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(20, 0, 20, 0)

        # Add logo and title
        self.logo_layout = QHBoxLayout()
        self.logo_layout.setSpacing(10)

        self.app_icon = QLabel("☰")  # Placeholder for app icon
        self.app_icon.setObjectName("app_icon")

        self.logo_label = QLabel("MCP Server Manager")
        self.logo_label.setObjectName("app_title")

        self.logo_layout.addWidget(self.app_icon)
        self.logo_layout.addWidget(self.logo_label)

        # Add navigation links
        self.nav_widget = QWidget()
        self.nav_layout = QHBoxLayout(self.nav_widget)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(30)

        self.dashboard_button = QPushButton("Dashboard")
        self.dashboard_button.setFlat(True)
        self.dashboard_button.setObjectName("nav_button")
        self.dashboard_button.clicked.connect(self.show_dashboard)

        self.server_sources_button = QPushButton("Server Sources")
        self.server_sources_button.setFlat(True)
        self.server_sources_button.setObjectName("nav_button")
        self.server_sources_button.clicked.connect(self.show_server_sources)

        self.github_button = QPushButton("GitHub ↗")
        self.github_button.setFlat(True)
        self.github_button.setObjectName("nav_button")
        self.github_button.clicked.connect(lambda: print("GitHub button clicked"))

        self.nav_layout.addWidget(self.dashboard_button)
        self.nav_layout.addWidget(self.server_sources_button)
        self.nav_layout.addWidget(self.github_button)

        # Add to header layout
        self.header_layout.addLayout(self.logo_layout)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.nav_widget)

        # Add header to main layout
        self.header.setObjectName("header")
        self.main_layout.addWidget(self.header)

        # Add separator line
        self.header_separator = QFrame()
        self.header_separator.setFrameShape(QFrame.Shape.HLine)
        self.header_separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.header_separator.setObjectName("separator")
        self.main_layout.addWidget(self.header_separator)

    def create_content_area(self):
        # Create stacked widget to switch between views
        self.content_stack = QStackedWidget()

        # Create dashboard view
        self.dashboard_view = QWidget()
        self.dashboard_layout = QHBoxLayout(self.dashboard_view)
        self.dashboard_layout.setContentsMargins(0, 0, 0, 0)
        self.dashboard_layout.setSpacing(0)

        # Create sidebar
        self.create_sidebar()

        # Create main content area
        self.server_content = QWidget()
        self.server_content_layout = QVBoxLayout(self.server_content)
        self.server_content_layout.setContentsMargins(25, 25, 25, 25)
        self.server_content_layout.setSpacing(20)

        # Add server details to content area
        self.create_server_details()

        # Add sidebar and content to dashboard layout
        self.dashboard_layout.addWidget(self.sidebar)
        self.dashboard_layout.addWidget(self.server_content)

        # Set stretch factors (1:3 ratio)
        self.dashboard_layout.setStretch(0, 1)  # Sidebar
        self.dashboard_layout.setStretch(1, 3)  # Content

        # Create server sources view
        self.server_sources_view = QWidget()
        self.server_sources_layout = QVBoxLayout(self.server_sources_view)
        self.server_sources_layout.setContentsMargins(25, 25, 25, 25)
        self.server_sources_layout.setSpacing(20)

        # Add server sources content
        self.create_server_sources_content()

        # Add views to stack
        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.addWidget(self.server_sources_view)

        # Add stack to main layout
        self.main_layout.addWidget(self.content_stack, 1)  # 1 is stretch factor

    def create_sidebar(self):
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
        self.sidebar_layout.addWidget(self.search_box)

        # Add servers label
        self.servers_label = QLabel("SERVERS")
        self.servers_label.setObjectName("sidebar_section_label")
        self.sidebar_layout.addWidget(self.servers_label)

        # Add server list
        self.server_list = QListWidget()
        self.server_list.setObjectName("server_list")
        self.server_list.setFrameShape(QFrame.Shape.NoFrame)
        self.server_list.setVerticalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.server_list.itemClicked.connect(self.on_server_selected)
        self.sidebar_layout.addWidget(self.server_list)

        # Create custom server list items
        self.add_server_item("Neon MCP Server", "2 sources", "green_dot")
        self.add_server_item("Local Development MCP", "VS Code", "blue_dot")
        self.add_server_item("OpenAI Tools Server", "3 sources", "purple_dot")
        self.add_server_item("Custom MCP Server", "Claude Desktop", "red_dot")

        # Connect item selection to update server details
        self.server_list.setCurrentRow(0)  # Select Neon by default

    def on_server_selected(self, item):
        print(f"Selected server: {item.text()}")
        # In a real application, this would update the server details

    def add_server_item(self, name, subtitle, icon_class):
        # Create a custom widget for the server item
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(10, 10, 10, 10)

        # Add icon
        icon = QLabel("●")
        icon.setObjectName(icon_class)

        # Add name and subtitle in a vertical layout
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)

        name_label = QLabel(name)
        name_label.setObjectName("server_item_name")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("server_item_subtitle")

        text_layout.addWidget(name_label)
        text_layout.addWidget(subtitle_label)

        # Add items to the layout
        item_layout.addWidget(icon, 0)
        item_layout.addWidget(text_widget, 1)  # 1 is stretch factor

        # Add arrow indicator at the end
        arrow = QLabel(">")
        arrow.setObjectName("server_item_arrow")
        item_layout.addWidget(arrow, 0)

        # Create a list widget item and set its size
        list_item = QListWidgetItem(self.server_list)
        list_item.setSizeHint(item_widget.sizeHint())
        list_item.setText(name)  # Store name for reference

        # Set the custom widget
        self.server_list.setItemWidget(list_item, item_widget)

    def create_server_details(self):
        # Create server title section
        self.server_title_widget = QWidget()
        self.server_title_layout = QHBoxLayout(self.server_title_widget)
        self.server_title_layout.setContentsMargins(0, 0, 0, 5)

        self.server_icon = QLabel("●")
        self.server_icon.setObjectName("green_dot")

        self.server_name = QLabel("Neon MCP Server")
        self.server_name.setObjectName("server_name")

        self.edit_button = QPushButton("Edit")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setText("✎ Edit")
        self.edit_button.clicked.connect(lambda: print("Edit server clicked"))

        self.server_title_layout.addWidget(self.server_icon)
        self.server_title_layout.addWidget(self.server_name)
        self.server_title_layout.addStretch()
        self.server_title_layout.addWidget(self.edit_button)

        self.server_content_layout.addWidget(self.server_title_widget)

        # Create server link section
        self.create_detail_section(
            "Server Link:",
            "https://mcp.neon.tech/sse",
            "server_link_section",
            "🔗",  # Link icon
        )

        # Create command section
        self.create_detail_section(
            "Command:",
            "npx -y mcp-remote https://mcp.neon.tech/sse",
            "command_section",
            "⌘",  # Command icon
        )

        # Create tools section
        self.tools_widget = QWidget()
        self.tools_widget.setObjectName("section_container")
        self.tools_layout = QVBoxLayout(self.tools_widget)

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

        self.tools_buttons_widget = QWidget()
        self.tools_buttons_layout = QHBoxLayout(self.tools_buttons_widget)
        self.tools_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.tools_buttons_layout.setSpacing(10)

        # Add tool buttons
        self.list_projects_button = QPushButton("listProjects")
        self.list_projects_button.setObjectName("tool_button")
        self.list_projects_button.clicked.connect(lambda: print("listProjects clicked"))

        self.create_database_button = QPushButton("createDatabase")
        self.create_database_button.setObjectName("tool_button")
        self.create_database_button.clicked.connect(
            lambda: print("createDatabase clicked")
        )

        self.run_query_button = QPushButton("runQuery")
        self.run_query_button.setObjectName("tool_button")
        self.run_query_button.clicked.connect(lambda: print("runQuery clicked"))

        self.tools_buttons_layout.addWidget(self.list_projects_button)
        self.tools_buttons_layout.addWidget(self.create_database_button)
        self.tools_buttons_layout.addWidget(self.run_query_button)
        self.tools_buttons_layout.addStretch()

        self.tools_layout.addWidget(self.tools_header)
        self.tools_layout.addWidget(self.tools_buttons_widget)

        self.server_content_layout.addWidget(self.tools_widget)

        # Create sources section
        self.sources_widget = QWidget()
        self.sources_widget.setObjectName("section_container")
        self.sources_layout = QVBoxLayout(self.sources_widget)

        # Sources header
        self.sources_header = QWidget()
        self.sources_header_layout = QHBoxLayout(self.sources_header)
        self.sources_header_layout.setContentsMargins(0, 0, 0, 20)

        self.sources_icon = QLabel("📱")  # Sources icon
        self.sources_icon.setObjectName("section_icon")

        self.sources_label = QLabel("Sources:")
        self.sources_label.setObjectName("section_label")

        self.sources_actions = QWidget()
        self.sources_actions_layout = QHBoxLayout(self.sources_actions)
        self.sources_actions_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_actions_layout.setSpacing(10)

        self.remove_from_all_button = QPushButton("Remove from all")
        self.remove_from_all_button.setObjectName("action_button")
        self.remove_from_all_button.setIcon(QIcon.fromTheme("edit-delete"))
        self.remove_from_all_button.clicked.connect(
            lambda: print("Remove from all clicked")
        )

        self.sync_to_all_button = QPushButton("Sync to all")
        self.sync_to_all_button.setObjectName("action_button")
        self.sync_to_all_button.setIcon(QIcon.fromTheme("view-refresh"))
        self.sync_to_all_button.clicked.connect(lambda: print("Sync to all clicked"))

        self.sources_actions_layout.addWidget(self.remove_from_all_button)
        self.sources_actions_layout.addWidget(self.sync_to_all_button)

        self.sources_header_layout.addWidget(self.sources_icon)
        self.sources_header_layout.addWidget(self.sources_label)
        self.sources_header_layout.addStretch()
        self.sources_header_layout.addWidget(self.sources_actions)

        # Sources grid
        self.sources_grid = QWidget()
        self.sources_grid_layout = QGridLayout(self.sources_grid)
        self.sources_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_grid_layout.setSpacing(16)

        # Create source cards
        self.claude_card = self.create_source_card(
            "●", "Claude Desktop", "Added", "purple_dot"
        )

        self.vscode_card = self.create_source_card(
            "✓", "VS Code", "Not Added", "blue_dot"
        )

        self.cursor_card = self.create_source_card("►", "Cursor", "Added", "green_dot")

        self.windsurf_card = self.create_source_card(
            "♦", "Windsurf", "Not Added", "orange_dot"
        )

        # Add cards to grid
        self.sources_grid_layout.addWidget(self.claude_card, 0, 0)
        self.sources_grid_layout.addWidget(self.vscode_card, 0, 1)
        self.sources_grid_layout.addWidget(self.cursor_card, 1, 0)
        self.sources_grid_layout.addWidget(self.windsurf_card, 1, 1)

        # Add to sources layout
        self.sources_layout.addWidget(self.sources_header)
        self.sources_layout.addWidget(self.sources_grid)

        self.server_content_layout.addWidget(self.sources_widget)
        self.server_content_layout.addStretch()

    def create_detail_section(
        self, label_text, value_text, object_name, icon_text=None
    ):
        section = QWidget()
        section.setObjectName("section_container")
        section_layout = QVBoxLayout(section)

        # Header with icon and label
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 10)

        if icon_text:
            icon = QLabel(icon_text)
            icon.setObjectName("section_icon")
            header_layout.addWidget(icon)

        label = QLabel(label_text)
        label.setObjectName("section_label")

        header_layout.addWidget(label)
        header_layout.addStretch()

        # Value field with copy button
        value_widget = QWidget()
        value_layout = QHBoxLayout(value_widget)
        value_layout.setContentsMargins(0, 0, 0, 0)
        value_layout.setSpacing(10)

        value = QLineEdit(value_text)
        value.setReadOnly(True)
        value.setObjectName("value_field")

        copy_button = QPushButton("📋")  # Copy icon
        copy_button.setObjectName("copy_button")
        copy_button.setToolTip("Copy to clipboard")
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(value_text))

        value_layout.addWidget(value)
        value_layout.addWidget(copy_button)

        section_layout.addWidget(header)
        section_layout.addWidget(value_widget)

        section.setObjectName(object_name)
        self.server_content_layout.addWidget(section)

        return section

    def copy_to_clipboard(self, text):
        # In a real app, this would copy to clipboard
        print(f"Copied to clipboard: {text}")

    def create_source_card(self, icon_text, name, status, icon_class):
        card = QFrame()
        card.setObjectName("source_card")
        card.setFrameShape(QFrame.Shape.StyledPanel)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)

        icon = QLabel(icon_text)
        icon.setObjectName(icon_class)

        info = QWidget()
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)

        name_label = QLabel(name)
        name_label.setObjectName("source_name")

        status_label = QLabel(status)
        status_label.setObjectName("source_status")

        info_layout.addWidget(name_label)
        info_layout.addWidget(status_label)

        # Add dropdown/status indicator
        dropdown = QLabel("▼")
        dropdown.setObjectName("dropdown_icon")
        dropdown.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        card_layout.addWidget(icon)
        card_layout.addWidget(info, 1)  # 1 is stretch factor
        card_layout.addWidget(dropdown)

        return card

    def create_server_sources_content(self):
        # Title and subtitle
        self.sources_title = QLabel("Server Sources")
        self.sources_title.setObjectName("page_title")

        self.sources_subtitle = QLabel(
            "Manage MCP server sources from different applications"
        )
        self.sources_subtitle.setObjectName("page_subtitle")

        # Header widget containing title, subtitle, and add button
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
        self.add_source_button.clicked.connect(lambda: print("Add Source clicked"))

        # Add to header layout
        self.sources_header_layout.addWidget(self.sources_title_container)
        self.sources_header_layout.addStretch()
        self.sources_header_layout.addWidget(self.add_source_button)

        # Add header to sources layout
        self.server_sources_layout.addWidget(self.sources_header)

        # Create scrollable area for source list
        self.sources_scroll = QScrollArea()
        self.sources_scroll.setWidgetResizable(True)
        self.sources_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.sources_scroll_content = QWidget()
        self.sources_scroll_layout = QVBoxLayout(self.sources_scroll_content)
        self.sources_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.sources_scroll_layout.setSpacing(16)

        # Add source items
        self.sources_scroll_layout.addWidget(
            self.create_source_item(
                "●",
                "Claude Desktop",
                "/Users/user/.config/claude-desktop/mcp.json",
                "purple_dot",
            )
        )

        self.sources_scroll_layout.addWidget(
            self.create_source_item(
                "✓",
                "VS Code",
                "/Users/user/.vscode/extensions/anthropic.claude-1.0.0/mcp.json",
                "blue_dot",
            )
        )

        self.sources_scroll_layout.addWidget(
            self.create_source_item(
                "►",
                "Cursor",
                "/Applications/Cursor.app/Contents/Resources/mcp.json",
                "green_dot",
            )
        )

        self.sources_scroll_layout.addWidget(
            self.create_source_item(
                "♦", "Windsurf", "/Users/user/.windsurf/mcp.json", "orange_dot"
            )
        )

        # Add stretch to push items to the top
        self.sources_scroll_layout.addStretch()

        # Set scroll content and add to layout
        self.sources_scroll.setWidget(self.sources_scroll_content)
        self.server_sources_layout.addWidget(
            self.sources_scroll, 1
        )  # 1 is stretch factor

    def create_source_item(self, icon_text, name, path, icon_class):
        # Create container frame
        item = QFrame()
        item.setObjectName("source_item")
        item.setFrameShape(QFrame.Shape.StyledPanel)

        # Create layout
        item_layout = QHBoxLayout(item)
        item_layout.setContentsMargins(16, 16, 16, 16)

        # Icon
        icon = QLabel(icon_text)
        icon.setObjectName(icon_class)

        # Info container
        info = QWidget()
        info_layout = QVBoxLayout(info)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(5)

        # Name and path
        name_label = QLabel(name)
        name_label.setObjectName("source_item_name")

        path_label = QLabel(path)
        path_label.setObjectName("source_item_path")

        info_layout.addWidget(name_label)
        info_layout.addWidget(path_label)

        # Action buttons
        actions = QWidget()
        actions_layout = QHBoxLayout(actions)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(10)

        edit_button = QPushButton("✎")
        edit_button.setObjectName("icon_button")
        edit_button.setToolTip("Edit source")
        edit_button.clicked.connect(lambda: print(f"Edit {name} clicked"))

        delete_button = QPushButton("🗑")
        delete_button.setObjectName("icon_button")
        delete_button.setToolTip("Delete source")
        delete_button.clicked.connect(lambda: print(f"Delete {name} clicked"))

        actions_layout.addWidget(edit_button)
        actions_layout.addWidget(delete_button)

        # Add widgets to item layout
        item_layout.addWidget(icon)
        item_layout.addWidget(info, 1)  # 1 is stretch factor
        item_layout.addWidget(actions)

        return item

    def create_footer(self):
        # Create footer widget and layout
        self.footer = QWidget()
        self.footer.setFixedHeight(50)
        self.footer_layout = QHBoxLayout(self.footer)
        self.footer_layout.setContentsMargins(20, 0, 20, 0)

        # Add copyright info
        self.copyright = QLabel("© 2025 MCP Server Manager. All rights reserved.")
        self.copyright.setObjectName("footer_text")

        # Add footer links
        self.footer_links = QWidget()
        self.footer_links_layout = QHBoxLayout(self.footer_links)
        self.footer_links_layout.setContentsMargins(0, 0, 0, 0)
        self.footer_links_layout.setSpacing(30)

        self.docs_button = QPushButton("Documentation")
        self.docs_button.setFlat(True)
        self.docs_button.setObjectName("footer_link")
        self.docs_button.clicked.connect(lambda: print("Documentation clicked"))

        self.github_footer_button = QPushButton("GitHub")
        self.github_footer_button.setFlat(True)
        self.github_footer_button.setObjectName("footer_link")
        self.github_footer_button.clicked.connect(
            lambda: print("GitHub footer clicked")
        )

        self.support_button = QPushButton("Support ↗")
        self.support_button.setFlat(True)
        self.support_button.setObjectName("footer_link")
        self.support_button.clicked.connect(lambda: print("Support clicked"))

        self.footer_links_layout.addWidget(self.docs_button)
        self.footer_links_layout.addWidget(self.github_footer_button)
        self.footer_links_layout.addWidget(self.support_button)

        # Add to footer layout
        self.footer_layout.addWidget(self.copyright)
        self.footer_layout.addStretch()
        self.footer_layout.addWidget(self.footer_links)

        # Add separator line
        self.footer_separator = QFrame()
        self.footer_separator.setFrameShape(QFrame.Shape.HLine)
        self.footer_separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.footer_separator.setObjectName("separator")

        # Add footer and separator to main layout
        self.main_layout.addWidget(self.footer_separator)
        self.main_layout.addWidget(self.footer)

    def show_dashboard(self):
        self.content_stack.setCurrentIndex(0)
        self.dashboard_button.setProperty("active", True)
        self.server_sources_button.setProperty("active", False)
        self.dashboard_button.setStyleSheet("")  # Force style refresh
        self.server_sources_button.setStyleSheet("")  # Force style refresh
        self.apply_styles()

    def show_server_sources(self):
        self.content_stack.setCurrentIndex(1)
        self.dashboard_button.setProperty("active", False)
        self.server_sources_button.setProperty("active", True)
        self.dashboard_button.setStyleSheet("")  # Force style refresh
        self.server_sources_button.setStyleSheet("")  # Force style refresh
        self.apply_styles()

    def apply_styles(self):
        # General app styles
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #ffffff;
                font-family: Arial, sans-serif;
            }
            
            #header, #footer {
                background-color: #ffffff;
                border: none;
            }
            
            #separator {
                color: #e1e4e8;
                height: 1px;
            }
            
            #app_icon {
                font-size: 18px;
                color: #0366d6;
            }
            
            #app_title {
                font-size: 16px;
                font-weight: bold;
                color: #24292e;
            }
            
            #nav_button {
                border: none;
                padding: 8px 12px;
                color: #586069;
                font-size: 14px;
            }
            
            #nav_button:hover {
                color: #0366d6;
            }
            
            #nav_button[active="true"] {
                color: #0366d6;
                font-weight: bold;
            }
            
            #sidebar {
                background-color: #f6f8fa;
                border-right: 1px solid #e1e4e8;
            }
            
            #sidebar_section_label {
                color: #586069;
                font-size: 12px;
                font-weight: bold;
                padding-top: 10px;
                padding-bottom: 5px;
            }
            
            #search_box {
                padding: 8px;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                background-color: #fff;
            }
            
            #server_list {
                border: none;
                background-color: transparent;
            }
            
            #server_list::item {
                border-radius: 6px;
                padding: 5px;
            }
            
            #server_list::item:selected {
                background-color: #f1f8ff;
            }
            
            #server_item_name {
                font-weight: bold;
                color: #24292e;
                font-size: 14px;
            }
            
            #server_item_subtitle {
                color: #586069;
                font-size: 12px;
            }
            
            #server_item_arrow {
                color: #a0a0a0;
            }
            
            #server_name {
                font-size: 24px;
                font-weight: bold;
                color: #24292e;
            }
            
            #edit_button, #copy_button, #action_button, #icon_button {
                padding: 6px 12px;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                background-color: #fafbfc;
                color: #24292e;
            }
            
            #edit_button:hover, #copy_button:hover, #action_button:hover, #icon_button:hover {
                background-color: #f3f4f6;
            }
            
            #section_container {
                background-color: #ffffff;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                padding: 16px;
            }
            
            #section_label {
                font-weight: bold;
                color: #24292e;
                font-size: 16px;
            }
            
            #section_icon {
                color: #6a737d;
                font-size: 16px;
            }
            
            #value_field {
                padding: 8px;
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                color: #24292e;
            }
            
            #tool_button {
                padding: 6px 12px;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
                background-color: #fafbfc;
                color: #24292e;
            }
            
            #tool_button:hover {
                background-color: #f3f4f6;
            }
            
            #source_card, #source_item {
                background-color: #f6f8fa;
                border: 1px solid #e1e4e8;
                border-radius: 6px;
            }
            
            #source_name, #source_item_name {
                font-weight: bold;
                color: #24292e;
                font-size: 14px;
            }
            
            #source_status {
                color: #586069;
                font-size: 12px;
            }
            
            #source_item_path {
                color: #586069;
                font-size: 12px;
                font-family: monospace;
            }
            
            #dropdown_icon {
                color: #a0a0a0;
                font-size: 12px;
            }
            
            #footer_text, #footer_link {
                color: #586069;
                font-size: 12px;
            }
            
            #footer_link {
                border: none;
            }
            
            #footer_link:hover {
                color: #0366d6;
            }
            
            #page_title {
                font-size: 24px;
                font-weight: bold;
                color: #24292e;
            }
            
            #page_subtitle {
                color: #586069;
                font-size: 14px;
            }
            
            #add_button {
                padding: 6px 16px;
                border-radius: 6px;
                background-color: #2ea44f;
                color: white;
                font-weight: bold;
            }
            
            #add_button:hover {
                background-color: #22863a;
            }
            
            #green_dot {
                color: #2ea44f;
                font-size: 16px;
            }
            
            #blue_dot {
                color: #0366d6;
                font-size: 16px;
            }
            
            #purple_dot {
                color: #8250df;
                font-size: 16px;
            }
            
            #red_dot {
                color: #d73a49;
                font-size: 16px;
            }
            
            #orange_dot {
                color: #f9826c;
                font-size: 16px;
            }
        """
        )


def main():
    app = QApplication(sys.argv)
    window = MCPServerManager()
    window.show()

    # Default to Dashboard view
    window.show_dashboard()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
