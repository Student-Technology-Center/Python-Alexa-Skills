@echo off

RMDIR /S /Q skill_env
MKDIR skill_env

pip install -r requirements.txt -t skill_env
xcopy /s lambda skill_env
