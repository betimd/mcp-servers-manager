"""
Source card widget for the dashboard sources section
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class SourceCard(QFrame):
    """
    A card widget that displays source information in the dashboard
    """

    def __init__(self, icon_text, name, status, icon_class):
        """
        Initialize a new source card

        Args:
            icon_text: Text for the icon (e.g., "●", "✓")
            name: Name of the source
            status: Status text (e.g., "Added", "Not Added")
            icon_class: CSS class for the icon color
        """
        super().__init__()

        # Set frame properties
        self.setObjectName("source_card")
        self.setFrameShape(QFrame.StyledPanel)

        # Create layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)

        # Add icon
        self.icon = QLabel(icon_text)
        self.icon.setObjectName(icon_class)

        # Add info container with name and status
        self.info = QWidget()
        self.info_layout = QVBoxLayout(self.info)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.info_layout.setSpacing(5)

        self.name_label = QLabel(name)
        self.name_label.setObjectName("source_name")

        self.status_label = QLabel(status)
        self.status_label.setObjectName("source_status")

        self.info_layout.addWidget(self.name_label)
        self.info_layout.addWidget(self.status_label)

        # Add dropdown/status indicator
        self.dropdown = QLabel("▼")
        self.dropdown.setObjectName("dropdown_icon")
        self.dropdown.setCursor(QCursor(Qt.PointingHandCursor))

        # Add widgets to layout
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.info, 1)  # 1 is stretch factor
        self.layout.addWidget(self.dropdown)
