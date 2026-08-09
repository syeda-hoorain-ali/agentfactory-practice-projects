@echo off
cd /d "%~dp0"
opencode run "run the daily-lint-sweep skill" >> lint-sweep.log 2>&1
