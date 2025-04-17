from enum import Enum


class SERVER_TYPE(Enum):
    LOCAL = "local"
    REMOTE = "remote"


class SERVER_SOURCE(Enum):
    CLAUDE_DESKTOP = "claude_desktop"
    VC_CODE = "vscode"
    CURSOR = "cursor"
    WINDSURF = "windsurf"
