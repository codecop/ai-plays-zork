from frotz.local_game_mcp_server import GameMcpServer
import pytest


@pytest.fixture(name="new_server")
def fixture_new_server():
    server = GameMcpServer(debug=False)
    yield server
    server._game.close()


def test_Initialize(new_server):

    response = new_server._handle_initialize(request_id=1)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert response["result"]["protocolVersion"] == "2024-11-05"
    assert "tools" in response["result"]["capabilities"]
    assert response["result"]["serverInfo"]["name"] == "local-game-mcp-server"
    assert response["result"]["serverInfo"]["version"] == "1.0.0"


def test_ToolsList(new_server):

    response = new_server._handle_tools_list(request_id=2)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 2
    assert len(response["result"]["tools"]) == 4

    tool_names = [tool["name"] for tool in response["result"]["tools"]]
    assert "send_command" in tool_names
    assert "get_last_answer" in tool_names
    assert "get_game_status" in tool_names
    assert "get_gameplay_notes" in tool_names


def test_ToolsCall_SendCommand(new_server):

    params = {"name": "send_command", "arguments": {"command": "look"}}
    response = new_server._handle_tools_call(request_id=3, params=params)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 3
    assert "result" in response
    assert len(response["result"]["content"]) == 1
    assert response["result"]["content"][0]["type"] == "text"
    assert "West of House" in response["result"]["content"][0]["text"]


def test_ToolsCall_GameStatus(new_server):

    params = {"name": "get_game_status", "arguments": {}}
    response = new_server._handle_tools_call(request_id=5, params=params)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 5
    status_text = response["result"]["content"][0]["text"]
    assert "Room:" in status_text
    assert "Moves:" in status_text
    assert "Score:" in status_text


def test_ToolsCall_UnknownTool(new_server):

    params = {"name": "unknown_tool", "arguments": {}}
    response = new_server._handle_tools_call(request_id=7, params=params)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 7
    assert "error" in response
    assert response["error"]["code"] == -32601
    assert "Unknown tool" in response["error"]["message"]
