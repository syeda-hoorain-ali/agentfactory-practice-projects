@echo off
REM Lives in .opencode/scripts/, two levels below the project folder,
REM so cd up twice before running.
cd /d "%~dp0../.."
opencode run "run the daily-lint-sweep skill" >> lint-sweep.log 2>&1
