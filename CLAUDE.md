# -*- coding: utf-8 -*-
# CFD y+ 計算工具 - 自動發布系統指南

> **自動化開發工作流程**：測試、Lint、版本管理、提交、發布

---

## 📋 目錄

1. [概述](#概述)
2. [版本規則](#版本規則)
3. [使用指南](#使用指南)
4. [發布流程](#發布流程)
5. [常見問題](#常見問題)

---

## 概述

CFD y+ 計算工具配備了完整的自動發布系統，可自動執行以下任務：

| 任務 | 描述 |
|------|------|
| **測試** | 執行 `pytest` 驗證所有功能 |
| **Lint** | 執行 `ruff format` 和 `ruff check --fix` |
| **版本管理** | 根據提交類型自動更新版本號 |
| **提交提交** | 創建語義化提交和版本標籤 |
| **GitHub 推送** | 推送到遠端倉庫和發布版本 |

---

## 版本規則

本專案遵循 **Semantic Versioning (語義化版本)** 規則：

### 版本號格式
```
v MAJOR.MINOR.PATCH
  ↓      ↓      ↓
  │      │      └─ Bug 修復、效能提升 (重新啟動後遞增)
  │      └────────── 新功能 (MINOR 遞增，PATCH 歸零)
  └───────────────── 重大變更 (MAJOR 遞增，MINOR/PATCH 歸零)
```

### Commit 類型對應關係

```bash
git commit -m "fix: 修復 y+ 計算誤差"        # PATCH:  1.0.0 → 1.0.1
git commit -m "feat: 新增溫度修正因子"      # MINOR:  1.0.0 → 1.1.0
git commit -m "breaking: 重構計算核心"      # MAJOR:  1.0.0 → 2.0.0
```

### 提交規範

採用 **Conventional Commits** 格式：

```
<type>: <description>

[optional body]

[optional footer]
```

**常見類型：**
- `feat:` - 新功能（觸發 MINOR 版本更新）
- `fix:` - 錯誤修復（觸發 PATCH 版本更新）
- `docs:` - 文檔變更（不觸發版本更新）
- `style:` - 代碼風格（不觸發版本更新）
- `refactor:` - 代碼重構（不觸發版本更新）
- `perf:` - 效能優化（觸發 PATCH 版本更新）
- `breaking:` - 破壞性變更（觸發 MAJOR 版本更新）

**例子：**
```bash
git commit -m "feat: 支援自定義流體模型"
git commit -m "fix: 修復 Windows 編碼問題"
git commit -m "breaking: 移除舊版 API 支援"
```

---

## 使用指南

### 前置條件

✅ 虛擬環境已啟動（`.venv314`）  
✅ 所有依賴已安裝  
✅ Git 倉庫已初始化  
✅ GitHub 遠端已配置

### 方法 1：PowerShell（推薦 Windows）

```powershell
# 啟動虛擬環境
.\.venv314\Scripts\Activate.ps1

# 執行發布流程
.\release.ps1
```

### 方法 2：批處理檔（快速啟動）

```batch
# Windows 命令行
release.bat
```

### 方法 3：直接使用 Python

```bash
# 任何平台
uv run python release.py
```

---

## 發布流程

### 完整流程圖

```
┌─────────────────────────────────────────────────┐
│  開始 - 檢查環境                                 │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 1️⃣  執行 pytest 測試                            │
│    ❌ 失敗 → 流程中止                            │
│    ✅ 通過 → 進行下一步                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 2️⃣  執行 Lint 檢查與修復                        │
│    - ruff format .                              │
│    - ruff check --fix .                         │
│    ✅ 自動修復代碼問題                           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 3️⃣  檢測變更類型                                │
│    分析 git 日誌 (最近 10 個 commits)           │
│    - breaking: → MAJOR (X.0.0)                 │
│    - feat: → MINOR (1.X.0)                     │
│    - 其他 → PATCH (1.0.X)                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 4️⃣  更新版本號                                  │
│    修改 pyproject.toml 中的 version             │
│    例：1.0.0 → 1.1.0                           │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 5️⃣  提交與標籤化                                │
│    git add -A                                   │
│    git commit -m "✨ 新功能發布: v1.1.0"       │
│    git tag -a v1.1.0 -m "Release v1.1.0"      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 6️⃣  推送到 GitHub                              │
│    git push -u origin main                      │
│    git push origin --tags                       │
│    ✅ 版本在 GitHub 上發布                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│  完成 ✅                                         │
│  訪問: github.com/.../releases/tag/v1.1.0      │
└─────────────────────────────────────────────────┘
```

### 實際執行示例

```bash
# 進行開發和提交
git add main.py
git commit -m "feat: 新增溫度修正因子"

# 準備發布
.venv314\Scripts\Activate.ps1
.\release.ps1

# 輸出示例：
# ================================================================
#  🚀 CFD y+ 計算工具 - 自動發布系統
# ================================================================
# 當前版本: 1.0.0
#
# ▶️  執行 pytest 測試...
# ✅ 執行 pytest 測試 成功
#
# ▶️  執行 Lint 檢查和修復...
#   - 執行 ruff format...
#   - 執行 ruff check --fix...
# ✅ Lint 檢查和修復成功
#
# 📊 偵測到變更類型: minor → v1.1.0
# ✅ 版本號已更新: 1.0.0 → 1.1.0
#
# ▶️  提交變更並創建版本 tag...
# ✅ 已提交: ✨ 新功能發布: v1.1.0
# ✅ 已創建 tag: v1.1.0
#
# ▶️  推送到 GitHub...
# ✅ Commits 推送成功
# ✅ Tags 推送成功
#
# ================================================================
# 📦 發布摘要
# ================================================================
# 📝 版本更新: 1.0.0 → 1.1.0
# 📊 變更類型: MINOR
# ⏰ 發布時間: 2026-02-06 15:30:45
# 🔗 GitHub: https://github.com/wang-yi2/yplus-calculate/releases/tag/v1.1.0
# ================================================================
```

---

## 常見問題

### ❓ 如何查看版本發布歷史？

```bash
# 查看本地 tags
git tag -l

# 查看 GitHub releases 頁面
https://github.com/wang-yi2/yplus-calculate/releases
```

### ❓ 發布流程失敗了怎麼辦？

**檢查清單：**

1. ✅ 虛擬環境已啟動？
   ```bash
   .\.venv314\Scripts\Activate.ps1
   ```

2. ✅ 所有依賴已安裝？
   ```bash
   uv pip install -e ".[dev]"
   ```

3. ✅ 測試通過？
   ```bash
   pytest -v
   ```

4. ✅ Lint 無錯誤？
   ```bash
   ruff format .
   ruff check .
   ```

5. ✅ Git 狀態正常？
   ```bash
   git status
   git log --oneline -5
   ```

### ❓ 如何手動管理版本？

```bash
# 查看當前版本
grep 'version' pyproject.toml

# 手動更新版本
# 編輯 pyproject.toml，更改 version = "X.Y.Z"

# 手動創建標籤
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin --tags
```

### ❓ 如何撤銷發布？

```bash
# 刪除本地標籤
git tag -d v1.1.0

# 刪除遠端標籤
git push origin --delete v1.1.0

# 撤銷最後一次提交
git revert HEAD
git push origin main
```

### ❓ 版本偵測錯誤了怎麼辦？

自動發布系統根據最近 10 個 commits 的類型偵測變更：

- **檢查 breaking:** 關鍵字 → MAJOR
- **檢查 feat:** 關鍵字 → MINOR
- **其他情況** → PATCH

如果偵測不準確，請檢查最近的 commit 訊息是否符合規範：

```bash
# 檢查最近的 commits
git log --oneline -10

# 確保 commit 訊息格式正確
git commit -m "fix: 描述"
git commit -m "feat: 描述"
git commit -m "breaking: 描述"
```

---

## 🔧 系統組件

### release.py
- **功能**：核心發布邏輯（Python 實現）
- **入口點**：`ReleaseManager` 類
- **主要方法**：`test()`, `lint()`, `commit_and_tag()`, `push()`

### release.bat
- **功能**：Windows 批處理快速啟動
- **用途**：一鍵啟動虛擬環境和發布流程
- **優勢**：無需手動啟動虛擬環境

### release.ps1
- **功能**：PowerShell 啟動腳本
- **特性**：彩色輸出、UTF-8 支援
- **選項**：`-DryRun`（測試模式）

---

## 📚 相關文檔

- [ENCODING.md](ENCODING.md) - UTF-8 編碼規範
- [CONTRIBUTING.md](CONTRIBUTING.md) - 開發貢獻指南
- [README.md](README.md) - 項目說明

---

## 🚀 快速參考

| 任務 | 命令 |
|------|------|
| 發布新版本 | `.\release.ps1` |
| 執行測試 | `uv run pytest` |
| Lint 檢查 | `ruff check . --fix` |
| 查看版本 | `grep version pyproject.toml` |
| 查看標籤 | `git tag -l` |
| 查看 commits | `git log --oneline -10` |

---

**最後更新**: 2026-02-06  
**版本**: v1.0.0  
**狀態**: 🟢 運行中
