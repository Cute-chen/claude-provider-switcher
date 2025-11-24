"""
Setup script for building macOS .app bundle (使用 tkinter)
"""
from setuptools import setup

APP = ['claude_switcher_app.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': [],
    'iconfile': None,
    'excludes': ['setuptools._vendor', 'setuptools.extern'],
    'plist': {
        'CFBundleName': 'Claude Provider Switcher',
        'CFBundleDisplayName': 'Claude Provider Switcher',
        'CFBundleGetInfoString': "切换 Claude Code 提供商",
        'CFBundleIdentifier': "com.claude.providerswitcher",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "Copyright © 2025"
    }
}

setup(
    app=APP,
    name='Claude Provider Switcher',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
