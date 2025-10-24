@if exist %~n0%~x0 @cd ..
pytest --cov --cov-report=term-missing %*
