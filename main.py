import json
import os
import sys

from PySide6.QtWidgets import QApplication

from constants import MCP_SERVER_SOURCES_FILE_NAME, SYSTEM_DEFAULTS_FILE_NAME
from ui.main_window import MCPServerManager


def system_initiation_check():
    """
    Perform system checks before starting the application.
    This function can be expanded to include various checks as needed.
    """

    SERVER_SOURCES_FILE_PATH = f"./data/{MCP_SERVER_SOURCES_FILE_NAME}"

    if not os.path.exists("./system_defaults.json"):
        sys.exit(
            "System info definition file does NOT exists. Please check your installation."
        )
        return

    if os.path.exists(SERVER_SOURCES_FILE_PATH):
        print("Data source file already exists. System is already OK.")
        return

    running_platform = sys.platform
    print(f"Running on platform: {running_platform}")

    # read system defaults
    system_defaults = None
    with open(SYSTEM_DEFAULTS_FILE_NAME, "r") as file:
        system_defaults = json.load(file)
        print("System defaults loaded successfully.")

    if system_defaults is None:
        sys.exit("Failed to load system defaults.")
        return

    initial_server_sources = system_defaults.get("initial_sources", None)
    print(f"Initial server sources: {initial_server_sources}")

    # If there are no initial sources defined we cannot proceed further.
    if not initial_server_sources:
        print(
            "No initial sources defined in system defaults - skipping data file creation."
        )
        return

    # ---------------------------------------------------------------------
    # Build the user‑specific sources list based on the operating system
    # and expand any environment variables / home directory markers so the
    # resulting JSON contains absolute, user‑friendly paths.
    # ---------------------------------------------------------------------

    def _resolve_path(raw_path: str) -> str:  # local helper
        """Expand ~ and %VAR% / $VAR placeholders in a path string."""
        if not raw_path:
            return ""
        # First expand environment variables (Windows style %VAR% and Unix $VAR)
        expanded = os.path.expandvars(raw_path)
        # Then expand home directory ~
        expanded = os.path.expanduser(expanded)

        return expanded

    platform_key = None
    if (
        running_platform.startswith("darwin")
        or running_platform == "mac"
        or running_platform == "darwin"
    ):
        platform_key = "mac_json_path"
    elif running_platform.startswith("win"):
        platform_key = "win_json_path"
    else:
        # For linux or unknown – try a dedicated linux key, otherwise default to mac path
        platform_key = (
            "linux_json_path"
            if any("linux_json_path" in s for s in initial_server_sources)
            else "mac_json_path"
        )

    prepared_sources = []

    for src in initial_server_sources:
        raw_path = (
            src.get(platform_key)
            or src.get("mac_json_path")
            or src.get("win_json_path")
        )

        prepared_sources.append(
            {
                "id": src.get("id"),
                "name": src.get("name"),
                # We keep icon reference so UI can show it later if desired
                "icon": src.get("icon"),
                "path": _resolve_path(raw_path),
            }
        )

    # ------------------------------------------------------------------
    # Persist to ./data/mcp_server_source.json so the rest of the app can
    # load / append user‑added sources later on.
    # ------------------------------------------------------------------

    os.makedirs("./data", exist_ok=True)

    data_payload = {"sources": prepared_sources}

    try:
        with open(SERVER_SOURCES_FILE_PATH, "w", encoding="utf-8") as outfile:
            json.dump(data_payload, outfile, indent=2)
        print("Initial data source file created at ./data/mcp_server_source.json")
    except IOError as exc:
        sys.exit(f"Failed to create data source file: {exc}")


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
