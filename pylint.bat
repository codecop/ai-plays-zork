@setlocal
@set PYTHONPATH=src
@pylint.exe --rcfile .pylintrc src test %*
@endlocal
