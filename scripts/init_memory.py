#!/usr/bin/env python3

from __future__ import annotations

from memory_files import ensure_memory_files, GLOBAL, STABLE, PROJECT, VOLATILE


def main() -> None:
    ensure_memory_files()
    print("initialized memory files:")
    for path in [GLOBAL, STABLE, PROJECT, VOLATILE]:
        print(path)


if __name__ == "__main__":
    main()
