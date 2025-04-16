"""
Custom widget for server items in the sidebar list
"""

from PySide6.QtWidgets import QHBoxLayout, QLabel, QListWidgetItem, QVBoxLayout, QWidget


class ServerItem:
    """Creates a custom server item in a QListWidget"""

    def __init__(self, list_widget, name, subtitle, icon_class):
        """
        Initialize a new server item

        Args:
            list_widget: The QListWidget to add this item to
            name: Server name
            subtitle: Subtitle text (source count or type)
            icon_class: CSS class for the icon color
        """
        # Create a list widget item
        self.list_item = QListWidgetItem(list_widget)
        self.list_item.setText(name)  # Store name for reference

        # Create a custom widget for the item
        self.widget = QWidget()
        self.layout = QHBoxLayout(self.widget)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # Add icon
        self.icon = QLabel("●")
        self.icon.setObjectName(icon_class)

        # Add name and subtitle in a vertical layout
        self.text_widget = QWidget()
        self.text_layout = QVBoxLayout(self.text_widget)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.text_layout.setSpacing(2)

        self.name_label = QLabel(name)
        self.name_label.setObjectName("server_item_name")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("server_item_subtitle")

        self.text_layout.addWidget(self.name_label)
        self.text_layout.addWidget(self.subtitle_label)

        # Add arrow indicator at the end
        self.arrow = QLabel(">")
        self.arrow.setObjectName("server_item_arrow")

        # Add items to the layout
        self.layout.addWidget(self.icon, 0)
        self.layout.addWidget(self.text_widget, 1)  # 1 is stretch factor
        self.layout.addWidget(self.arrow, 0)

        # Set the size hint and add the custom widget to the list item
        self.list_item.setSizeHint(self.widget.sizeHint())
        list_widget.setItemWidget(self.list_item, self.widget)
