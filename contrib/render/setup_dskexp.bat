@echo off
REM
REM setup_dskexp.bat
REM
REM Author: Rahul R. Sah
REM Email: f1rahulranjan@gmail.com
REM
REM Description:
REM   Downloads and installs DSKEXP, a command-line program from NASA's SPICE
REM   Toolkit that exports data from DSK (Digital Shape Kernel) files to text files.
REM   DSKEXP currently supports type 2 (plate model) DSK segments and can export
REM   to plate-vertex table, vertex-facet (OBJ), and Rosetta/OSIRIS VER formats.
REM
REM Reference:
REM   DSKEXP User's Guide: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/ug/dskexp.html
REM

setlocal

set URL=https://naif.jpl.nasa.gov/pub/naif/utilities/PC_Windows_64bit/dskexp.exe
set INSTALL_DIR=%LOCALAPPDATA%\bin
set INSTALL_PATH=%INSTALL_DIR%\dskexp.exe

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

if exist "%INSTALL_PATH%" (
    echo dskexp already installed
    exit /b 0
)

echo Downloading dskexp...
curl -fSL "%URL%" -o "%INSTALL_PATH%"
echo Done