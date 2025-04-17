"""Utility helpers for reading different application configuration files and
collecting all MCP servers referenced inside them.
"""

from __future__ import annotations

import json
import os
from typing import Dict, List

from models import SERVER_SOURCE, SERVER_TYPE, Server


def get_mcp_servers_from_claude_desktop(config_path: str) -> List[Server]:
    """Return a list of mcp servers from the *Claude Desktop* config file."""

    if not os.path.exists(config_path):
        return []

    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        print(f"Warning: Failed to parse Claude Desktop config file: {exc}")
        return []

    if not isinstance(data.get("mcpServers"), dict):
        print(
            "Warning: Unexpected structure in Claude Desktop config file. Falling back to regex scan."
        )
        return []

    mcpServers = data["mcpServers"]

    servers: list[Server] = []

    for name, srv in mcpServers.items():
        srv_id = name.replace(" ", "_")
        new_srv: Server = Server(
            server_type=SERVER_TYPE.LOCAL,
            server_source=SERVER_SOURCE.CLAUDE_DESKTOP,
            url="",
            id=srv_id,
            name=name,
            cmd=srv.get("command"),
            cmd_args=srv.get("args"),
        )
        servers.append(new_srv)

    return servers


def get_mcp_servers_from_cursor(mcp_json_path: str) -> List[Server]:
    """Return a *list of Server objects* defined in Cursor's
    ``~/.cursor/mcp.json`` configuration.
    """

    if not os.path.exists(mcp_json_path):
        return []

    try:
        with open(mcp_json_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        print(f"Warning: Failed to parse Cursor config file: {exc}")
        return []

    # ---------------------------------------------------------------------
    # Normal decoding path – look for "mcpServers" first.
    # ---------------------------------------------------------------------

    servers: list[Server] = []

    def _create_server(name: str, spec: dict):  # local helper
        """Convert a single mcpServers entry into a Server object."""

        srv_id = name.replace(" ", "_")

        if isinstance(spec, dict) and isinstance(spec.get("url"), str):
            # Remote endpoint
            return Server(
                id=srv_id,
                name=name,
                url=spec["url"],
                server_type=SERVER_TYPE.REMOTE,
                server_source=SERVER_SOURCE.CURSOR,
            )

        # Fallback – treat as *local* server started via command
        return Server(
            id=srv_id,
            name=name,
            url="",  # local
            server_type=SERVER_TYPE.LOCAL,
            server_source=SERVER_SOURCE.CURSOR,
            cmd=spec.get("command") if isinstance(spec, dict) else None,
            cmd_args=spec.get("args") if isinstance(spec, dict) else None,
        )

    if isinstance(data, dict) and isinstance(data.get("mcpServers"), dict):
        for name, entry in data["mcpServers"].items():
            server_obj = _create_server(name, entry)
            servers.append(server_obj)

    # ------------------------------------------------------------------
    # Legacy / alternate layout – top‑level "servers" list (older docs)
    # ------------------------------------------------------------------
    if not servers and isinstance(data, dict) and isinstance(data.get("servers"), list):
        for entry in data["servers"]:
            if not isinstance(entry, dict):
                continue

            url = entry.get("url")
            if not url:
                continue

            name = entry.get("name", url)
            srv_id = name.replace(" ", "_")
            servers.append(
                Server(
                    id=srv_id,
                    name=name,
                    url=url,
                    server_type=SERVER_TYPE.REMOTE,
                    server_source=SERVER_SOURCE.CURSOR,
                )
            )

    return servers


def get_mcp_servers_from_vscode(settings_path: str) -> List[Dict[str, str]]:
    """Parse *VS Code*'s *settings.json* for MCP Servers."""

    if not os.path.exists(settings_path):
        return []

    return []


def get_mcp_servers_from_windsurf(mcp_json_path: str) -> List[Server]:
    """Return a *list of Server objects* defined by **Windsurf / Codeium**.

    Codeium stores the configuration for *WindSurf* - its background MCP
    management process - in a JSON file usually located at::

        ~/.codeium/windsurf/mcp_config.json

    The exact structure of this JSON file is **not formally documented** and
    tends to evolve.  The two most common layouts that have been observed in
    the wild are listed below so the parser tries to handle them gracefully:

    1.  A top‑level ``"mcpServers"`` object (dictionary - similar to Claude
        Desktop / Cursor) where each key is a *display name* and every value
        is either …

        • a mapping containing at least a ``"url"`` for *remote* servers or
        • a mapping with ``"command"``/``"args"`` that describes how to start
          a *local* server process.

    2.  A more minimal layout that contains a top-level ``"servers"`` *list* of
        objects.  Each item must at least specify ``"url"`` and may optionally
        define ``"name"``.

    Anything that cannot be parsed safely is ignored - the caller will merely
    receive the successfully decoded servers.  The function never raises on
    malformed entries (only prints a warning) to mirror the behavior of the
    other helpers in this module.
    """

    if not os.path.exists(mcp_json_path):
        return []

    try:
        with open(mcp_json_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:  # pragma: no cover – we are defensive here
        print(f"Warning: Failed to parse Windsurf config file: {exc}")
        return []

    servers: list[Server] = []

    # ------------------------------------------------------------------
    # Helper that converts one *spec* dictionary into a Server object
    # ------------------------------------------------------------------

    def _spec_to_server(name: str, spec: dict) -> Server | None:  # local helper
        """Best-effort conversion of a single server specification."""

        if not isinstance(name, str):
            return None

        srv_id = name.replace(" ", "_")

        # --- Remote server (has explicit URL) -------------------------
        if isinstance(spec, dict) and isinstance(spec.get("url"), str):
            return Server(
                id=srv_id,
                name=name,
                url=spec["url"],
                server_type=SERVER_TYPE.REMOTE,
                server_source=SERVER_SOURCE.WINDSURF,
            )

        # --- Local server (uses command + args) -----------------------
        if isinstance(spec, dict):
            cmd = spec.get("command") or spec.get("cmd")
            cmd_args = spec.get("args")
            return Server(
                id=srv_id,
                name=name,
                url="",  # local – no URL
                server_type=SERVER_TYPE.LOCAL,
                server_source=SERVER_SOURCE.WINDSURF,
                cmd=cmd,
                cmd_args=cmd_args,
            )

        return None  # Unexpected shape – ignore

    # ------------------------------------------------------------------
    # 1. *mcpServers* dictionary (preferred format)
    # ------------------------------------------------------------------

    if isinstance(data, dict) and isinstance(data.get("mcpServers"), dict):
        for disp_name, spec in data["mcpServers"].items():
            srv_obj = _spec_to_server(disp_name, spec)
            if srv_obj:
                servers.append(srv_obj)

    # ------------------------------------------------------------------
    # 2. Legacy / minimal format – top‑level *servers* list
    # ------------------------------------------------------------------

    if not servers and isinstance(data, dict) and isinstance(data.get("servers"), list):
        for spec in data["servers"]:
            if not isinstance(spec, dict):
                continue

            url = spec.get("url")
            if not url or not isinstance(url, str):
                # If there is no URL we cannot treat it as a remote server –
                # in that case fall back to the generic helper which may still
                # produce a valid *local* server.
                name_guess = spec.get("name") or spec.get("label") or "Unnamed"
                srv_obj = _spec_to_server(name_guess, spec)
                if srv_obj:
                    servers.append(srv_obj)
                continue

            # Build a deterministic name if none provided (use the URL).
            name = spec.get("name") or url
            srv_id = name.replace(" ", "_")
            servers.append(
                Server(
                    id=srv_id,
                    name=name,
                    url=url,
                    server_type=SERVER_TYPE.REMOTE,
                    server_source=SERVER_SOURCE.WINDSURF,
                )
            )

    return servers


def get_mcp_servers(mcp_server_sources_file: str) -> List[Server]:
    """Read *mcp_server_sources.json* and return **all** referenced servers.

    The function does **not** persist anything - it only inspects external
    configuration files and aggregates the information for the caller.
    """

    if not os.path.exists(mcp_server_sources_file):
        raise FileNotFoundError(mcp_server_sources_file)

    try:
        with open(mcp_server_sources_file, "r", encoding="utf-8") as fp:
            sources_payload = json.load(fp)
    except json.JSONDecodeError as exc:
        raise ValueError("Corrupted mcp_server_sources.json") from exc

    if not isinstance(sources_payload, dict) or not isinstance(
        sources_payload.get("sources"), list
    ):
        return []

    all_servers: List[Server] = []

    all_server_source = sources_payload["sources"]

    for server_source in all_server_source:
        source_id = server_source.get("id", None)
        if not source_id:
            print("Warning: Missing source ID.")
            continue

        if source_id == "claude-desktop":
            claude_desktop_path = server_source.get("path", None)
            if not claude_desktop_path:
                print("Warning: Missing path for claude-desktop source.")
            else:
                claude_mcp_servers = get_mcp_servers_from_claude_desktop(
                    claude_desktop_path
                )
                all_servers += claude_mcp_servers

        elif source_id == "cursor":
            cursor_path = server_source.get("path", None)
            if not cursor_path:
                print("Warning: Missing path for cursor source.")
            else:
                cursor_mcp_servers = get_mcp_servers_from_cursor(cursor_path)
                all_servers += cursor_mcp_servers

        elif source_id == "windsurf":
            windsurf_path = server_source.get("path", None)
            if not windsurf_path:
                print("Warning: Missing path for windsurf source.")
            else:
                windsurf_servers = get_mcp_servers_from_windsurf(windsurf_path)
                all_servers += windsurf_servers

    return all_servers
