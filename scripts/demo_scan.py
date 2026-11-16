"""音乐文件扫描演示。

扫描你指定的音乐文件夹，读取元数据，导入数据库。

用法：
    python scripts/demo_scan.py "你的音乐文件夹路径"

例如：
    python scripts/demo_scan.py "C:/Users/18496/Music"
    python scripts/demo_scan.py "D:/Music"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from music_manager.database import init_db, get_session
from music_manager.metadata_scanner import scan_directory, import_to_database


def main():
    if len(sys.argv) < 2:
        print("用法：python scripts/demo_scan.py <音乐文件夹路径>")
        print("例如：python scripts/demo_scan.py D:/Music")
        sys.exit(1)

    music_dir = sys.argv[1]

    print("=" * 50)
    print("Phase 3 · 音乐文件扫描演示")
    print("=" * 50)

    # 第 1 步：扫描，看看有什么
    print(f"\n[1] 扫描目录: {music_dir}")
    metas = scan_directory(music_dir)
    print(f"    找到 {len(metas)} 个音乐文件")

    if not metas:
        print("\n没找到音乐文件。可能的原因：")
        print("  - 路径不对（检查文件夹是否存在）")
        print("  - 文件夹里没有 mp3/flac/m4a/ogg/wav 文件")
        print("  - 文件在子目录里（本脚本会递归扫描，应该能找到）")
        return

    # 展示前 5 个文件的元数据
    print(f"\n[2] 前 {min(5, len(metas))} 个文件的元数据：")
    for i, m in enumerate(metas[:5], 1):
        duration_str = f"{m['duration'] // 60}:{m['duration'] % 60:02d}" if m["duration"] else "?"
        print(f"    {i}. {m['title']}")
        print(f"       艺术家: {m['artist'] or '未知'}")
        print(f"       专辑: {m['album'] or '无'}")
        print(f"       时长: {duration_str}")

    # 第 3 步：导入数据库
    print("\n[3] 导入数据库...")
    init_db()
    session = get_session()
    count = import_to_database(session, music_dir)
    print(f"    新增 {count} 首（已存在的跳过）")
    session.close()

    print("\n" + "=" * 50)
    print("扫描演示完成！用 DB Browser 或 SQLite Viewer 打开")
    print("music_manager.db，能看到新导入的歌曲。")
    print("=" * 50)


if __name__ == "__main__":
    main()
