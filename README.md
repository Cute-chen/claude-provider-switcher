# Claude Code 提供商切换工具

一个 macOS GUI 应用程序，用于管理和切换 Claude Code CLI 工具的不同 API 提供商。

## 项目概述

本应用程序提供了一个用户友好的界面，可以轻松在 Claude Code 的不同 API 提供商之间切换，包括第三方 Claude API 提供商和 DeepSeek。它会自动管理您的 shell 配置文件，并提供完善的备份机制。

## 主要功能

- **提供商管理**：配置和切换多个 API 提供商
- **安全配置**：安全存储 API 密钥和提供商设置
- **自动备份**：在修改前自动备份您的 `.zshrc` 文件
- **现代界面**：简洁的 iOS 风格界面，支持标签页导航
- **状态监控**：实时显示当前激活的提供商
- **多种构建方式**：支持 py2app 和 PyInstaller 构建

## 支持的提供商

### 第三方 Claude API
- 可自定义的基础 URL 和 API 密钥
- 灵活的配置，支持任何 Claude 兼容的 API 提供商

### DeepSeek
- 预配置的 DeepSeek API 端点
- 优化的环境变量配置
- 自动模型配置

## 安装方法

### 方法一：直接运行
```bash
# 克隆仓库
git clone <仓库地址>
cd "claude code模型商切换"

# 运行应用程序
./run.sh
```

### 方法二：构建 macOS 应用程序包
```bash
# 使用 py2app 构建
./build.sh

# 应用程序将创建在 dist/Claude Provider Switcher.app
```

### 方法三：使用 PyInstaller 构建
```bash
# 使用 PyInstaller 构建
./build_pyinstaller.sh
```

## 使用说明

1. **启动应用程序**：使用上述任一安装方法运行应用程序

2. **配置提供商**：
   - 前往"第三方 Claude"标签页配置第三方提供商设置
   - 前往"DeepSeek"标签页配置 DeepSeek API 密钥
   - 点击"保存配置"保存您的设置

3. **切换提供商**：
   - 点击"切换到此提供商"切换到您想要的提供商
   - 应用程序会自动更新您的 `.zshrc` 文件

4. **应用更改**：
   - 切换后，重启终端或运行：
   ```bash
   source ~/.zshrc
   ```

## 配置文件

应用程序将配置存储在 `~/.claude_provider_config.json`：

```json
{
  "third_party": {
    "base_url": "https://api.aicodemirror.com/api/claudecode",
    "api_key": "您的-api-密钥"
  },
  "deepseek": {
    "api_key": "您的-deepseek-api-密钥"
  }
}
```

## 文件结构

```
├── claude_switcher_app.py     # 主要现代 UI 应用程序
├── claude_provider_switcher.py # 高级 UI，包含 JSON 编辑器
├── setup.py                   # py2app 配置文件
├── build.sh                   # py2app 构建脚本
├── build_pyinstaller.sh       # PyInstaller 构建脚本
├── run.sh                     # 直接运行脚本
├── build/                     # 构建产物
└── dist/                      # 分发目录
```

## 系统要求

- **Python 3**（macOS 自带）
- **Tkinter**（macOS Python 自带）
- **zsh shell**（现代 macOS 默认）

### 构建依赖
- **py2app**（用于构建 macOS 应用程序包）
- **PyInstaller**（用于构建独立可执行文件）

## 安全性

- **无网络访问**：应用程序不会进行任何网络请求
- **本地存储**：所有配置都存储在您的本地主目录中
- **备份保护**：在修改前自动备份 `.zshrc`
- **安全输入**：UI 中 API 密钥会被屏蔽显示

## 技术细节

### 工作原理
1. 读取并修改您的 `~/.zshrc` 文件
2. 为 Claude Code 环境变量创建专用区域
3. 在更改前自动备份您的 `.zshrc`
4. 将提供商配置存储在 `~/.claude_provider_config.json`

### 管理的环境变量
- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_API_KEY`
- `DEEPSEEK_API_KEY`
- `ANTHROPIC_AUTH_TOKEN`
- `ANTHROPIC_MODEL`
- 以及其他 Claude Code 特定变量

## 故障排除

### 常见问题

**"无法读取 .zshrc 文件"**
- 确保您的主目录中有 `.zshrc` 文件
- 检查文件权限

**更改未生效**
- 切换提供商后记得运行 `source ~/.zshrc`
- 重启终端应用程序

**应用程序无法启动**
- 确保 Python 3 已安装：`python3 --version`
- 检查 Tkinter 是否可用：`python3 -m tkinter`

### 备份文件
备份文件存储在 `~/.claude_provider_backups/` 目录中，包含时间戳：
```
~/.claude_provider_backups/zshrc_backup_20250101_120000
```

## 贡献

欢迎贡献！请随时提交 pull request 或为 bug 和功能请求开启 issue。

## 许可证

本项目是开源的。详情请参阅 LICENSE 文件。

## 免责声明

此工具旨在帮助管理 Claude Code API 提供商配置。它会修改您的 shell 配置文件，因此在使用前请查看代码并了解其功能。始终确保您有重要配置文件的适当备份。

---

**注意**：此应用程序专门为使用 zsh shell 的 macOS 用户设计。在其他操作系统或使用不同 shell 时可能无法正常工作。