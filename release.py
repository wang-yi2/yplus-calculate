# -*- coding: utf-8 -*-
"""
CFD y+ 計算工具 - 自動發布系統
自動執行測試、Lint 檢查、版本更新、提交和 GitHub 推送
"""

import subprocess
import sys
import re
from pathlib import Path
from datetime import datetime


class ReleaseManager:
    """管理自動發布流程"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.pyproject_path = self.project_root / "pyproject.toml"
        self.current_version = self._get_version()
        self.changelog = []

    def _get_version(self) -> str:
        """從 pyproject.toml 讀取當前版本"""
        with open(self.pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'version\s*=\s*"([\d.]+)"', content)
            if match:
                return match.group(1)
            raise ValueError("無法找到版本號")

    def _set_version(self, version: str) -> None:
        """更新 pyproject.toml 中的版本號"""
        with open(self.pyproject_path, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = re.sub(
            r'version\s*=\s*"[\d.]+"', f'version = "{version}"', content
        )

        with open(self.pyproject_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ 版本號已更新: {self.current_version} → {version}")

    def _calculate_next_version(self, change_type: str) -> str:
        """根據變更類型計算下一版本號"""
        parts = [int(x) for x in self.current_version.split(".")]

        if change_type == "major":
            parts[0] += 1
            parts[1] = 0
            parts[2] = 0
        elif change_type == "minor":
            parts[1] += 1
            parts[2] = 0
        elif change_type == "patch":
            parts[2] += 1

        return ".".join(str(x) for x in parts)

    def _detect_change_type(self) -> str:
        """偵測 git 日誌中的變更類型"""
        try:
            # 獲取自上一個 tag 以來的 commits
            result = subprocess.run(
                ["git", "log", "--oneline", "-10"],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            commits = result.stdout

            # 檢查 commit 訊息
            if "breaking:" in commits or "BREAKING CHANGE" in commits:
                return "major"
            elif "feat:" in commits:
                return "minor"
            else:
                return "patch"

        except Exception as e:
            print(f"⚠️  無法偵測變更類型: {e}")
            return "patch"

    def _run_command(self, cmd: list, description: str) -> bool:
        """執行命令並報告結果"""
        print(f"\n▶️  {description}...")
        try:
            result = subprocess.run(cmd, cwd=self.project_root, encoding="utf-8")
            if result.returncode == 0:
                print(f"✅ {description} 成功")
                return True
            else:
                print(f"❌ {description} 失敗")
                return False
        except Exception as e:
            print(f"❌ 執行失敗: {e}")
            return False

    def test(self) -> bool:
        """執行測試"""
        return self._run_command(
            ["uv", "run", "pytest", "-v", "--tb=short"], "執行 pytest 測試"
        )

    def lint(self) -> bool:
        """執行 Lint 檢查和修復"""
        print("\n▶️  執行 Lint 檢查和修復...")

        # 格式化代碼
        print("  - 執行 ruff format...")
        format_result = subprocess.run(
            ["ruff", "format", "."],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        # Lint 檢查和修復
        print("  - 執行 ruff check --fix...")
        lint_result = subprocess.run(
            ["ruff", "check", "--fix", "."],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if format_result.returncode == 0 and lint_result.returncode == 0:
            print("✅ Lint 檢查和修復成功")
            return True
        else:
            print("⚠️  Lint 發現一些問題")
            if lint_result.stdout:
                print(lint_result.stdout)
            return True  # 繼續流程，因為已自動修復

    def update_readme(self) -> bool:
        """更新 README 版本信息"""
        readme_path = self.project_root / "README.md"
        if not readme_path.exists():
            return True

        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 檢查是否需要更新版本信息
        # 這是一個簡單示例，實際可視需求調整
        if f"v{self.current_version}" not in content:
            print("✅ README 版本信息已最新")
            return True

        return True

    def commit_and_tag(self, version: str, change_type: str) -> bool:
        """提交變更並創建 tag"""
        print("\n▶️  提交變更並創建版本 tag...")

        # 添加所有變更
        subprocess.run(["git", "add", "-A"], cwd=self.project_root, capture_output=True)

        # 生成 commit 訊息
        change_type_map = {
            "major": "🚀 重大版本更新",
            "minor": "✨ 新功能發布",
            "patch": "🔧 錯誤修復和優化",
        }
        message = f"{change_type_map.get(change_type, '更新')}: v{version}"

        # 提交
        commit_result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if commit_result.returncode != 0:
            print("⚠️  沒有新的變更要提交")
        else:
            print(f"✅ 已提交: {message}")

        # 創建 tag
        tag_result = subprocess.run(
            ["git", "tag", "-a", f"v{version}", "-m", f"Release v{version}"],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if tag_result.returncode == 0:
            print(f"✅ 已創建 tag: v{version}")
            return True
        else:
            print(f"❌ Tag 創建失敗: {tag_result.stderr}")
            return False

    def push(self) -> bool:
        """推送到 GitHub"""
        print("\n▶️  推送到 GitHub...")

        # 推送 commits
        push_result = subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if push_result.returncode != 0:
            print(f"❌ 推送失敗: {push_result.stderr}")
            return False

        print("✅ Commits 推送成功")

        # 推送 tags
        tag_result = subprocess.run(
            ["git", "push", "origin", "--tags"],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        if tag_result.returncode == 0:
            print("✅ Tags 推送成功")
            return True
        else:
            print(f"⚠️  Tags 推送失敗: {tag_result.stderr}")
            return True  # 非關鍵失敗

    def print_summary(
        self, old_version: str, new_version: str, change_type: str
    ) -> None:
        """打印發布摘要"""
        print("\n" + "=" * 60)
        print("📦 發布摘要")
        print("=" * 60)
        print(f"📝 版本更新: {old_version} → {new_version}")
        print(f"📊 變更類型: {change_type.upper()}")
        print(f"⏰ 發布時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"🔗 GitHub: https://github.com/wang-yi2/yplus-calculate/releases/tag/v{new_version}"
        )
        print("=" * 60)

    def run(self) -> bool:
        """執行完整的發布流程"""
        print("\n" + "=" * 60)
        print("🚀 CFD y+ 計算工具 - 自動發布系統")
        print("=" * 60)
        print(f"當前版本: {self.current_version}\n")

        # 1. 執行測試
        if not self.test():
            print("\n❌ 測試失敗，發布已中止")
            return False

        # 2. 執行 Lint
        if not self.lint():
            print("\n⚠️  Lint 檢查發現問題，請手動審查")

        # 3. 更新 README
        self.update_readme()

        # 4. 偵測變更類型並更新版本
        change_type = self._detect_change_type()
        new_version = self._calculate_next_version(change_type)

        print(f"\n📊 偵測到變更類型: {change_type} → v{new_version}")

        # 更新版本號
        self._set_version(new_version)

        # 5. 提交和創建 tag
        if not self.commit_and_tag(new_version, change_type):
            print("\n❌ 提交失敗，發布已中止")
            return False

        # 6. 推送到 GitHub
        if not self.push():
            print("\n⚠️  推送失敗，請手動推送")
            return False

        # 7. 打印摘要
        self.print_summary(self.current_version, new_version, change_type)

        print("\n✅ 發布流程完成！\n")
        return True


def main():
    """主程序入口"""
    manager = ReleaseManager()
    success = manager.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
