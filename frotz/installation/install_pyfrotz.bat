@if exist %~n0%~x0 @cd ..\..
@rem install Windows modified version of pyfrotz
call pip install Frotz\installation\pyFrotz-0.1.5
call pip list
