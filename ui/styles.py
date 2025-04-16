"""
Stylesheet definitions for the MCP Server Manager
"""


def apply_main_styles(window):
    """Apply the main application styles to the window"""
    window.setStyleSheet(
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
    """
    )


def apply_dashboard_styles(dashboard):
    """Apply styles specific to the dashboard view"""
    dashboard.setStyleSheet(
        """
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
        
        #source_card {
            background-color: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }
        
        #source_name {
            font-weight: bold;
            color: #24292e;
            font-size: 14px;
        }
        
        #source_status {
            color: #586069;
            font-size: 12px;
        }
        
        #dropdown_icon {
            color: #a0a0a0;
            font-size: 12px;
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


def apply_server_sources_styles(sources):
    """Apply styles specific to the server sources view"""
    sources.setStyleSheet(
        """
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
        
        #source_item {
            background-color: #f6f8fa;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
        }
        
        #source_item_name {
            font-weight: bold;
            color: #24292e;
            font-size: 14px;
        }
        
        #source_item_path {
            color: #586069;
            font-size: 12px;
            font-family: monospace;
        }
        
        #edit_button, #icon_button {
            padding: 6px 12px;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            background-color: #fafbfc;
            color: #24292e;
        }
        
        #edit_button:hover, #icon_button:hover {
            background-color: #f3f4f6;
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
        
        #orange_dot {
            color: #f9826c;
            font-size: 16px;
        }
    """
    )
