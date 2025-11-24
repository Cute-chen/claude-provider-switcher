#!/usr/bin/env python3
"""
Claude Code Provider Switcher
在 DeepSeek 和第三方 Claude 中转站之间切换
"""

import os
import sys
import json
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# 配置文件路径
ZSHRC_PATH = os.path.expanduser("~/.zshrc")
CONFIG_PATH = os.path.expanduser("~/.claude_provider_config.json")
BACKUP_DIR = os.path.expanduser("~/.claude_provider_backups")

# 默认配置
DEFAULT_CONFIG = {
    "third_party": {
        "name": "第三方 Claude 中转站",
        "env_vars": {
            "ANTHROPIC_BASE_URL": "https://api.aicodemirror.com/api/claudecode",
            "ANTHROPIC_API_KEY": "sk-ant-api03-your-key-here"
        }
    },
    "deepseek": {
        "name": "DeepSeek",
        "env_vars": {
            "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
            "ANTHROPIC_AUTH_TOKEN": "${DEEPSEEK_API_KEY}",
            "API_TIMEOUT_MS": "600000",
            "ANTHROPIC_MODEL": "deepseek-chat",
            "ANTHROPIC_SMALL_FAST_MODEL": "deepseek-chat",
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
        }
    }
}


class ProviderSwitcher:
    def __init__(self):
        self.ensure_backup_dir()
        self.config = self.load_config()

    def ensure_backup_dir(self):
        """确保备份目录存在"""
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

    def load_config(self):
        """加载配置文件"""
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        """保存配置文件"""
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def backup_zshrc(self):
        """备份 .zshrc 文件"""
        if not os.path.exists(ZSHRC_PATH):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"zshrc_backup_{timestamp}")

        try:
            shutil.copy2(ZSHRC_PATH, backup_path)
            return backup_path
        except Exception as e:
            print(f"备份失败: {e}")
            return None

    def read_zshrc(self):
        """读取 .zshrc 文件内容"""
        if not os.path.exists(ZSHRC_PATH):
            return ""

        try:
            with open(ZSHRC_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取 .zshrc 失败: {e}")
            return None

    def remove_claude_env_section(self, content):
        """移除现有的 Claude Code 环境变量部分"""
        lines = content.split('\n')
        result = []
        in_claude_section = False

        for line in lines:
            if '# Claude Code Environment Variables' in line:
                in_claude_section = True
                continue
            elif '# End Claude Code Environment Variables' in line:
                in_claude_section = False
                continue
            elif not in_claude_section:
                result.append(line)

        # 移除末尾多余的空行
        while result and not result[-1].strip():
            result.pop()

        return '\n'.join(result)

    def generate_env_section(self, provider_key):
        """生成环境变量配置段"""
        if provider_key not in self.config:
            return None

        provider = self.config[provider_key]
        lines = ["", "# Claude Code Environment Variables"]

        for key, value in provider['env_vars'].items():
            lines.append(f"export {key}={value}")

        lines.append("# End Claude Code Environment Variables")
        lines.append("")

        return '\n'.join(lines)

    def switch_provider(self, provider_key):
        """切换提供商"""
        # 备份
        backup_path = self.backup_zshrc()
        if backup_path:
            print(f"已备份 .zshrc 到: {backup_path}")

        # 读取现有内容
        content = self.read_zshrc()
        if content is None:
            return False, "无法读取 .zshrc 文件"

        # 移除旧的 Claude Code 配置
        content = self.remove_claude_env_section(content)

        # 添加新的配置
        new_section = self.generate_env_section(provider_key)
        if new_section is None:
            return False, f"未知的提供商: {provider_key}"

        new_content = content + new_section

        # 写入文件
        try:
            with open(ZSHRC_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, f"已切换到 {self.config[provider_key]['name']}"
        except Exception as e:
            return False, f"写入 .zshrc 失败: {e}"

    def get_current_provider(self):
        """检测当前使用的提供商"""
        content = self.read_zshrc()
        if not content:
            return "未配置"

        if "api.deepseek.com" in content:
            return "deepseek"
        elif "ANTHROPIC_BASE_URL" in content:
            return "third_party"

        return "未知"


class ProviderSwitcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Claude Code 提供商切换工具")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        self.switcher = ProviderSwitcher()

        self.create_widgets()
        self.update_current_status()

    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 配置根窗口的网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # 标题
        title_label = ttk.Label(main_frame, text="Claude Code 提供商切换",
                               font=('Helvetica', 16, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # 当前状态
        status_frame = ttk.LabelFrame(main_frame, text="当前状态", padding="10")
        status_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        status_frame.columnconfigure(1, weight=1)

        ttk.Label(status_frame, text="当前提供商:").grid(row=0, column=0, sticky=tk.W)
        self.current_provider_label = ttk.Label(status_frame, text="检测中...",
                                               font=('Helvetica', 11, 'bold'))
        self.current_provider_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        # 切换按钮区域
        switch_frame = ttk.LabelFrame(main_frame, text="切换提供商", padding="10")
        switch_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        ttk.Button(switch_frame, text="切换到第三方 Claude 中转站",
                  command=lambda: self.switch_to('third_party'),
                  width=30).grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(switch_frame, text="切换到 DeepSeek",
                  command=lambda: self.switch_to('deepseek'),
                  width=30).grid(row=0, column=1, padx=5, pady=5)

        # 配置编辑区域
        config_frame = ttk.LabelFrame(main_frame, text="配置管理", padding="10")
        config_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        main_frame.rowconfigure(3, weight=1)
        config_frame.columnconfigure(0, weight=1)
        config_frame.rowconfigure(0, weight=1)

        # 配置编辑器
        self.config_text = scrolledtext.ScrolledText(config_frame, height=15, width=70)
        self.config_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 加载配置到文本框
        self.load_config_to_text()

        # 配置按钮
        config_btn_frame = ttk.Frame(config_frame)
        config_btn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Button(config_btn_frame, text="保存配置",
                  command=self.save_config_from_text).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_btn_frame, text="重置为默认",
                  command=self.reset_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(config_btn_frame, text="刷新状态",
                  command=self.update_current_status).pack(side=tk.LEFT, padx=5)

    def load_config_to_text(self):
        """加载配置到文本框"""
        self.config_text.delete('1.0', tk.END)
        config_str = json.dumps(self.switcher.config, indent=2, ensure_ascii=False)
        self.config_text.insert('1.0', config_str)

    def save_config_from_text(self):
        """从文本框保存配置"""
        try:
            config_str = self.config_text.get('1.0', tk.END)
            new_config = json.loads(config_str)
            self.switcher.config = new_config
            if self.switcher.save_config():
                messagebox.showinfo("成功", "配置已保存")
            else:
                messagebox.showerror("错误", "配置保存失败")
        except json.JSONDecodeError as e:
            messagebox.showerror("错误", f"JSON 格式错误: {e}")

    def reset_config(self):
        """重置配置为默认值"""
        if messagebox.askyesno("确认", "确定要重置为默认配置吗？"):
            self.switcher.config = DEFAULT_CONFIG.copy()
            self.switcher.save_config()
            self.load_config_to_text()
            messagebox.showinfo("成功", "配置已重置为默认值")

    def update_current_status(self):
        """更新当前状态显示"""
        current = self.switcher.get_current_provider()
        if current == "third_party":
            status_text = "第三方 Claude 中转站"
            color = "blue"
        elif current == "deepseek":
            status_text = "DeepSeek"
            color = "green"
        else:
            status_text = current
            color = "red"

        self.current_provider_label.config(text=status_text, foreground=color)

    def switch_to(self, provider_key):
        """切换到指定提供商"""
        success, message = self.switcher.switch_provider(provider_key)

        if success:
            messagebox.showinfo("成功", f"{message}\n\n请重启终端或运行 'source ~/.zshrc' 使配置生效")
            self.update_current_status()
        else:
            messagebox.showerror("错误", message)


def main():
    """主函数"""
    root = tk.Tk()
    app = ProviderSwitcherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
