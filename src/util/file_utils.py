"""Utilities for reading, saving text files and creating 'run' folders."""

import re
from pathlib import Path


ENCODING = "utf-8"


def read_file(path) -> str:
    with open(path, "r", encoding=ENCODING) as file:
        return file.read()


def write_file(path, content: str) -> None:
    with open(path, "w", encoding=ENCODING) as file:
        file.write(content)


def next_folder_name(base_path: Path, pattern: str) -> Path:
    pattern_regex = re.compile(re.escape(pattern) + r"-(\d{3})")

    max_num = 0

    path = Path(base_path)
    path.mkdir(parents=True, exist_ok=True)

    for item in path.iterdir():
        max_num = _next_num(pattern_regex, item, max_num)

    next_num = max_num + 1
    next_name = f"{pattern}-{next_num:03d}"

    run_folder = path / next_name
    run_folder.mkdir(exist_ok=True)

    return run_folder


def _next_num(pattern_regex: re.Pattern, item: Path, current_num: int) -> int:
    if item.is_dir():
        match = pattern_regex.fullmatch(item.name)
        if match:
            num = int(match.group(1))
            return max(current_num, num)

    return current_num
