import json
import os
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MCPServerManager


def system_initiation_check():
    """
    Perform system checks before starting the application.
    This function can be expanded to include various checks as needed.
    """

    if not os.path.exists("./system_defaults.json"):
        sys.exit(
            "System info definition file does NOT exists. Please check your installation."
        )
        return

    if os.path.exists("./data/mcp_server_source.json"):
        print("Data source file already exists. System is already OK.")
        return

    running_platform = sys.platform
    print(f"Running on platform: {running_platform}")

    # read system defaults
    system_defaults = None
    with open("./system_defaults.json", "r") as file:
        system_defaults = json.load(file)
        print("System defaults loaded successfully.")

    if system_defaults is None:
        sys.exit("Failed to load system defaults.")
        return

    initial_server_sources = system_defaults.get("initial_sources", None)
    print(f"Initial server sources: {initial_server_sources}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    window = MCPServerManager()
    window.show()

    # Default to Dashboard view on startup
    window.show_dashboard()

    sys.exit(app.exec())


if __name__ == "__main__":
    system_initiation_check()
    main()
