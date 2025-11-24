#!/bin/bash

# Claude Provider Switcher 构建工具 (使用 PyInstaller)

set -e

echo "==================================="
echo "Claude Provider Switcher 构建工具"
echo "==================================="
echo ""

# 检查 Python
PYTHON_CMD=$(command -v python3)
if [ -z "$PYTHON_CMD" ]; then
    echo "❌ 未找到 Python 3"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo "✓ 找到 Python 3: $PYTHON_VERSION"
echo ""

# 检查依赖
echo "📦 检查依赖..."
$PYTHON_CMD -m pip install pyinstaller --user --quiet
echo "✓ 依赖检查完成"
echo ""

# 清理旧构建
echo "🧹 清理旧构建..."
rm -rf build dist
echo ""

# 构建应用
echo "🔨 构建 macOS 应用..."
$PYTHON_CMD -m PyInstaller \
    --name="Claude Provider Switcher" \
    --windowed \
    --onefile \
    --clean \
    --noconfirm \
    claude_switcher_app.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 构建成功!"
    echo "应用程序位于: dist/Claude Provider Switcher.app"
    echo ""

    # 显示应用信息
    if [ -d "dist/Claude Provider Switcher.app" ]; then
        SIZE=$(du -sh "dist/Claude Provider Switcher.app" | cut -f1)
        echo "应用大小: $SIZE"
    fi
else
    echo ""
    echo "❌ 构建失败"
    exit 1
fi
