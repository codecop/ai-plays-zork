import sys
from mcp.local_mcp import LocalMcp


class AddMcpServer(LocalMcp):

    def name(self) -> str:
        return "local-add-mcp-server"

    def handle_tools_list(self, request_id):
        self._debug(f"Handling tools/list request: {request_id}")
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

    def handle_tools_call(self, request_id, params: dict):
        self._debug(f"Handling tools/call request: {request_id}")
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if tool_name == "add":
            result = arguments["a"] * arguments["b"]
            return self._handle_text_result(request_id, str(result))

        return self._handle_error(request_id, -32601, f"Unknown tool: {tool_name}")


def main() -> None:
    debug_enabled = len(sys.argv) > 1 and sys.argv[1] == "--debug"
    server = AddMcpServer(debug_enabled)
    server.run()
    server.close()


if __name__ == "__main__":
    main()
