from fastmcp import FastMCP


mcp = FastMCP(name="remote-add-mcp-server")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a * b


def main() -> None:
    # mcp.run()  # via STDIO transport
    mcp.run(transport="http", host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
