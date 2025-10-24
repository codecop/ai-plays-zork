@if exist %~n0%~x0 @cd ..
@setlocal
@set PYTHONPATH=src
@pylint.exe src test %*
@endlocal
