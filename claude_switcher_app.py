#!/usr/bin/env python3
"""
Claude Code Provider Switcher - Modern UI
"""

import os
import sys
import json
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

# 配置文件路径
ZSHRC_PATH = os.path.expanduser("~/.zshrc")
CONFIG_PATH = os.path.expanduser("~/.claude_provider_config.json")
BACKUP_DIR = os.path.expanduser("~/.claude_provider_backups")


class ProviderSwitcher:
    """提供商切换核心逻辑"""

    def __init__(self):
        self.ensure_backup_dir()
        self.config = self.load_config()

    def ensure_backup_dir(self):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)

    def load_config(self):
        default_config = {
            "third_party": {
                "base_url": "https://api.aicodemirror.com/api/claudecode",
                "api_key": ""
            },
            "deepseek": {
                "api_key": ""
            }
        }

        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    for provider in default_config:
                        if provider not in loaded:
                            loaded[provider] = default_config[provider]
                        else:
                            for key in default_config[provider]:
                                if key not in loaded[provider]:
                                    loaded[provider][key] = default_config[provider][key]
                    return loaded
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                return default_config
        return default_config

    def save_config(self):
        try:
            with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def backup_zshrc(self):
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
        if not os.path.exists(ZSHRC_PATH):
            return ""
        try:
            with open(ZSHRC_PATH, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"读取 .zshrc 失败: {e}")
            return None

    def remove_claude_env_section(self, content):
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
        while result and not result[-1].strip():
            result.pop()
        return '\n'.join(result)

    def switch_to_third_party(self):
        if not self.config['third_party']['api_key']:
            return False, "请先配置第三方 API Key"
        backup_path = self.backup_zshrc()
        content = self.read_zshrc()
        if content is None:
            return False, "无法读取 .zshrc 文件"
        content = self.remove_claude_env_section(content)
        new_section = f"""
# Claude Code Environment Variables
export ANTHROPIC_BASE_URL={self.config['third_party']['base_url']}
export ANTHROPIC_API_KEY={self.config['third_party']['api_key']}
# End Claude Code Environment Variables
"""
        new_content = content + new_section
        try:
            with open(ZSHRC_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "已切换到第三方 Claude 中转站"
        except Exception as e:
            return False, f"写入 .zshrc 失败: {e}"

    def switch_to_deepseek(self):
        if not self.config['deepseek']['api_key']:
            return False, "请先配置 DeepSeek API Key"
        backup_path = self.backup_zshrc()
        content = self.read_zshrc()
        if content is None:
            return False, "无法读取 .zshrc 文件"
        content = self.remove_claude_env_section(content)
        new_section = f"""
# Claude Code Environment Variables
export DEEPSEEK_API_KEY={self.config['deepseek']['api_key']}
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=${{DEEPSEEK_API_KEY}}
export API_TIMEOUT_MS=600000
export ANTHROPIC_MODEL=deepseek-chat
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-chat
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
# End Claude Code Environment Variables
"""
        new_content = content + new_section
        try:
            with open(ZSHRC_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, "已切换到 DeepSeek"
        except Exception as e:
            return False, f"写入 .zshrc 失败: {e}"

    def get_current_provider(self):
        content = self.read_zshrc()
        if not content:
            return "未配置"
        if "api.deepseek.com" in content or "deepseek-chat" in content:
            return "DeepSeek"
        elif "ANTHROPIC_BASE_URL" in content:
            return "第三方 Claude"
        return "未配置"


class MainWindow:
    """主窗口 - 现代简约风格"""

    def __init__(self, root):
        self.root = root
        self.switcher = ProviderSwitcher()
        self.setup_styles()
        self.init_ui()
        self.load_settings()
        self.update_status()

    def setup_styles(self):
        # 使用 ttk 样式
        self.style = ttk.Style()
        if sys.platform == 'darwin':
            self.style.theme_use('clam')  # 在 macOS 上使用 clam 或 aqua
        
        # 颜色定义
        self.colors = {
            'primary': '#007AFF',    # iOS 蓝
            'success': '#34C759',    # iOS 绿
            'bg': '#F5F5F7',         # 浅灰背景
            'card_bg': '#FFFFFF',
            'text': '#1D1D1F',
            'subtext': '#86868B'
        }

        self.root.configure(bg=self.colors['bg'])
        
        # 配置通用样式
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('Card.TFrame', background=self.colors['card_bg'], relief='flat')
        
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'], font=('Helvetica', 13))
        self.style.configure('Header.TLabel', font=('Helvetica', 24, 'bold'), background=self.colors['bg'])
        self.style.configure('Subheader.TLabel', font=('Helvetica', 13), foreground=self.colors['subtext'], background=self.colors['bg'])
        
        self.style.configure('CardTitle.TLabel', font=('Helvetica', 14, 'bold'), background=self.colors['card_bg'])
        self.style.configure('Card.TLabel', background=self.colors['card_bg'])
        
        self.style.configure('Primary.TButton', font=('Helvetica', 13))
        
        self.style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        self.style.configure('TNotebook.Tab', padding=[12, 8], font=('Helvetica', 13))

    def init_ui(self):
        self.root.title("Claude Code Provider Switcher")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # 主容器，带内边距
        main_container = ttk.Frame(self.root, padding="20 20 20 20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # ===== 头部 =====
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="Provider Switcher", style='Header.TLabel').pack(anchor='w')
        ttk.Label(header_frame, text="管理和切换 Claude Code 的 API 提供商", style='Subheader.TLabel').pack(anchor='w', pady=(5, 0))

        # ===== 状态卡片 =====
        status_frame = tk.Frame(main_container, bg=self.colors['card_bg'], padx=15, pady=15)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        # 给 Frame 加个边框效果 (可选)
        
        status_top = tk.Frame(status_frame, bg=self.colors['card_bg'])
        status_top.pack(fill=tk.X)
        
        tk.Label(status_top, text="当前状态", font=('Helvetica', 12, 'bold'), bg=self.colors['card_bg'], fg=self.colors['subtext']).pack(side=tk.LEFT)
        
        self.status_label = tk.Label(status_frame, text="检测中...", font=('Helvetica', 18, 'bold'), bg=self.colors['card_bg'], fg=self.colors['primary'])
        self.status_label.pack(anchor='w', pady=(5, 0))
        
        # 刷新按钮
        refresh_btn = ttk.Button(status_top, text="刷新", command=self.update_status, width=6)
        refresh_btn.pack(side=tk.RIGHT)

        # ===== 标签页 =====
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- Tab 1: 第三方 Claude ---
        tab1 = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(tab1, text='第三方 Claude')
        
        self._build_input_field(tab1, "Base URL", "third_party_url")
        self._build_input_field(tab1, "API Key", "third_party_key", show="●")
        
        btn_frame1 = ttk.Frame(tab1)
        btn_frame1.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame1, text="保存配置", command=lambda: self.save_settings('third_party')).pack(fill=tk.X, pady=(0, 10))
        ttk.Button(btn_frame1, text="切换到此提供商", command=self.switch_to_third_party).pack(fill=tk.X)

        # --- Tab 2: DeepSeek ---
        tab2 = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(tab2, text='DeepSeek')
        
        self._build_input_field(tab2, "API Key", "deepseek_key", show="●")
        
        info_frame = tk.Frame(tab2, bg='#FFF9E6', padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(15, 0))
        tk.Label(info_frame, text="DeepSeek 自动配置", font=('Helvetica', 12, 'bold'), bg='#FFF9E6', fg='#B78505').pack(anchor='w')
        tk.Label(info_frame, text="Base URL: https://api.deepseek.com/anthropic\nModel: deepseek-chat", justify=tk.LEFT, bg='#FFF9E6', fg='#B78505', font=('Helvetica', 11)).pack(anchor='w', pady=(5, 0))

        btn_frame2 = ttk.Frame(tab2)
        btn_frame2.pack(fill=tk.X, pady=20)
        ttk.Button(btn_frame2, text="保存配置", command=lambda: self.save_settings('deepseek')).pack(fill=tk.X, pady=(0, 10))
        ttk.Button(btn_frame2, text="切换到此提供商", command=self.switch_to_deepseek).pack(fill=tk.X)

        # ===== 底部提示 =====
        footer_label = ttk.Label(main_container, text="提示: 切换后请在终端运行 source ~/.zshrc 生效", font=('Helvetica', 11), foreground=self.colors['subtext'])
        footer_label.pack(side=tk.BOTTOM)

    def _build_input_field(self, parent, label_text, attr_name, show=None):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame, text=label_text, font=('Helvetica', 12, 'bold')).pack(anchor='w', pady=(0, 5))
        
        entry = ttk.Entry(frame, font=('Helvetica', 13))
        if show:
            entry.config(show=show)
        entry.pack(fill=tk.X)
        
        setattr(self, attr_name, entry)

    def load_settings(self):
        self.third_party_url.delete(0, tk.END)
        self.third_party_url.insert(0, self.switcher.config['third_party']['base_url'])
        self.third_party_key.delete(0, tk.END)
        self.third_party_key.insert(0, self.switcher.config['third_party']['api_key'])
        self.deepseek_key.delete(0, tk.END)
        self.deepseek_key.insert(0, self.switcher.config['deepseek']['api_key'])

    def save_settings(self, provider):
        if provider == 'third_party':
            self.switcher.config['third_party']['base_url'] = self.third_party_url.get()
            self.switcher.config['third_party']['api_key'] = self.third_party_key.get()
        elif provider == 'deepseek':
            self.switcher.config['deepseek']['api_key'] = self.deepseek_key.get()

        if self.switcher.save_config():
            messagebox.showinfo("成功", "配置已保存")
        else:
            messagebox.showerror("错误", "配置保存失败")

    def update_status(self):
        current = self.switcher.get_current_provider()
        self.status_label.config(text=current)
        
        if current == "DeepSeek":
            self.status_label.config(fg="#007AFF") # Blue
        elif current == "第三方 Claude":
            self.status_label.config(fg="#AF52DE") # Purple
        else:
            self.status_label.config(fg="#8E8E93") # Gray

    def switch_to_third_party(self):
        success, message = self.switcher.switch_to_third_party()
        if success:
            messagebox.showinfo("成功", f"{message}\n\n请重启终端或运行:\nsource ~/.zshrc")
            self.update_status()
        else:
            messagebox.showerror("错误", message)

    def switch_to_deepseek(self):
        success, message = self.switcher.switch_to_deepseek()
        if success:
            messagebox.showinfo("成功", f"{message}\n\n请重启终端或运行:\nsource ~/.zshrc")
            self.update_status()
        else:
            messagebox.showerror("错误", message)


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()