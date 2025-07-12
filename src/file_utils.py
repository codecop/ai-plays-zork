from pathlib import Path
import re


def readFile(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def writeFile(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def getNextFolderName(basePath: str, pattern: str) -> str:
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
    return f"{pattern}-{nextNum:03d}"
