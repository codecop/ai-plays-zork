@if exist %~n0%~x0 @cd ..
call frotz\installation\install_pyfrotz.bat
call pip install -r requirements.txt
call pip list
