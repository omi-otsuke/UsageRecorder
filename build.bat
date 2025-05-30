@echo off
setlocal

pushd "%~dp0"
pyinstaller --noconsole --name UsageRecorder --add-data "conf\*.toml;conf" source\ura.py
move dist\UsageRecorder\_internal\conf dist\UsageRecorder
mkdir dist\UsageRecorder\log
popd

pause
