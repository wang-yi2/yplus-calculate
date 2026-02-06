# -*- coding: utf-8 -*-
# CFD y+ 計算工具 - PowerShell 發布腳本
#
# 使用方式:
#   ./release.ps1                  # 執行完整發布流程
#   ./release.ps1 -DryRun          # 測試模式（不提交）
#   ./release.ps1 -SkipTests       # 跳過測試

param(
    [switch]$DryRun = $false,
    [switch]$SkipTests = $false
)

# 設定 UTF-8 編碼
$OutputEncoding = [System.Text.UTF8Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::UTF8

# 顏色定義
function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "▶️  $Message" -ForegroundColor Cyan
}

# 檢查虛擬環境
Write-Info "檢查虛擬環境..."
$venvPath = ".\.venv314"
if (-not (Test-Path "$venvPath\Scripts\Activate.ps1")) {
    Write-Error "找不到虛擬環境 $venvPath"
    exit 1
}

# 啟動虛擬環境
& "$venvPath\Scripts\Activate.ps1"
Write-Success "虛擬環境已啟動"

# 執行 Python release 腳本
Write-Info "執行自動發布流程..."
Write-Info ""

python release.py

$releaseExitCode = $LASTEXITCODE
if ($releaseExitCode -ne 0) {
    Write-Error "發布流程失敗"
    exit 1
}

Write-Success "發布流程完成"
exit 0
