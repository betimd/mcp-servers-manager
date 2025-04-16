"""
Main Window class for the MCP Server Manager application
"""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.dashboard_view import DashboardView
from ui.server_sources_view import ServerSourcesView
from ui.styles import apply_main_styles


class MCPServerManager(QMainWindow):
    """Main window for the MCP Server Manager application"""

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

        # Create content areas
        self.create_header()
        self.create_content_area()
        self.create_footer()

        # Apply styles
        apply_main_styles(self)

    def create_header(self):
        """Create the application header with navigation"""
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
        self.header_separator.setFrameShape(QFrame.HLine)
        self.header_separator.setFrameShadow(QFrame.Sunken)
        self.header_separator.setObjectName("separator")
        self.main_layout.addWidget(self.header_separator)

    def create_content_area(self):
        """Create the main content area with stacked views"""
        # Create stacked widget to switch between views
        self.content_stack = QStackedWidget()

        # Create and add dashboard view
        self.dashboard_view = DashboardView()

        # Create and add server sources view
        self.server_sources_view = ServerSourcesView()

        # Add views to stack
        self.content_stack.addWidget(self.dashboard_view)
        self.content_stack.addWidget(self.server_sources_view)

        # Add stack to main layout
        self.main_layout.addWidget(self.content_stack, 1)  # 1 is stretch factor

    def create_footer(self):
        """Create the application footer with links"""
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
        self.footer_separator.setFrameShape(QFrame.HLine)
        self.footer_separator.setFrameShadow(QFrame.Sunken)
        self.footer_separator.setObjectName("separator")

        # Add footer and separator to main layout
        self.main_layout.addWidget(self.footer_separator)
        self.main_layout.addWidget(self.footer)

    def show_dashboard(self):
        """Switch to the dashboard view"""
        self.content_stack.setCurrentIndex(0)
        self.dashboard_button.setProperty("active", True)
        self.server_sources_button.setProperty("active", False)
        self.dashboard_button.setStyleSheet("")  # Force style refresh
        self.server_sources_button.setStyleSheet("")  # Force style refresh
        self.style().polish(self.dashboard_button)
        self.style().polish(self.server_sources_button)

    def show_server_sources(self):
        """Switch to the server sources view"""
        self.content_stack.setCurrentIndex(1)
        self.dashboard_button.setProperty("active", False)
        self.server_sources_button.setProperty("active", True)
        self.dashboard_button.setStyleSheet("")  # Force style refresh
        self.server_sources_button.setStyleSheet("")  # Force style refresh
        self.style().polish(self.dashboard_button)
        self.style().polish(self.server_sources_button)
