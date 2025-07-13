from pathlib import Path
import re

"""Utilities for reading, saving text files and creating 'run' folders."""

encoding = "utf-8"


def readFile(path: str) -> str:
    with open(path, "r", encoding=encoding) as file:
        return file.read()


def writeFile(path: str, content: str) -> None:
    with open(path, "w", encoding=encoding) as file:
        file.write(content)


def getNextFolderName(basePath: Path, pattern: str) -> Path:
    patternRegex = re.compile(re.escape(pattern) + r"-(\d{3})")

    maxNum = 0

    path = Path(basePath)
    for item in path.iterdir():
        if item.is_dir():
            match = patternRegex.fullmatch(item.name)
            if match:
                num = int(match.group(1))
                if num > maxNum:
                    maxNum = num

    nextNum = maxNum + 1
    nextName = f"{pattern}-{nextNum:03d}"

    runFolder = path / nextName
    runFolder.mkdir(exist_ok=True)

    return runFolder


def readGamePlayNotes() -> str:
    return readFile("data/Zork Gameplay Notes.txt")
