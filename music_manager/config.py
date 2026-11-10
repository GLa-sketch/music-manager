"""项目配置。

集中管理路径、数据库位置等配置项。
后续阶段会逐步用到。
"""
from pathlib import Path

# 项目根目录（main.py 所在位置）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 数据库文件路径（Phase 2 启用）
DB_PATH = PROJECT_ROOT / "music_manager.db"

# 音乐库根目录（用户自己指定，Phase 3 启用）
# 示例：MUSIC_LIBRARY_DIR = Path("D:/Music")
MUSIC_LIBRARY_DIR: Path | None = None
