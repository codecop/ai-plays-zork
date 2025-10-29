@if exist %~n0%~x0 @cd ..
call PowerShell -Command "pip freeze | ForEach-Object { pip uninstall $_ -y }"
call pip list
