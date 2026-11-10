"""音乐元数据扫描（Phase 3 填充）。

使用 mutagen 读取 mp3/flac/m4a 等文件的元数据（标题、艺术家、专辑、时长），
扫描指定文件夹并把歌曲信息写入数据库。

需要处理的难点：
- 中文标签编码（GBK / UTF-8 混杂）
- 缺失字段的默认值
- 重复文件检测

目前为占位，等待 Phase 3 实现。
"""

# TODO Phase 3:
# from pathlib import Path
# from mutagen import File as MutagenFile
#
# SUPPORTED_EXTS = {".mp3", ".flac", ".m4a", ".ogg", ".wav"}
#
# def read_metadata(file_path: Path) -> dict:
#     """读取单个文件的元数据。"""
#     ...
#
# def scan_directory(library_dir: Path) -> list[dict]:
#     """递归扫描目录，返回所有支持格式的元数据列表。"""
#     ...
