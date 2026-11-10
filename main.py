"""Music Manager 入口文件。

运行方式：
    python main.py

后续 Phase 4 完成后，可通过 CLI 直接调用：
    python -m music_manager.cli
"""
from music_manager import __version__


def main():
    print(f"Music Manager v{__version__}")
    print("=" * 40)
    print("项目骨架已就绪。")
    print("下一步：完成 Phase 1 的 Git 初始化与首次提交。")
    print("详见 docs/roadmap.md")


if __name__ == "__main__":
    main()
