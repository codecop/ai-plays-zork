@echo setting up Frotz
@setlocal

@set TARGET=%HOMEDRIVE%%HOMEPATH%\.pyfrotz
@if exist "%TARGET%\dfrotz.exe" @goto done

mkdir "%TARGET%"
copy "dfrotz.exe" "%TARGET%"

:done
@endlocal
