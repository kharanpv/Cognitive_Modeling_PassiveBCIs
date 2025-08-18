@echo off
setlocal

echo [*] Bootstrapping Windows environment...

:: -------- Check for Winget --------
where winget >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [!] winget is not available. Please install App Installer from Microsoft Store.
    exit /b 1
)

:: -------- Check Python 3.12+ --------
echo [*] Checking Python installation...
for /f "delims=" %%i in ('python --version 2^>nul') do set PYVER=%%i

set PYOK=0
for /f "tokens=2 delims= " %%v in ("%PYVER%") do (
    set VER=%%v
    for /f "tokens=1,2 delims=." %%a in ("%%v") do (
        if %%a GEQ 3 if %%b GEQ 11 set PYOK=1
    )
)

if %PYOK%==0 (
    echo [!] Installing Python 3.12...
    winget install -e --id Python.Python.3.12
) else (
    echo [✓] Python is already installed: %VER%
)

:: -------- Install Poetry --------
where poetry >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [*] Installing Poetry...
    curl -sSL https://install.python-poetry.org | python -
    set PATH=%USERPROFILE%\AppData\Roaming\Python\Scripts;%USERPROFILE%\.local\bin;%PATH%
) else (
    echo [✓] Poetry is already installed.
)

:: -------- Install FFmpeg --------
where ffmpeg >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [*] Installing FFmpeg...

    :: Try Chocolatey
    where choco >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        choco install ffmpeg -y
    ) else (
        echo [!] Chocolatey not found. Downloading FFmpeg manually...
        powershell -Command "Invoke-WebRequest https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip -OutFile ffmpeg.zip"
        powershell -Command "Expand-Archive ffmpeg.zip -DestinationPath %CD%\ffmpeg"
        set PATH=%CD%\ffmpeg\ffmpeg-*;bin;%PATH%
    )
) else (
    echo [✓] FFmpeg is already installed.
)

:: -------- Install Cygwin --------
set CYGDIR=C:\cygwin64
if not exist "%CYGDIR%" (
    echo [*] Installing Cygwin...
    powershell -Command "Invoke-WebRequest https://cygwin.com/setup-x86_64.exe -OutFile setup-cygwin.exe"
    setup-cygwin.exe -q -P git,make,gcc-core,gcc-g++,cmake,libopencv-devel,libboost-devel,tbb
    del setup-cygwin.exe
) else (
    echo [✓] Cygwin is already installed at %CYGDIR%
)

:: -------- Run Poetry Install --------
echo [*] Running Poetry install...
call poetry install

:: -------- Clone OpenFace --------
if not exist "external\OpenFace" (
    echo [*] Cloning OpenFace...
    git clone https://github.com/TadasBaltrusaitis/OpenFace external\OpenFace
    echo [!] Please use Cygwin to build OpenFace manually:
    echo.
    echo     cd /cygdrive/your/project/path/external/OpenFace
    echo     ./download_models.sh
    echo     cd lib && mkdir build && cd build && cmake .. && make
    echo     cd ../../build && cmake .. && make
    echo.
) else (
    echo [✓] OpenFace already exists.
)

echo [✓] Setup complete.
