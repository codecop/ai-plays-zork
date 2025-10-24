@if exist %~n0%~x0 @cd ..
@setlocal
@set PYTHONPATH=src
@pylint.exe --rcfile bin\.pylintrc src test %*
@endlocal
