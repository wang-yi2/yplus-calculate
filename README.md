# CFD y+ 計算工具

[![CI Status](https://github.com/wang-yi2/yplus-calculate/workflows/Tests/badge.svg)](https://github.com/wang-yi2/yplus-calculate/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub stars](https://img.shields.io/github/stars/wang-yi2/yplus-calculate.svg?style=social&label=Stars)](https://github.com/wang-yi2/yplus-calculate)
[![GitHub forks](https://img.shields.io/github/forks/wang-yi2/yplus-calculate.svg?style=social&label=Fork)](https://github.com/wang-yi2/yplus-calculate)
[![GitHub issues](https://img.shields.io/github/issues/wang-yi2/yplus-calculate.svg)](https://github.com/wang-yi2/yplus-calculate/issues)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=wang-yi2/yplus-calculate&type=Date)](https://star-history.com/#wang-yi2/yplus-calculate&Date)

---

## 📋 項目概述

CFD y+ 計算工具是一個基於 PySide6 的圖形化應用程式，用於計算計算流體動力學（CFD）中的無量綱數 **y+（y-plus）**。

y+ 是評估邊界層網格是否適當的關鍵指標，幫助工程師確定是否能充分解析粘性底層或是否適合使用壁面函數。

---

## 🎯 主要功能

### 1. **預設流體管理**
- 🌬️ 空氣 (20°C / 25°C)
- 💧 水 (20°C / 25°C)
- ⚡ 一鍵載入預設流體參數

### 2. **三種計算模式**

#### 模式 A：Blasius 公式 ⭐
```
流程：密度、粘度、流速、長度 → 雷諾數 → 摩擦係數 → 摩擦速度 → y+
```
- 自動計算邊界層雷諾數
- 區分層流和湍流邊界層
- 適用於一般流動分析

#### 模式 B：直接輸入摩擦係數
```
流程：摩擦係數 Cf → 摩擦速度 → y+
```
- 直接使用已知的摩擦係數
- 加快計算速度

#### 模式 C：直接輸入剪應力或摩擦速度
```
流程：剪應力 τw 或 摩擦速度 u_τ → y+
```
- 從 CFD 求解器直接輸入壁面剪應力
- 支援摩擦速度直接輸入

### 3. **智能網格評估**
根據計算結果提供專業的網格評估建議

### 4. **數據匯出功能**
- 📊 **CSV 匯出**：參數表、計算結果、時間戳
- 📄 **TXT 匯出**：詳細計算報告（含公式、步驟、評估）

---

## 📐 y+ 物理意義

### y+ 的定義

$$y^+ = \frac{y \cdot u_\tau}{\nu}$$

其中：
- $y$ ：第一個網格節點到牆面的距離（m）
- $u_\tau$ ：摩擦速度 = $\sqrt{\frac{\tau_w}{\rho}}$ （m/s）
- $\nu$ ：動力學粘度 = $\frac{\mu}{\rho}$ （m²/s）
- $\tau_w$ ：牆面剪應力（Pa）

---

## 🌊 邊界層流場示意圖

### 邊界層結構與 y+ 分佈

```
                   自由流 (U∞)
     ────────────────────────────────────────────
                                   
          速度漸變區域（邊界層）
     ┌────────────────┐
     │   外層 (Outer) │  y+ > 30-300
     │  邊界層區域    │
     ├────────────────┤
  y  │  緩衝層 Buffer │  y+ ≈ 5-30  ⚠️ 不推薦
  ^  │               │
  │  ├────────────────┤
  │  │ 粘性底層       │  y+ < 1      ✅ 精確解析
  │  │ (Viscous      │
  │  │  Sublayer)    │
  │  ├────────────────┤
  │  │               │
  └──→ ─────────→─────────→─────────→
      U=0          牆面           U=U∞
    (No-slip)      (Wall)      (Free stream)

     ╔═══════════════════════════════════════╗
     ║  對數律區域 (Logarithmic Layer)       ║
     ║  U+ = (1/κ)·ln(y+) + C               ║
     ║  κ ≈ 0.41 (Von Kármán 常數)          ║
     ╚═══════════════════════════════════════╝
```

---

## 📊 y+ 值的典型範圍與應用

| y+ 範圍 | 說明 | 適用模型 | 推薦場景 |
|--------|------|--------|--------|
| **y+ < 1** | 精確解析邊界層 | LES / DNS / 精確 RANS | 複雜流動、分離流 |
| **1 ≤ y+ ≤ 5** | 標準精確範圍 | 精確 RANS（k-ε/k-ω） | 推薦選擇 ✅ |
| **5 < y+ < 30** | 介於兩者之間 | 不適用 | ⚠️ 需要調整網格 |
| **30 < y+ ≤ 300** | 壁面函數適用 | 壁面函數法 RANS | 粗糙網格可用 |
| **y+ > 300** | 過於粗糙 | 不適用 | ❌ 需要更細網格 |

---

## 🔬 計算公式詳解

### 摩擦係數計算（Blasius-Schlichting 公式）

**層流邊界層** ($Re_x < 5 \times 10^5$)：
$$C_f = \frac{0.664}{\sqrt{Re_x}}$$

**湍流邊界層** ($Re_x \geq 5 \times 10^5$)：
$$C_f = \frac{0.455}{(\log_{10}Re_x)^{2.58}}$$

其中雷諾數：
$$Re_x = \frac{\rho \cdot U \cdot L}{\mu}$$

### 摩擦速度

$$u_\tau = \sqrt{\frac{C_f}{2}} \cdot U$$

或

$$u_\tau = \sqrt{\frac{\tau_w}{\rho}}$$

---

## 💻 使用指南

### 系統要求
- **Python 版本**：3.14+
- **套件管理器**：uv
- **虛擬環境**：`.venv314`
- **文字編碼**：UTF-8（所有檔案）

### 文件編碼標準

此專案遵循嚴格的 **UTF-8 編碼標準**：
- ✅ 所有 `.py` 檔案包含 `# -*- coding: utf-8 -*-` 聲明
- ✅ 所有檔案讀寫明確指定 `encoding="utf-8"`
- ✅ CSV 匯出使用 `encoding="utf-8-sig"` 確保 Excel 相容
- ✅ Windows 批次檔設定 `PYTHONIOENCODING=utf-8`

詳見 [ENCODING.md](ENCODING.md) 編碼規範文件。

### 安裝與啟動

```bash
# 進入專案目錄
cd /path/to/project

# 方法 1：啟動虛擬環境並執行（推薦）
.venv314\Scripts\activate
python main.py

# 方法 2：使用 Windows 批次檔（自動設定編碼）
run.bat

# 方法 3：設定環境變數後執行
set PYTHONIOENCODING=utf-8
python main.py
```

### 使用步驟

1. **選擇流體**
   - 從下拉選單選擇預設流體（空氣或水）
   - 點擊「載入預設」自動填入參數

2. **輸入流動參數**
   - 密度 ρ (kg/m³)
   - 動力粘度 μ (Pa·s)
   - 流速 U (m/s)
   - 第一層高度 y (m)
   - 特徵長度 L (m)

3. **選擇計算模式**
   - **模式 A**：自動計算（推薦新手）
   - **模式 B**：輸入已知 Cf
   - **模式 C**：輸入 τw 或 u_τ

4. **點擊「計算 y+」**
   - 查看詳細計算結果
   - 檢查網格評估建議

5. **匯出結果**
   - CSV：適合數據處理
   - TXT：適合報告編寫

---

## 📈 計算範例

### 範例 1：空氣流過平板（Blasius 公式）

| 參數 | 數值 | 單位 |
|-----|------|------|
| 密度 ρ | 1.204 | kg/m³ |
| 動力粘度 μ | 1.810×10⁻⁵ | Pa·s |
| 流速 U | 10.0 | m/s |
| 特徵長度 L | 1.0 | m |
| 第一層高度 y | 1.0×10⁻⁶ | m |

**計算步驟：**
```
1. Re_x = 1.204 × 10.0 × 1.0 / (1.810×10⁻⁵) = 6.65×10⁵

2. 湍流邊界層：C_f = 0.455 / (log₁₀(6.65×10⁵))^2.58 = 2.87×10⁻³

3. u_τ = √(2.87×10⁻³/2) × 10.0 = 0.120 m/s

4. ν = 1.810×10⁻⁵ / 1.204 = 1.504×10⁻⁵ m²/s

5. y⁺ = 1.0×10⁻⁶ × 0.120 / (1.504×10⁻⁵) = 0.0798
```

**結果**：y⁺ ≈ 0.08 → ✅ 精確解析邊界層

---

### 範例 2：水流計算（直接輸入 Cf）

| 參數 | 數值 | 單位 |
|-----|------|------|
| 密度 ρ | 998.2 | kg/m³ |
| 動力粘度 μ | 1.002×10⁻³ | Pa·s |
| 流速 U | 2.0 | m/s |
| 摩擦係數 Cf | 0.005 | - |
| 第一層高度 y | 5.0×10⁻⁵ | m |

**結果**：y⁺ ≈ 2.5 → ✅ 標準精確解析範圍

---

## 🔧 進階設定

### 常見問題

**Q：y+ 值太大怎麼辦？**
- ❌ 增加流速：錯誤，會增加 u_τ
- ✅ 減小第一層高度 y：正確，直接減少 y+
- ✅ 使用壁面函數法：適合粗網格

**Q：邊界層 y+ 應該設為多少？**
- 對於 k-ε 或 k-ω 模型：**y⁺ < 1** 或 **y⁺ > 30**
- 避免 **5 < y⁺ < 30** 的中間區域
- 精確性要求高時：選擇 **y⁺ < 1**

**Q：如何驗證計算結果？**
```python
# 驗證公式
y_plus = y * (sqrt(rho * tau_w)) / mu
# 應與程式計算結果相符
```

---

## 📦 專案結構

```
project/
├── main.py                 # 主應用程式（UTF-8 編碼）
├── run.bat                 # Windows 快速啟動指令檔
├── .venv314/              # Python 3.14 虛擬環境
├── README.md              # 項目說明文件
├── ENCODING.md            # UTF-8 編碼規範
├── pyproject.toml         # Python 專案配置（UTF-8）
├── pytest.ini             # pytest 測試配置（UTF-8）
└── tests/                 # (可選) 測試目錄
    ├── test_calculator.py
    └── fixtures/          # 測試數據（UTF-8 編碼）
```

**重要**：所有檔案均採用 UTF-8 編碼存儲。

---

## 🚀 特色功能亮點

✨ **用戶友好的界面**
- 直觀的參數輸入佈局
- 即時計算結果顯示
- 清晰的網格評估建議

🧪 **三種計算模式**
- 滿足不同工作流程
- 支援多種輸入方式

📊 **完整的數據管理**
- CSV 和 TXT 匯出
- 保存計算歷史
- 便於報告編寫

🎨 **科學的結果呈現**
- 詳細的計算步驟
- 清晰的評估等級
- 專業的建議反饋

---

## 📚 參考文獻

1. **Schlichting, H. (1979)**. *Boundary-Layer Theory* (7th ed.). McGraw-Hill.

2. **ANSYS Fluent Theory Guide**. 邊界層網格最佳實踐指南。

3. **Cebeci, T., & Bradshaw, P. (1977)**. *Momentum Transfer in Boundary Layers*. Hemisphere Publishing.

4. **Pope, S. B. (2000)**. *Turbulent Flows*. Cambridge University Press.

---

## 💡 開發資訊

| 項目 | 詳情 |
|-----|------|
| 開發語言 | Python 3.14 |
| GUI 框架 | PySide6 6.10.2 |
| 套件管理 | uv |
| 環境名稱 | .venv314 |
| 創建日期 | 2026-02-06 |

---

## 📞 支援

如有問題或建議，請檢查：
1. Python 版本是否為 3.14+
2. PySide6 是否正確安裝
3. 虛擬環境是否已啟動
4. 輸入參數單位是否正確

---

## 📄 許可證

此項目為開源項目，可自由使用和修改。

---

**祝您使用愉快！** 🎉

*CFD y+ 計算工具 - 讓邊界層網格設定變得簡單*
