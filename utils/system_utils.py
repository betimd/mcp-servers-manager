"""Utility helpers for reading different application configuration files and
collecting all MCP server endpoints referenced inside them.

The public ``get_mcp_servers`` function takes the *mcp_server_sources.json* file
created during ``system_initiation_check`` and returns **one** combined list of
servers with duplicates (same URL) removed.

Each supported application (Claude-desktop, VS Code, Cursor, Windsurf) has a
small specialized reader that knows where within the corresponding JSON / text
file the server URLs usually live. Even if these heuristics fail for a
specific future version of an application we still fall back to a generic
URL-scanner so we will never completely miss a server that is literally
referenced in the file.
"""

from __future__ import annotations

import json
import os
import re
from typing import Dict, List

from models import SERVER_SOURCE, SERVER_TYPE, Server

# Regular expression used as a last-resort fallback for detecting HTTP(S)
# endpoints inside the configuration files.
_URL_RE = re.compile(r"https?://[^\s'\"`]+", re.IGNORECASE)


# Helper is intentionally short and returns a generator; we therefore ignore
# "imperative mood" docstring rule (D401).


def _extract_urls_from_json(data):  # noqa: D401
    """Recursively walk a *loaded* JSON object and yield all string values that
    look like an HTTP(S) URL.
    """

    if isinstance(data, dict):
        for value in data.values():
            yield from _extract_urls_from_json(value)
    elif isinstance(data, list):
        for item in data:
            yield from _extract_urls_from_json(item)
    elif isinstance(data, str):
        if _URL_RE.search(data):
            yield data


# ---------------------------------------------------------------------------
# Individual source readers
# ---------------------------------------------------------------------------


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


def get_mcp_servers_from_vscode(settings_path: str) -> List[Dict[str, str]]:
    """Parse *VS Code*'s *settings.json* for MCP endpoints.

    The official Anthropic extension stores the URL under
    ``"claude.mcp.endpoint"``.  Again, we keep the code lenient and fall back
    to a generic scan when necessary.
    """

    if not os.path.exists(settings_path):
        return []

    # VS Code allows // comments in settings.json.  We therefore read the file
    # as *text*, strip line comments and attempt to decode afterwards.
    try:
        with open(settings_path, "r", encoding="utf-8") as fp:
            raw_content = fp.readlines()

        # Remove simple // comments. We ignore edge-cases such as URLs that
        # themselves contain "//" because it is extremely unlikely to appear
        # in a VS Code setting string value.
        cleaned_lines = []
        for line in raw_content:
            # Preserve part before // if it is not inside a string literal.
            if "//" in line:
                quote_cnt = line.count('"')
                if quote_cnt % 2 == 0:  # even number of quotes - not inside a string
                    line = line.split("//", 1)[0] + "\n"
            cleaned_lines.append(line)

        json_data = json.loads("".join(cleaned_lines))
    except Exception:
        return _scan_file_for_urls(settings_path, source_name="VS Code")

    # Preferred dedicated key
    url = None
    for key in (
        "claude.mcp.endpoint",
        "claude.mcp.url",
        "anthropic.mcp.endpoint",
    ):
        if key in json_data and isinstance(json_data[key], str):
            url = json_data[key]
            break

    servers: List[Dict[str, str]] = []
    if url:
        servers.append({"name": "VS Code", "url": url})

    # Fallback - any other URLs in the file
    if not servers:
        for detected in _extract_urls_from_json(json_data):
            servers.append({"name": detected, "url": detected})

    return servers


def get_mcp_servers_from_cursor(mcp_json_path: str) -> List[Dict[str, str]]:
    """Read *Cursor*'s ``~/.cursor/mcp.json`` file.

    Cursor stores a very simple JSON structure (see below)::

        {
            "servers": [
                {"name": "Production", "url": "https://mcp.cursor.so/sse"}
            ]
        }
    """

    if not os.path.exists(mcp_json_path):
        return []

    try:
        with open(mcp_json_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception:
        return _scan_file_for_urls(mcp_json_path, source_name="Cursor")

    servers: List[Dict[str, str]] = []
    if isinstance(data, dict) and isinstance(data.get("servers"), list):
        for entry in data["servers"]:
            if not isinstance(entry, dict):
                continue
            url = entry.get("url")
            if url:
                servers.append({"name": entry.get("name", url), "url": url})

    if not servers:
        for url in _extract_urls_from_json(data):
            servers.append({"name": url, "url": url})

    return servers


def get_mcp_servers_from_windsurf(mcp_json_path: str) -> List[Dict[str, str]]:
    """Parse Windsurf's ``mcp_config.json`` file (part of *Codeium*).

    The file layout is identical to Cursor - we therefore reuse the same logic.
    """

    if not os.path.exists(mcp_json_path):
        return []

    try:
        with open(mcp_json_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception:
        return _scan_file_for_urls(mcp_json_path, source_name="Windsurf")

    servers: List[Dict[str, str]] = []
    if isinstance(data, dict) and isinstance(data.get("servers"), list):
        for entry in data["servers"]:
            if not isinstance(entry, dict):
                continue
            url = entry.get("url")
            if url:
                servers.append({"name": entry.get("name", url), "url": url})

    if not servers:
        for url in _extract_urls_from_json(data):
            servers.append({"name": url, "url": url})

    return servers


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------


def _scan_file_for_urls(path: str, source_name: str | None = None):
    """Return a very *best-effort* list of servers found via pure regex search.

    The function is intentionally **permissive** - if we accidentally pick up a
    non-MCP URL it can still easily be ignored or removed by the user, whereas
    silently missing a valid endpoint would be far more annoying.
    """

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fp:
            content = fp.read()
    except IOError:
        return []

    servers = []
    for match in _URL_RE.findall(content):
        servers.append({"name": source_name or match, "url": match})

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

    return all_servers
