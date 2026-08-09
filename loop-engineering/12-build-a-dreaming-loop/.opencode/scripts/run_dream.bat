@echo off
cd /d "%~dp0..\.."
opencode run "run the dreaming-loop skill" >> dreaming-loop.log 2>&1
