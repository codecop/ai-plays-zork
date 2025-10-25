import sys
import json


def read_message():
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line.strip())


def write_message(message):
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


def handle_tools_call(request_id, params):
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


def main():
    while True:
        message = read_message()
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
