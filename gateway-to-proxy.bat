@echo off
setlocal enabledelayedexpansion

:: This script is used in the scenario when a hyper-V VM connected to the Ethernet through "Default Switch", and it wants to use the host as a proxy server. The proxy server in the view of the VM is the default gateway, but it could change overtime especially when the host is rebooted or the network is changed somehow. This script will detect the default gateway and set it as the system proxy in the VM, while the user need to specify the port and set the proxy in the host. It also copies the gateway IP to the clipboard for easy access.

echo Checking for Ethernet IPv4 Gateway...
:: Replace xxxxx with the desired port number for the proxy
set "port=xxxxx"

:: 1. Read the default IPv4 gateway specifically for "Ethernet"
set "gateway="
for /f "tokens=2 delims=:" %%a in ('netsh interface ipv4 show config name^="Ethernet" ^| findstr "Default Gateway"') do (
    set "gateway=%%a"
    :: Strip leading spaces
    set "gateway=!gateway:~1!"
)

:: Fallback check if "Ethernet" interface isn't found or doesn't have a gateway
if "%gateway%"=="" (
    echo [ERROR] Could not find a default gateway for an interface named "Ethernet".
    echo Checking for any active default gateway instead...
    for /f "tokens=3" %%a in ('route print 0.0.0.0 ^| findstr "\<0.0.0.0\>"') do (
        set "gateway=%%a"
    )
)

:: If still empty, exit
if "%gateway%"=="" (
    echo [ERROR] No default gateway detected. Exiting.
    pause
    exit /b
)

echo Found Gateway: %gateway%

:: 2. Set the system proxy to the gateway IP with port
set "proxy_server=%gateway%:%port%"
echo Setting system proxy to: %proxy_server%

:: Update Registry keys for Internet Settings
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f >nul
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d "%proxy_server%" /f >nul

:: 3. Copy the default IPv4 gateway to the clipboard
echo %gateway%| clip
echo Gateway IP copied to clipboard.

echo.
echo Success! System proxy updated and IP copied to clipboard.
pause