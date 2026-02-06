# -*- coding: utf-8 -*-
"""
CFD y+ 計算工具 - 文字編碼規範
UTF-8 Encoding Standard Documentation
"""

## 📋 編碼標準總覽

本專案所有文字檔案一律採用 **UTF-8** 編碼，確保跨平台相容性和中文正確顯示。

---

## 📝 Python 文件 (.py)

### 檔案頭部

每個 Python 檔案**必須**在第一行添加編碼聲明：

```python
# -*- coding: utf-8 -*-
"""
模組說明
此文件使用 UTF-8 編碼
"""
```

### 標準庫導入

```python
import io
import sys

# 強制 UTF-8 編碼（推薦）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```

### 文件讀寫

**正確做法 ✅**：
```python
# 讀取文件
with open("file.txt", encoding="utf-8") as f:
    content = f.read()

# 寫入文件
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("中文內容")

# CSV 匯出（含 BOM，確保 Excel 正確顯示）
with open("file.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
```

**錯誤做法 ❌**：
```python
with open("file.txt") as f:  # 可能使用系統預設編碼
    content = f.read()
```

---

## 🔧 組態文件 (.toml, .ini, .yml)

### pyproject.toml

```toml
[project]
requires-python = ">=3.14"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.poetry]
encoding = "utf-8"
```

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py

# UTF-8 編碼說明：讀寫測試數據時明確指定 encoding="utf-8"
```

---

## 🧪 測試文件 (.py)

### 規範寫法

```python
# -*- coding: utf-8 -*-
import pytest

class TestCFDCalculator:
    """CFD 計算器測試類"""
    
    def test_blasius_formula(self):
        """測試 Blasius 公式計算"""
        # 讀取測試數據 - 明確指定 UTF-8
        with open("tests/fixtures/test_data.txt", encoding="utf-8") as f:
            test_data = f.read()
        
        # 驗證中文輸出
        assert "計算結果" in test_data
    
    def test_export_csv(self, tmp_path):
        """測試 CSV 匯出功能"""
        # 寫入測試文件 - 明確指定 UTF-8
        csv_file = tmp_path / "result.csv"
        with open(csv_file, "w", encoding="utf-8-sig") as f:
            f.write("參數,數值\n密度,1.204\n")
        
        # 驗證內容
        with open(csv_file, encoding="utf-8") as f:
            content = f.read()
            assert "密度" in content
```

---

## 💻 Windows 終端設定

### PowerShell

在執行 Python 前設定：
```powershell
$env:PYTHONIOENCODING = "utf-8"
python main.py
```

### CMD 或 Batch 檔案 (.bat)

```batch
@echo off
REM 設定 UTF-8 編碼
set PYTHONIOENCODING=utf-8

REM 設定終端代碼頁為 UTF-8
chcp 65001 >nul

python main.py
```

---

## 🐧 Linux/macOS 終端設定

### Bash/Zsh

```bash
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
python main.py
```

### 也可在虛擬環境啟動時設定

```bash
source .venv314/bin/activate
export PYTHONIOENCODING=utf-8
python main.py
```

---

## 🔄 CI/CD 環境設定

### GitHub Actions

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.14"
      
      - name: Set UTF-8 encoding
        run: |
          export LANG=en_US.UTF-8
          export LC_ALL=en_US.UTF-8
      
      - name: Run tests
        env:
          PYTHONIOENCODING: utf-8
        run: pytest
```

### Windows CI (AppVeyor, etc.)

```yaml
environment:
  PYTHONIOENCODING: utf-8
  LANG: en_US.UTF-8

before_test:
  - chcp 65001

test_script:
  - python -m pytest
```

---

## 📋 檔案檢查清單

| 檔案類型 | 編碼 | 驗證方法 |
|---------|------|--------|
| `.py` | UTF-8 | `file -i script.py` 或在編輯器檢查 |
| `.md` | UTF-8 | 在瀏覽器預覽中文是否正確 |
| `.txt` | UTF-8 | 用文字編輯器確認編碼選項 |
| `.csv` | UTF-8 with BOM | Excel 開啟中文不亂碼 |
| `.toml`/`.ini` | UTF-8 | 驗證設定是否被正確解析 |

---

## 🧬 驗證編碼工具

### Linux/macOS

```bash
# 檢查檔案編碼
file -i main.py

# 顯示為 UTF-8
# main.py: text/plain; charset=utf-8 ✅

# 轉換為 UTF-8（如需要）
iconv -f ISO-8859-1 -t UTF-8 old_file.txt -o new_file.txt
```

### Windows PowerShell

```powershell
# 檢查編碼
Get-Content main.py -Encoding UTF8 -ReadCount 1 | Select-Object -First 1

# 或使用 Python
python -c "with open('main.py', 'rb') as f: print(f.read(20))"
```

---

## ⚠️ 常見問題

### Q：為什麼 CSV 檔案要用 `utf-8-sig`？
**A**：`utf-8-sig` 會在檔案開頭添加 BOM (Byte Order Mark)，讓 Excel 在 Windows 下自動識別為 UTF-8，避免中文亂碼。

### Q：在 Windows CMD 中顯示中文亂碼？
**A**：設定 `chcp 65001` 將終端代碼頁改為 UTF-8，或在 `.bat` 檔中設定 `PYTHONIOENCODING=utf-8`。

### Q：測試文件讀寫時需要指定編碼嗎？
**A**：**必須**明確指定 `encoding="utf-8"`，不要依賴系統預設編碼。

### Q：pyproject.toml 是否也要 UTF-8？
**A**：是的，所有設定檔都應該使用 UTF-8 編碼。

---

## ✅ 編碼檢查清單

- [ ] 所有 `.py` 檔案有 `# -*- coding: utf-8 -*-` 聲明
- [ ] 所有檔案讀寫明確指定 `encoding="utf-8"` 或 `encoding="utf-8-sig"`
- [ ] 環境變數 `PYTHONIOENCODING=utf-8` 已設定
- [ ] Windows `.bat` 檔案包含 `chcp 65001` 和 `set PYTHONIOENCODING=utf-8`
- [ ] CI/CD 設定包含 `LANG=en_US.UTF-8` 和 `LC_ALL=en_US.UTF-8`
- [ ] CSV 匯出使用 `encoding="utf-8-sig"` 確保 Excel 相容
- [ ] 所有 `.md`、`.toml`、`.ini`、`.txt` 檔案以 UTF-8 存檔

---

## 📚 參考資源

1. **PEP 263** - Defining Python Source Code Encodings
   https://www.python.org/dev/peps/pep-0263/

2. **Python 官方文檔** - Text Encoding Support
   https://docs.python.org/3/library/codecs.html

3. **UTF-8 標準** - The Unicode Standard
   https://unicode.org/

4. **ANSYS Fluent** - 輸入檔案編碼指南

---

**確保項目編碼統一，讓國際化開發變得簡單！** 🌍

*最後更新：2026-02-06*
