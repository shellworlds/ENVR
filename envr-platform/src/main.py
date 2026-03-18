#!/usr/bin/env python3
"""ENVR env report: Python entry for client diagnostics."""
import json
import os
import platform
import sys


def main() -> None:
    data = {
        "python": sys.version,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cwd": os.getcwd(),
        "user": os.environ.get("USER", ""),
    }
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
