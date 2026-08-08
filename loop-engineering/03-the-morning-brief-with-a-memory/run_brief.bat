@echo off
cd /d "%~dp0"
opencode run "run the morning-brief skill" >> morning-brief.log 2>&1
