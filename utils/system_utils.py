import os

from models import Source


def get_mcp_servers_from_claude_desktop(config_path):
    """
    Get a list of MCP servers from the Claude desktop application.
    """

    if not os.path.exists(config_path):
        return []


def get_mcp_servers_from_vscode(settings_path):
    """
    Get a list of MCP servers from the VS Code application.
    """

    if not os.path.exists(settings_path):
        return []


def get_mcp_servers_from_cursor(mcp_json_path):
    """
    Get a list of MCP servers from the Cursor application.
    """

    if not os.path.exists(mcp_json_path):
        return []


def get_mcp_servers_from_windsurf(mcp_json_path):
    """
    Get a list of MCP servers from the Windsurf application.
    """

    if not os.path.exists(mcp_json_path):
        return []


def get_mcp_servers(mcp_server_sources_file):
    """
    Create a default MCP server sources file if it doesn't exist.
    This function is called when the script is run directly.
    """

    claude_mcp_servers = get_mcp_servers_from_claude_desktop()
    vs_code_mcp_servers = get_mcp_servers_from_vscode()
    cursor_mcp_servers = get_mcp_servers_from_cursor()
    windsurf_mcp_servers = get_mcp_servers_from_windsurf()

    # Combine all MCP servers into a single list
    mcp_servers = (
        claude_mcp_servers
        + vs_code_mcp_servers
        + cursor_mcp_servers
        + windsurf_mcp_servers
    )

    return mcp_servers
