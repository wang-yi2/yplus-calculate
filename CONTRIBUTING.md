# -*- coding: utf-8 -*-
# 貢獻指南

感謝您對 CFD y+ 計算工具的興趣！這份文件提供了貢獻的指南。

## 開發環境設置

### 1. 克隆倉庫

```bash
git clone https://github.com/wang-yi2/yplus-calculate.git
cd yplus-calculate
```

### 2. 建立虛擬環境

```bash
# 使用 uv
uv venv .venv314 --python 3.14
source .venv314/bin/activate  # macOS/Linux
.venv314\Scripts\activate     # Windows
```

### 3. 安裝開發依賴

```bash
uv pip install -e ".[dev]"
uv pip install ruff pytest pytest-cov
```

## 代碼標準

### 編碼標準

- **所有檔案必須使用 UTF-8 編碼**
- Python 檔案須包含 `# -*- coding: utf-8 -*-` 聲明
- 所有文件讀寫必須明確指定 `encoding="utf-8"`

詳見 [ENCODING.md](ENCODING.md)

### 代碼風格

使用 `ruff` 進行代碼檢查和格式化：

```bash
# 自動修復格式
ruff format .

# 檢查並修復 import 等問題
ruff check --fix .

# 最終檢查
ruff check .
```

### 常見 Lint 問題修復

| 問題 | 說明 | 修復方式 |
|-----|------|--------|
| W293 | 空白行包含多餘空格 | `ruff format` 自動修復 |
| E722 | 使用 bare except | 改為 `except Exception:` |
| I001 | import 未排序 | `ruff check --fix` 自動修復 |
| F401 | 未使用的 import | 刪除或加 `# noqa: F401` |

## 提交流程

### 1. 建立功能分支

```bash
git checkout -b feature/your-feature-name
```

### 2. 提交代碼

```bash
# 執行代碼檢查
ruff format .
ruff check --fix .
ruff check .

# 確認通過後提交
git add .
git commit -m "描述您的改動"
```

### 3. 推送並建立 Pull Request

```bash
git push origin feature/your-feature-name
```

然後在 GitHub 上建立 Pull Request

## 測試

運行測試套件：

```bash
pytest tests/ -v
pytest tests/ --cov  # 包含覆蓋率報告
```

## 文檔

- 更新 README.md（如有新功能）
- 在代碼中添加 docstring
- 保持 ENCODING.md 最新

## 報告問題

使用 GitHub Issues 報告 Bug 或建議新功能。

## 行為準則

請遵守本倉庫的行為準則，尊重他人，促進友好的社區環境。

---

感謝您的貢獻！🎉
