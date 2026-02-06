# -*- coding: utf-8 -*-
"""
CFD y+ Calculator - Test Suite
"""

import pytest


class TestCFDCalculator:
    """基本測試類"""

    def test_import_main(self):
        """測試主模組導入"""
        try:
            from main import CFDYPlusCalculator
            assert CFDYPlusCalculator is not None
        except ImportError:
            pytest.skip("PySide6 not available in test environment")

    def test_utf8_support(self):
        """測試 UTF-8 編碼支援"""
        # 驗證中文字符
        test_string = "CFD y+ 計算工具"
        assert "計算" in test_string
        assert len(test_string) == 9

    def test_encoding_declaration(self):
        """測試檔案編碼聲明"""
        with open("main.py", encoding="utf-8") as f:
            first_line = f.readline()
            assert "coding: utf-8" in first_line
