"""
Source item widget for the server sources view
"""

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SourceItem(QFrame):
    """
    A list item widget that displays source information in the server sources view
    """

    def __init__(self, icon_text, name, path, icon_class, on_edit=None, on_delete=None):
        """
        Initialize a new source item

        Args:
            icon_text: Text for the icon (e.g., "●", "✓")
            name: Name of the source
            path: File path of the source configuration
            icon_class: CSS class for the icon color
            on_edit: Callback function for edit button click
            on_delete: Callback function for delete button click
        """
        super().__init__()

        # Set frame properties
        self.setObjectName("source_item")
        self.setFrameShape(QFrame.StyledPanel)

        # Create layout
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)

        # Add icon
        self.icon = QLabel(icon_text)
        self.icon.setObjectName(icon_class)

        # Add info container with name and path
        self.info = QWidget()
        self.info_layout = QVBoxLayout(self.info)
        self.info_layout.setContentsMargins(0, 0, 0, 0)
        self.info_layout.setSpacing(5)

        self.name_label = QLabel(name)
        self.name_label.setObjectName("source_item_name")

        self.path_label = QLabel(path)
        self.path_label.setObjectName("source_item_path")

        self.info_layout.addWidget(self.name_label)
        self.info_layout.addWidget(self.path_label)

        # Add action buttons container
        self.actions = QWidget()
        self.actions_layout = QHBoxLayout(self.actions)
        self.actions_layout.setContentsMargins(0, 0, 0, 0)
        self.actions_layout.setSpacing(10)

        # Add edit button
        self.edit_button = QPushButton("✎")
        self.edit_button.setObjectName("icon_button")
        self.edit_button.setToolTip("Edit source")
        if on_edit:
            self.edit_button.clicked.connect(on_edit)
        else:
            self.edit_button.clicked.connect(lambda: print(f"Edit {name} clicked"))

        # Add delete button
        self.delete_button = QPushButton("🗑")
        self.delete_button.setObjectName("icon_button")
        self.delete_button.setToolTip("Delete source")
        if on_delete:
            self.delete_button.clicked.connect(on_delete)
        else:
            self.delete_button.clicked.connect(lambda: print(f"Delete {name} clicked"))

        # Add buttons to actions layout
        self.actions_layout.addWidget(self.edit_button)
        self.actions_layout.addWidget(self.delete_button)

        # Add widgets to layout
        self.layout.addWidget(self.icon)
        self.layout.addWidget(self.info, 1)  # 1 is stretch factor
        self.layout.addWidget(self.actions)
