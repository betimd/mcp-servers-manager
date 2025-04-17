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


def get_mcp_servers_from_claude_desktop(config_path: str) -> List[Dict[str, str]]:
    """Return a list of ``{"name": .., "url": ..}`` dictionaries extracted from
    Anthropic's *Claude Desktop* configuration file.

    Claude currently stores a "servers" list in a JSON file located in the
    user's *Application Support* directory.  The structure we have seen so far
    is::

        {
            "mcp": {
                "servers": [
                    {"name": "Neon", "url": "https://mcp.neon.tech/sse"},
                    ...
                ]
            }
        }

    We intentionally keep the parser very defensive because the exact keys may
    change in future versions.  If we do not find a dedicated list we scan the
    whole file for URLs as a fallback.
    """

    if not os.path.exists(config_path):
        return []

    try:
        with open(config_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        # Failed to parse JSON - fallback to regex scan
        print(f"Warning: Failed to parse Claude Desktop config file: {exc}")
        return []

    if not isinstance(data.get("mcpServers"), dict):
        print(
            "Warning: Unexpected structure in Claude Desktop config file. Falling back to regex scan."
        )
        return []

    servers = data["mcpServers"]

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


def _deduplicate(servers: List[Dict[str, str]]):
    """Remove duplicate URLs while keeping order (first appearance wins)."""

    seen = set()
    unique: List[Dict[str, str]] = []
    for srv in servers:
        url = srv.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(srv)
    return unique


def get_mcp_servers(mcp_server_sources_file: str) -> List[Dict[str, str]]:  # noqa: D401
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

    all_servers: List[Dict[str, str]] = []

    # Map from source.id to specialised reader
    reader_map = {
        "claude-desktop": get_mcp_servers_from_claude_desktop,
        "vscode": get_mcp_servers_from_vscode,
        "cursor": get_mcp_servers_from_cursor,
        "windsurf": get_mcp_servers_from_windsurf,
    }

    for src in sources_payload["sources"]:
        if not isinstance(src, dict):
            continue

        src_id = src.get("id")
        src_path = src.get("path")
        if not src_id or not src_path:
            continue

        reader = reader_map.get(src_id)
        if reader is None:
            # Unknown source - generic scan
            all_servers.extend(
                _scan_file_for_urls(src_path, source_name=src.get("name"))
            )
        else:
            all_servers.extend(reader(src_path))

    return _deduplicate(all_servers)
