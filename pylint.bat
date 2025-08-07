@setlocal
@set PYTHONPATH=src
@pylint.exe src test %*
@endlocal
