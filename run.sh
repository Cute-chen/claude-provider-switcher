#!/bin/bash

# 直接运行应用（使用 macOS 自带的 Python 和 tkinter）

cd "$(dirname "$0")"

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    exit 1
fi

# 运行应用（tkinter 是 macOS 自带的，无需安装）
python3 claude_switcher_app.py
