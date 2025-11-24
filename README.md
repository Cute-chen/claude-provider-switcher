# Claude Code Provider Switcher

A macOS GUI application for managing and switching between different API providers for Claude Code CLI tool.

## Overview

This application provides a user-friendly interface to easily switch between different API providers for Claude Code, including third-party Claude API providers and DeepSeek. It automatically manages your shell configuration files with proper backup mechanisms.

## Features

- **Provider Management**: Configure and switch between multiple API providers
- **Secure Configuration**: Safely store API keys and provider settings
- **Automatic Backup**: Creates backups of your `.zshrc` file before any modifications
- **Modern UI**: Clean, iOS-inspired interface with tabbed navigation
- **Status Monitoring**: Real-time display of current active provider
- **Multiple Build Options**: Support for py2app and PyInstaller builds

## Supported Providers

### Third-party Claude API
- Customizable base URL and API key
- Flexible configuration for any Claude-compatible API provider

### DeepSeek
- Pre-configured DeepSeek API endpoint
- Optimized environment variables for DeepSeek integration
- Automatic model configuration

## Installation

### Method 1: Direct Execution
```bash
# Clone the repository
git clone <repository-url>
cd "claude code模型商切换"

# Run the application
./run.sh
```

### Method 2: Build macOS Application Bundle
```bash
# Build using py2app
./build.sh

# The application will be created in dist/Claude Provider Switcher.app
```

### Method 3: Build with PyInstaller
```bash
# Build using PyInstaller
./build_pyinstaller.sh
```

## Usage

1. **Launch the Application**: Run the application using any of the installation methods above

2. **Configure Providers**:
   - Go to the "第三方 Claude" tab to configure third-party provider settings
   - Go to the "DeepSeek" tab to configure DeepSeek API key
   - Click "保存配置" to save your settings

3. **Switch Providers**:
   - Click "切换到此提供商" to switch to your desired provider
   - The application will automatically update your `.zshrc` file

4. **Apply Changes**:
   - After switching, restart your terminal or run:
   ```bash
   source ~/.zshrc
   ```

## Configuration

The application stores configuration in `~/.claude_provider_config.json`:

```json
{
  "third_party": {
    "base_url": "https://api.aicodemirror.com/api/claudecode",
    "api_key": "your-api-key-here"
  },
  "deepseek": {
    "api_key": "your-deepseek-api-key-here"
  }
}
```

## File Structure

```
├── claude_switcher_app.py     # Main modern UI application
├── claude_provider_switcher.py # Advanced UI with JSON editor
├── setup.py                   # py2app configuration
├── build.sh                   # Build script for py2app
├── build_pyinstaller.sh       # Build script for PyInstaller
├── run.sh                     # Direct execution script
├── build/                     # Build artifacts
└── dist/                      # Distribution directory
```

## Requirements

- **Python 3** (included with macOS)
- **Tkinter** (included with macOS Python)
- **zsh shell** (default on modern macOS)

### Build Dependencies
- **py2app** (for macOS app bundle)
- **PyInstaller** (for standalone executable)

## Security

- **No Network Access**: The application does not make any network requests
- **Local Storage Only**: All configuration is stored locally in your home directory
- **Backup Protection**: Automatic backups of `.zshrc` before any modifications
- **Secure Input**: API keys are masked in the UI

## Technical Details

### How It Works
1. Reads and modifies your `~/.zshrc` file
2. Creates a dedicated section for Claude Code environment variables
3. Automatically backs up your `.zshrc` before making changes
4. Stores provider configurations in `~/.claude_provider_config.json`

### Environment Variables Managed
- `ANTHROPIC_BASE_URL`
- `ANTHROPIC_API_KEY`
- `DEEPSEEK_API_KEY`
- `ANTHROPIC_AUTH_TOKEN`
- `ANTHROPIC_MODEL`
- And other Claude Code specific variables

## Troubleshooting

### Common Issues

**"无法读取 .zshrc 文件" (Cannot read .zshrc file)**
- Ensure you have a `.zshrc` file in your home directory
- Check file permissions

**Changes not taking effect**
- Remember to run `source ~/.zshrc` after switching providers
- Restart your terminal application

**Application won't start**
- Ensure Python 3 is installed: `python3 --version`
- Check that Tkinter is available: `python3 -m tkinter`

### Backup Files
Backup files are stored in `~/.claude_provider_backups/` with timestamps:
```
~/.claude_provider_backups/zshrc_backup_20250101_120000
```

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source. See the LICENSE file for details.

## Disclaimer

This tool is designed to help manage Claude Code API provider configurations. It modifies your shell configuration files, so please review the code and understand what it does before using it. Always ensure you have proper backups of important configuration files.

---

**Note**: This application is specifically designed for macOS users with zsh shell. It may not work properly on other operating systems or with different shells.