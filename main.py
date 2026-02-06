# -*- coding: utf-8 -*-
"""
CFD y+ 計算工具 - 主應用程式
此文件使用 UTF-8 編碼
"""

import sys
import csv
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QGroupBox,
    QFormLayout,
    QRadioButton,
    QButtonGroup,
    QFileDialog,
    QMessageBox,
    QComboBox,
)
from math import log10

# 強制 UTF-8 編碼
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


class CFDYPlusCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        # 預設流體
        self.fluids = {
            "空氣 (25°C)": {"rho": 1.184, "mu": 1.849e-5},
            "空氣 (20°C)": {"rho": 1.204, "mu": 1.810e-5},
            "水 (20°C)": {"rho": 998.2, "mu": 1.002e-3},
            "水 (25°C)": {"rho": 997.0, "mu": 0.894e-3},
        }

        self.initUI()
        self.last_result = None

    def initUI(self):
        self.setWindowTitle("CFD y+ 計算工具")
        self.setGeometry(100, 100, 900, 900)

        # 中心佈局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # ========== 預設流體選擇組 ==========
        preset_group = QGroupBox("預設流體")
        preset_layout = QHBoxLayout()

        self.fluid_combo = QComboBox()
        self.fluid_combo.addItems(self.fluids.keys())
        self.fluid_combo.setCurrentIndex(1)  # 預設空氣 20°C

        load_preset_btn = QPushButton("載入預設")
        load_preset_btn.clicked.connect(self.load_preset)

        preset_layout.addWidget(QLabel("選擇流體："))
        preset_layout.addWidget(self.fluid_combo)
        preset_layout.addWidget(load_preset_btn)
        preset_layout.addStretch()

        preset_group.setLayout(preset_layout)
        main_layout.addWidget(preset_group)

        # ========== 通用輸入參數組 ==========
        common_group = QGroupBox("通用流動參數")
        common_layout = QFormLayout()

        self.rho_input = QLineEdit("1.204")
        self.mu_input = QLineEdit("1.810e-5")
        self.u_input = QLineEdit("10.0")
        self.y_input = QLineEdit("1e-6")
        self.L_input = QLineEdit("1.0")

        common_layout.addRow("密度 ρ (kg/m³):", self.rho_input)
        common_layout.addRow("動力粘度 μ (Pa·s):", self.mu_input)
        common_layout.addRow("流速 U (m/s):", self.u_input)
        common_layout.addRow("第一層高度 y (m):", self.y_input)
        common_layout.addRow("特徵長度 L (m):", self.L_input)

        common_group.setLayout(common_layout)
        main_layout.addWidget(common_group)

        # ========== 計算模式選擇 ==========
        mode_group = QGroupBox("計算模式")
        mode_layout = QHBoxLayout()

        self.mode_group = QButtonGroup()

        mode_blasius = QRadioButton("模式 A：Blasius 公式")
        mode_cf = QRadioButton("模式 B：直接輸入 Cf")
        mode_tau = QRadioButton("模式 C：直接輸入 τw 或 u_τ")

        mode_blasius.setChecked(True)

        self.mode_group.addButton(mode_blasius, 0)
        self.mode_group.addButton(mode_cf, 1)
        self.mode_group.addButton(mode_tau, 2)

        mode_layout.addWidget(mode_blasius)
        mode_layout.addWidget(mode_cf)
        mode_layout.addWidget(mode_tau)
        mode_layout.addStretch()

        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        # ========== 計算模式參數組 ==========
        mode_params_group = QGroupBox("計算模式參數")
        mode_params_layout = QFormLayout()

        self.cf_input = QLineEdit("0.01")
        self.tau_input = QLineEdit("0.1")
        self.u_tau_input = QLineEdit("0.5")

        mode_params_layout.addRow("模式 B - 摩擦系數 Cf:", self.cf_input)
        mode_params_layout.addRow("模式 C - 剪應力 τw (Pa):", self.tau_input)
        mode_params_layout.addRow("模式 C - 摩擦速度 u_τ (m/s):", self.u_tau_input)

        mode_params_group.setLayout(mode_params_layout)
        main_layout.addWidget(mode_params_group)

        # ========== 計算按鈕 ==========
        button_group = QGroupBox("操作")
        button_layout = QHBoxLayout()

        calc_button = QPushButton("計算 y+")
        calc_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        calc_button.clicked.connect(self.calculate)

        clear_button = QPushButton("清空")
        clear_button.clicked.connect(self.clear_inputs)

        export_csv_button = QPushButton("匯出 CSV")
        export_csv_button.clicked.connect(self.export_csv)

        export_txt_button = QPushButton("匯出 TXT")
        export_txt_button.clicked.connect(self.export_txt)

        button_layout.addWidget(calc_button)
        button_layout.addWidget(clear_button)
        button_layout.addWidget(export_csv_button)
        button_layout.addWidget(export_txt_button)

        button_group.setLayout(button_layout)
        main_layout.addWidget(button_group)

        # ========== 結果顯示區 ==========
        result_group = QGroupBox("計算結果")
        result_layout = QVBoxLayout()

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setMinimumHeight(300)
        result_layout.addWidget(self.result_display)

        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)

        main_layout.addStretch()

    def load_preset(self):
        """載入預設流體參數"""
        fluid_name = self.fluid_combo.currentText()
        fluid = self.fluids[fluid_name]

        self.rho_input.setText(str(fluid["rho"]))
        self.mu_input.setText(str(fluid["mu"]))

        self.result_display.setText(f"✓ 已載入預設流體：{fluid_name}")

    def calculate(self):
        """計算 y+"""
        try:
            # 獲取共通參數
            rho = float(self.rho_input.text())
            mu = float(self.mu_input.text())
            u = float(self.u_input.text())
            y = float(self.y_input.text())
            L = float(self.L_input.text())

            # 驗證基本參數
            if any(v <= 0 for v in [rho, mu, u, y, L]):
                self.show_error("所有參數必須為正數")
                return

            # 動力學粘度
            nu = mu / rho

            # 根據模式計算 u_tau
            mode = self.mode_group.checkedId()

            if mode == 0:  # Blasius 模式
                result_text = self._calculate_blasius(rho, mu, u, y, L, nu)
            elif mode == 1:  # 直接輸入 Cf 模式
                cf = float(self.cf_input.text())
                if cf <= 0:
                    self.show_error("摩擦系數 Cf 必須為正數")
                    return
                result_text = self._calculate_cf_mode(cf, u, y, nu)
            elif mode == 2:  # 直接輸入 τw 或 u_τ 模式
                result_text = self._calculate_tau_mode(rho, mu, u, y, L, nu)
            else:
                self.show_error("模式選擇錯誤")
                return

            self.result_display.setText(result_text)
            self.last_result = {
                "rho": rho,
                "mu": mu,
                "u": u,
                "y": y,
                "L": L,
                "result": result_text,
                "mode": mode,
            }

        except ValueError as e:
            self.show_error(f"輸入值無效：{str(e)}\n請檢查數值格式")
        except Exception as e:
            self.show_error(f"計算錯誤：{str(e)}")

    def _calculate_blasius(self, rho, mu, u, y, L, nu):
        """Blasius 公式計算模式"""
        # 計算雷諾數
        Re_x = rho * u * L / mu

        # 使用 Blasius-Schlichting 公式估算摩擦系數（湍流）
        if Re_x < 5e5:
            # 層流邊界層
            Cf = 0.664 / (Re_x**0.5)
        else:
            # 湍流邊界層
            Cf = 0.455 / ((log10(Re_x)) ** 2.58)

        # 計算摩擦速度
        u_tau = (Cf / 2) ** 0.5 * u

        # 計算 y+
        y_plus = y * u_tau / nu

        # 格式化結果
        result = f"""
計算結果（模式 A：Blasius 公式）
═══════════════════════════════════════════
【計算步驟】

1. 流動參數：
   - 密度 ρ = {rho:.4f} kg/m³
   - 動力粘度 μ = {mu:.4e} Pa·s
   - 動力學粘度 ν = {nu:.4e} m²/s
   - 流速 U = {u:.4f} m/s
   - 特徵長度 L = {L:.4f} m

2. 雷諾數：
   Re_x = ρ·U·L/μ = {Re_x:.4e}

3. 摩擦系數（Blasius-Schlichting）：
   C_f = 0.455 / (log₁₀(Re_x))^2.58
   C_f = {Cf:.6e}

4. 摩擦速度：
   u_τ = √(C_f/2) · U = {u_tau:.6f} m/s

5. y+ 計算：
   y⁺ = y · u_τ / ν = {y_plus:.6f}

═══════════════════════════════════════════
【最終結果】
y⁺ = {y_plus:.6f}

【網格評估】
"""
        if y_plus < 1:
            result += "✓ 精確解析邊界層（y⁺ < 1）\n   適用於 LES/DNS，需要精細網格"
        elif 1 <= y_plus <= 5:
            result += "✓ 標準精確解析範圍（1 ≤ y⁺ ≤ 5）\n   推薦用於精確的 RANS 模擬"
        elif 5 < y_plus <= 30:
            result += "⚠ 介於兩種方法之間（5 < y⁺ ≤ 30）\n   不推薦，建議調整網格"
        elif 30 < y_plus <= 300:
            result += "✓ 壁面函數適用範圍（30 < y⁺ ≤ 300）\n   適用於壁面函數法 RANS"
        else:
            result += "⚠ 過於粗糙的網格（y⁺ > 300）\n   需要更精細的邊界層網格"

        return result

    def _calculate_cf_mode(self, cf, u, y, nu):
        """直接輸入 Cf 的計算模式"""
        # 計算摩擦速度
        u_tau = (cf / 2) ** 0.5 * u

        # 計算 y+
        y_plus = y * u_tau / nu

        result = f"""
計算結果（模式 B：直接輸入摩擦系數）
═══════════════════════════════════════════
【計算步驟】

1. 輸入參數：
   - 流速 U = {u:.4f} m/s
   - 摩擦系數 C_f = {cf:.6e}
   - 動力學粘度 ν = {nu:.4e} m²/s
   - 第一層高度 y = {y:.4e} m

2. 摩擦速度：
   u_τ = √(C_f/2) · U = {u_tau:.6f} m/s

3. y+ 計算：
   y⁺ = y · u_τ / ν = {y_plus:.6f}

═══════════════════════════════════════════
【最終結果】
y⁺ = {y_plus:.6f}

【網格評估】
"""
        if y_plus < 1:
            result += "✓ 精確解析邊界層（y⁺ < 1）"
        elif 1 <= y_plus <= 5:
            result += "✓ 標準精確解析範圍（1 ≤ y⁺ ≤ 5）"
        elif 30 < y_plus <= 300:
            result += "✓ 壁面函數適用範圍（30 < y⁺ ≤ 300）"
        else:
            result += "⚠ 建議調整網格或摩擦係數"

        return result

    def _calculate_tau_mode(self, rho, mu, u, y, L, nu):
        """直接輸入剪應力或摩擦速度的計算模式"""
        use_tau = True

        try:
            tau = float(self.tau_input.text())
            if tau <= 0:
                # 嘗試使用 u_tau
                use_tau = False
                u_tau = float(self.u_tau_input.text())
                if u_tau <= 0:
                    self.show_error("剪應力 τw 或摩擦速度 u_τ 必須為正數")
                    return None
        except ValueError:
            use_tau = False
            try:
                u_tau = float(self.u_tau_input.text())
                if u_tau <= 0:
                    self.show_error("剪應力 τw 或摩擦速度 u_τ 必須為正數")
                    return None
            except ValueError:
                self.show_error("請輸入有效的 τw 或 u_τ 值")
                return None

        if use_tau:
            # 從剪應力計算摩擦速度
            u_tau = (tau / rho) ** 0.5
            tau_display = tau
        else:
            # 直接使用摩擦速度
            tau_display = u_tau**2 * rho

        # 計算 y+
        y_plus = y * u_tau / nu

        result = f"""
計算結果（模式 C：直接輸入剪應力或摩擦速度）
═══════════════════════════════════════════
【計算步驟】

1. 輸入參數：
   - 密度 ρ = {rho:.4f} kg/m³
   - 動力學粘度 ν = {nu:.4e} m²/s
   - 第一層高度 y = {y:.4e} m

2. 摩擦參數：
"""
        if use_tau:
            result += f"   - 剪應力 τ_w = {tau_display:.6e} Pa\n"
            result += f"   - 摩擦速度 u_τ = √(τ_w/ρ) = {u_tau:.6f} m/s\n"
        else:
            result += f"   - 摩擦速度 u_τ = {u_tau:.6f} m/s\n"
            result += f"   - 對應剪應力 τ_w = u_τ²·ρ = {tau_display:.6e} Pa\n"

        result += f"""
3. y+ 計算：
   y⁺ = y · u_τ / ν = {y_plus:.6f}

═══════════════════════════════════════════
【最終結果】
y⁺ = {y_plus:.6f}

【網格評估】
"""
        if y_plus < 1:
            result += "✓ 精確解析邊界層（y⁺ < 1）"
        elif 1 <= y_plus <= 5:
            result += "✓ 標準精確解析範圍（1 ≤ y⁺ ≤ 5）"
        elif 30 < y_plus <= 300:
            result += "✓ 壁面函數適用範圍（30 < y⁺ ≤ 300）"
        else:
            result += "⚠ 建議調整網格"

        return result

    def show_error(self, message):
        """顯示錯誤信息"""
        self.result_display.setText(f"❌ 錯誤：\n{message}")

    def clear_inputs(self):
        """清空輸入框"""
        self.rho_input.setText("1.204")
        self.mu_input.setText("1.810e-5")
        self.u_input.setText("10.0")
        self.y_input.setText("1e-6")
        self.L_input.setText("1.0")
        self.cf_input.setText("0.01")
        self.tau_input.setText("0.1")
        self.u_tau_input.setText("0.5")
        self.result_display.setText("")
        self.last_result = None

    def export_csv(self):
        """匯出為 CSV 檔案"""
        if not self.last_result:
            QMessageBox.warning(self, "警告", "請先執行計算")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "儲存 CSV 檔案", "", "CSV 檔案 (*.csv)"
        )

        if file_path:
            try:
                # 明確指定 UTF-8 編碼（含 BOM）確保中文正確顯示
                with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f)

                    # 寫入標題
                    writer.writerow(
                        [
                            "CFD y+ 計算結果",
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        ]
                    )
                    writer.writerow([])

                    # 寫入參數
                    writer.writerow(["參數", "數值", "單位"])
                    writer.writerow(["密度 ρ", self.last_result["rho"], "kg/m³"])
                    writer.writerow(["動力粘度 μ", self.last_result["mu"], "Pa·s"])
                    writer.writerow(["流速 U", self.last_result["u"], "m/s"])
                    writer.writerow(["第一層高度 y", self.last_result["y"], "m"])
                    writer.writerow(["特徵長度 L", self.last_result["L"], "m"])

                    writer.writerow([])
                    writer.writerow(
                        [
                            "計算模式",
                            ["Blasius 公式", "直接輸入 Cf", "直接輸入 τw/u_τ"][
                                self.last_result["mode"]
                            ],
                        ]
                    )
                    writer.writerow([])

                    # 寫入結果文本
                    writer.writerow(["計算結果"])
                    for line in self.last_result["result"].split("\n"):
                        writer.writerow([line])

                QMessageBox.information(self, "成功", f"已匯出到：{file_path}")

            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"匯出失敗：{str(e)}")

    def export_txt(self):
        """匯出為文字檔案"""
        if not self.last_result:
            QMessageBox.warning(self, "警告", "請先執行計算")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "儲存文字檔案", "", "文字檔案 (*.txt)"
        )

        if file_path:
            try:
                # 明確指定 UTF-8 編碼
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("═" * 50 + "\n")
                    f.write("CFD y+ 計算工具 - 詳細報告\n")
                    f.write(
                        f"生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    f.write("═" * 50 + "\n\n")

                    f.write("【輸入參數】\n")
                    f.write(f"密度 ρ: {self.last_result['rho']:.6f} kg/m³\n")
                    f.write(f"動力粘度 μ: {self.last_result['mu']:.6e} Pa·s\n")
                    f.write(f"流速 U: {self.last_result['u']:.6f} m/s\n")
                    f.write(f"第一層高度 y: {self.last_result['y']:.6e} m\n")
                    f.write(f"特徵長度 L: {self.last_result['L']:.6f} m\n")
                    f.write(
                        f"計算模式: {['Blasius 公式', '直接輸入 Cf', '直接輸入 τw/u_τ'][self.last_result['mode']]}\n\n"
                    )

                    f.write("【計算結果】\n")
                    f.write(self.last_result["result"])
                    f.write("\n\n")

                    f.write("═" * 50 + "\n")
                    f.write("報告結束\n")
                    f.write("═" * 50 + "\n")

                QMessageBox.information(self, "成功", f"已匯出到：{file_path}")

            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"匯出失敗：{str(e)}")


def main():
    app = QApplication(sys.argv)
    calculator = CFDYPlusCalculator()
    calculator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
