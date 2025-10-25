import sys
import json
from pathlib import Path
from typing import Any


DEBUG = True
if len(sys.argv) > 1:
    DEBUG = sys.argv[1] == "--debug"


def debug(message: str) -> None:
    if not DEBUG:
        return

    print(f"DEBUG: {message}", file=sys.stderr)
    sys.stderr.flush()

    log_file = Path(__file__).with_suffix(".log")
    with log_file.open("a") as fp:
        fp.write(f"DEBUG: {message}\n")


def read_message() -> dict[str, Any] | None:
    line = sys.stdin.readline()
    debug(f"Read line: {line}")
    if not line:
        return None
    return json.loads(line.strip())


def write_message(message: dict):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()
    debug(f"Wrote message: {message}")


def handle_initialize(request_id):
    debug(f"Handling initialize request: {request_id}")
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "local-add-mcp-server", "version": "1.0.0"},
        },
    }


def handle_tools_list(request_id):
    debug(f"Handling tools/list request: {request_id}")
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "tools": [
                {
                    "name": "add",
                    "description": "Add two numbers",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "a": {"type": "number"},
                            "b": {"type": "number"},
                        },
                        "required": ["a", "b"],
                    },
                }
            ]
        },
    }


def handle_tools_call(request_id, params: dict):
    debug(f"Handling tools/call request: {request_id}")
    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    if tool_name == "add":
        result = arguments["a"] * arguments["b"]
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"content": [{"type": "text", "text": str(result)}]},
        }

    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
    }


def main() -> None:
    while True:
        message = read_message()
        debug(f"Received message: {message}")
        if message is None:
            break

        method = message.get("method")
        request_id = message.get("id")
        params = message.get("params", {})

        if method == "initialize":
            response = handle_initialize(request_id)
        elif method == "tools/list":
            response = handle_tools_list(request_id)
        elif method == "tools/call":
            response = handle_tools_call(request_id, params)
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

        write_message(response)


if __name__ == "__main__":
    main()
