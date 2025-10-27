@if exist %~n0%~x0 @cd ..
call gemini extensions list
call gemini extensions uninstall local-game-mcp-server

:install
call gemini extensions install E:\Develop\Python\Python-3\AiPlaysZork\src\frotz\Gemini_mcp_setup
call gemini extensions list
call gemini mcp list

:run
call gemini --debug
