import sys
import json
from typing import Any


def read_message() -> dict[str, Any] | None:
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line.strip())


def write_message(message: dict):
    sys.stdout.write(json.dumps(message) + "\n")
    sys.stdout.flush()


def handle_initialize(request_id):
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
        if message is None:
            break

        method = message.get("method")
        request_id = message.get("id")
        params = message.get("params", {})

        if request_id is str and method == "initialize":
            response = handle_initialize(request_id)
        elif request_id is str and method == "tools/list":
            response = handle_tools_list(request_id)
        elif request_id is str and method == "tools/call":
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
