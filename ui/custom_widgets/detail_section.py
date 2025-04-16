"""
Detail section widget with label, value, and copy button
"""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DetailSection:
    """
    A reusable widget for a detail section with a label, value field, and copy button
    Used for sections like Server Link, Command, etc.
    """

    def __init__(
        self, parent, parent_layout, label_text, value_text, object_name, icon_text=None
    ):
        """
        Initialize a new detail section

        Args:
            parent: Parent widget
            parent_layout: Layout to add this section to
            label_text: Text for the section label
            value_text: Text value to display in the field
            object_name: Object name for CSS styling
            icon_text: Optional icon text to display before the label
        """
        # Create the section container
        self.section = QWidget(parent)
        self.section.setObjectName("section_container")
        self.section_layout = QVBoxLayout(self.section)

        # Create the header with icon and label
        self.header = QWidget()
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 10)

        # Add icon if provided
        if icon_text:
            self.icon = QLabel(icon_text)
            self.icon.setObjectName("section_icon")
            self.header_layout.addWidget(self.icon)

        # Add label
        self.label = QLabel(label_text)
        self.label.setObjectName("section_label")

        self.header_layout.addWidget(self.label)
        self.header_layout.addStretch()

        # Create value field with copy button
        self.value_widget = QWidget()
        self.value_layout = QHBoxLayout(self.value_widget)
        self.value_layout.setContentsMargins(0, 0, 0, 0)
        self.value_layout.setSpacing(10)

        # Add value field
        self.value = QLineEdit(value_text)
        self.value.setReadOnly(True)
        self.value.setObjectName("value_field")

        # Add copy button
        self.copy_button = QPushButton("📋")  # Copy icon
        self.copy_button.setObjectName("copy_button")
        self.copy_button.setToolTip("Copy to clipboard")
        self.copy_button.clicked.connect(lambda: self.copy_to_clipboard(value_text))

        self.value_layout.addWidget(self.value)
        self.value_layout.addWidget(self.copy_button)

        # Add components to section layout
        self.section_layout.addWidget(self.header)
        self.section_layout.addWidget(self.value_widget)

        # Set object name for styling
        self.section.setObjectName(object_name)

        # Add to parent layout
        parent_layout.addWidget(self.section)

    def copy_to_clipboard(self, text):
        """Copy the text to clipboard"""
        # In a real app, this would use system clipboard
        print(f"Copied to clipboard: {text}")
