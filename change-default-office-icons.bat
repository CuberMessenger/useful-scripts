@echo off
setlocal enableextensions enabledelayedexpansion
title Set icons for .docx/.xlsx/.pptx to Word/Excel/PowerPoint app icons

rem --- find the Office executables (works for 32/64-bit, M365, MSI) ---
call :GetAppExe "WINWORD.EXE" WINWORD
call :GetAppExe "EXCEL.EXE" EXCEL
call :GetAppExe "POWERPNT.EXE" POWERPNT

if not defined WINWORD echo [ERROR] Could not find WINWORD.EXE. Is Word installed? & goto :EOF
if not defined EXCEL   echo [ERROR] Could not find EXCEL.EXE.  Is Excel installed? & goto :EOF
if not defined POWERPNT echo [ERROR] Could not find POWERPNT.EXE. Is PowerPoint installed? & goto :EOF

rem --- resolve current ProgIDs for each extension (fallbacks if missing) ---
call :GetProgId ".docx" DOCX_PG "Word.Document.12"
call :GetProgId ".xlsx" XLSX_PG "Excel.Sheet.12"
call :GetProgId ".pptx" PPTX_PG "PowerPoint.Show.12"
call :GetProgId ".doc"  DOC_PG  "Word.Document.8"
call :GetProgId ".xls"  XLS_PG  "Excel.Sheet.8"
call :GetProgId ".ppt"  PPT_PG  "PowerPoint.Show.8"

echo Using ProgIDs:
echo   .docx -> %DOCX_PG%
echo   .xlsx -> %XLSX_PG%
echo   .pptx -> %PPTX_PG%
echo   .doc  -> %DOC_PG%
echo   .xls  -> %XLS_PG%
echo   .ppt  -> %PPT_PG%
echo.

rem --- write per-user DefaultIcon overrides under HKCU\Software\Classes ---
reg add "HKCU\Software\Classes\%DOCX_PG%\DefaultIcon" /ve /t REG_SZ /d "\"%WINWORD%\",0" /f >nul
reg add "HKCU\Software\Classes\%XLSX_PG%\DefaultIcon" /ve /t REG_SZ /d "\"%EXCEL%\",0"   /f >nul
reg add "HKCU\Software\Classes\%PPTX_PG%\DefaultIcon" /ve /t REG_SZ /d "\"%POWERPNT%\",0" /f >nul
reg add "HKCU\Software\Classes\%DOC_PG%\DefaultIcon"  /ve /t REG_SZ /d "\"%WINWORD%\",0"  /f >nul
reg add "HKCU\Software\Classes\%XLS_PG%\DefaultIcon"  /ve /t REG_SZ /d "\"%EXCEL%\",0"    /f >nul
reg add "HKCU\Software\Classes\%PPT_PG%\DefaultIcon"  /ve /t REG_SZ /d "\"%POWERPNT%\",0" /f >nul

echo [OK] Registry updated. Refreshing icon cache...
call :RefreshIcons
echo Done. If some icons didn’t update, sign out and back in.
goto :EOF


rem ===================== helpers =====================

:GetAppExe
rem %~1 = exe name (e.g., WINWORD.EXE)
rem %~2 = out var name (e.g., WINWORD)
set "EXE=%~1"
set "OUT=%~2"
set "APP_PATH="

for /f "skip=2 tokens=1,2,*" %%A in ('reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\%EXE%" /ve 2^>nul') do set "APP_PATH=%%C"
if not defined APP_PATH for /f "skip=2 tokens=1,2,*" %%A in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\%EXE%" /ve 2^>nul') do set "APP_PATH=%%C"
if not defined APP_PATH for /f "skip=2 tokens=1,2,*" %%A in ('reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths\%EXE%" /ve 2^>nul') do set "APP_PATH=%%C"

if not defined APP_PATH (
  for %%I in ("%ProgramFiles%\Microsoft Office\root\Office16\%EXE%") do if exist "%%~fI" set "APP_PATH=%%~fI"
  for %%I in ("%ProgramFiles(x86)%\Microsoft Office\root\Office16\%EXE%") do if exist "%%~fI" set "APP_PATH=%%~fI"
)

if defined APP_PATH set "%OUT%=%APP_PATH%"
exit /b


:GetProgId
rem %~1 = extension (e.g., .docx)
rem %~2 = out var name
rem %~3 = fallback ProgID
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
rem Rebuild icon cache and restart Explorer so changes appear immediately.
2>nul "%SystemRoot%\System32\ie4uinit.exe" -ClearIconCache
2>nul "%SystemRoot%\System32\ie4uinit.exe" -show
2>nul taskkill /f /im explorer.exe
start explorer.exe
exit /b
