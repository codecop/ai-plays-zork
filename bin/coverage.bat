@if exist %~n0%~x0 @cd ..
call pytest --cov --cov-report=term-missing %*
