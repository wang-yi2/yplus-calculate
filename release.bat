@REM -*- coding: utf-8 -*-
@REM CFD y+ 計算工具 - Windows 快速發布
@REM 
@REM 使用方式:
@REM   release.ps1                  # 執行完整發布流程
@REM   release.ps1 -DryRun          # 測試模式（不提交）
@REM   release.ps1 -SkipTests       # 跳過測試
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo  CFD y+ 計算工具 - Windows 發布助手
echo ================================================================
echo.

REM 啟動虛擬環境
if exist ".venv314\Scripts\activate.bat" (
    call .venv314\Scripts\activate.bat
    echo ✅ 虛擬環境已啟動
) else (
    echo ❌ 找不到虛擬環境 .venv314
    exit /b 1
)

REM 使用 Python 執行 release.py
python release.py %*

if errorlevel 1 (
    echo.
    echo ❌ 發布流程失敗
    exit /b 1
) else (
    echo.
    echo ✅ 發布流程完成
    exit /b 0
)
