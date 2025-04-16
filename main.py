#!/usr/bin/env python3
"""
MCP Server Manager - Application Entry Point
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MCPServerManager


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = MCPServerManager()
    window.show()

    # Default to Dashboard view on startup
    window.show_dashboard()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
