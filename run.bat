@echo off
REM -*- coding: utf-8 -*-
REM CFD y+ 計算工具啟動腳本
REM 設定 UTF-8 編碼環境

cd /d c:\Users\USER\Desktop\project

REM 設定 Python UTF-8 輸出編碼
set PYTHONIOENCODING=utf-8

REM 設定終端代碼頁為 UTF-8 (65001)
chcp 65001 >nul

REM 啟動虛擬環境
call .venv314\Scripts\activate.bat

REM 執行應用程式
python main.py

pause
