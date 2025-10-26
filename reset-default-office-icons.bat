@echo off
setlocal enableextensions
title Revert .docx/.xlsx/.pptx icons to their defaults (remove per-user overrides)

call :GetProgId ".docx" DOCX_PG "Word.Document.12"
call :GetProgId ".xlsx" XLSX_PG "Excel.Sheet.12"
call :GetProgId ".pptx" PPTX_PG "PowerPoint.Show.12"
call :GetProgId ".doc"  DOC_PG  "Word.Document.8"
call :GetProgId ".xls"  XLS_PG  "Excel.Sheet.8"
call :GetProgId ".ppt"  PPT_PG  "PowerPoint.Show.8"

rem Remove the DefaultIcon subkeys we created under HKCU\Software\Classes
reg delete "HKCU\Software\Classes\%DOCX_PG%\DefaultIcon" /f >nul 2>&1
reg delete "HKCU\Software\Classes\%XLSX_PG%\DefaultIcon" /f >nul 2>&1
reg delete "HKCU\Software\Classes\%PPTX_PG%\DefaultIcon" /f >nul 2>&1
reg delete "HKCU\Software\Classes\%DOC_PG%\DefaultIcon" /f >nul 2>&1
reg delete "HKCU\Software\Classes\%XLS_PG%\DefaultIcon" /f >nul 2>&1
reg delete "HKCU\Software\Classes\%PPT_PG%\DefaultIcon" /f >nul 2>&1

echo [OK] Removed per-user icon overrides. Refreshing icon cache...
call :RefreshIcons
echo Reverted. If icons don’t update, sign out/in.
goto :EOF


:GetProgId
set "EXT=%~1"
set "OUT=%~2"
set "FALLBACK=%~3"
set "PGID="

for /f "skip=2 tokens=1,2,*" %%A in ('reg query "HKCR\%EXT%" /ve 2^>nul') do set "PGID=%%C"
if not defined PGID (
  for /f "skip=2 tokens=1,2,*" %%A in ('reg query "HKCU\Software\Classes\%EXT%" /ve 2^>nul') do set "PGID=%%C"
)
if not defined PGID set "PGID=%FALLBACK%"
set "%OUT%=%PGID%"
exit /b


:RefreshIcons
2>nul "%SystemRoot%\System32\ie4uinit.exe" -ClearIconCache
2>nul "%SystemRoot%\System32\ie4uinit.exe" -show
2>nul taskkill /f /im explorer.exe
start explorer.exe
exit /b
