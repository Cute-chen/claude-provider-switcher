#!/bin/bash

# Claude Provider Switcher - 构建脚本（使用 tkinter）

echo "==================================="
echo "Claude Provider Switcher 构建工具"
echo "==================================="
echo ""

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3"
    exit 1
fi

echo "✓ 找到 Python 3: $(python3 --version)"
echo ""

# 检查 py2app
echo "📦 检查依赖..."
if ! python3 -c "import py2app" 2>/dev/null; then
    echo "安装 py2app..."
    pip3 install py2app

    if [ $? -ne 0 ]; then
        echo "❌ py2app 安装失败"
        exit 1
    fi
fi

echo "✓ 依赖检查完成"
echo ""

# 清理旧的构建
echo "🧹 清理旧构建..."
rm -rf build dist

# 构建 .app
echo "🔨 构建 macOS 应用..."
python3 setup.py py2app

if [ $? -ne 0 ]; then
    echo "❌ 构建失败"
    exit 1
fi

echo ""
echo "✅ 构建完成!"
echo ""
echo "应用位置: $(pwd)/dist/Claude Provider Switcher.app"
echo ""
echo "使用方法:"
echo "1. 打开 dist 文件夹"
echo "2. 将 'Claude Provider Switcher.app' 拖到应用程序文件夹"
echo "3. 双击运行"
echo ""
echo "或直接运行:"
echo "  open 'dist/Claude Provider Switcher.app'"
echo ""
