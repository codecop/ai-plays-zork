@if exist %~n0%~x0 @cd ..
@setlocal
@rem set PYTHONPATH=src
@mypy.exe --config-file bin\mypy.ini src %*
@mypy.exe --config-file bin\mypy.ini test %*
@endlocal
