"""音乐文件元数据扫描。

使用 mutagen 读取 mp3/flac/m4a 等文件的元数据（标题、艺术家、专辑、时长），
扫描指定文件夹，把歌曲信息导入数据库。

三个核心函数：
- read_metadata(file_path): 读取单个文件的元数据
- scan_directory(dir_path): 递归扫描目录，返回所有音乐文件的元数据
- import_to_database(session, dir_path): 扫描 + 导入数据库

为什么用 mutagen？
- 它是 Python 读取音频元数据的标准库
- 支持 mp3/flac/m4a/ogg/wav 等格式
- 自动处理大部分中文编码问题
"""
from pathlib import Path

from mutagen import File as MutagenFile

from music_manager import crud

# 支持的音乐文件扩展名
SUPPORTED_EXTS = {".mp3", ".flac", ".m4a", ".ogg", ".wav", ".wma"}


def read_metadata(file_path):
    """读取单个音乐文件的元数据。

    返回字典：{title, artist, album, duration, bitrate, track_no, file_path}
    缺失的字段为 None。如果文件不存在或不是音频，返回 None。

    不同格式的标签键名不同：
    - mp3 (ID3): TIT2/TPE1/TALB/TRCK
    - flac/m4a/ogg: title/artist/album/tracknumber
    get() 函数自动兼容两种。
    """
    path = Path(file_path)
    if not path.exists():
        return None

    audio = MutagenFile(path)
    if audio is None:  # 不是支持的音频格式
        return None

    tags = audio.tags or {}

    def get(*keys):
        """从多个可能的标签键里取第一个值。兼容 ID3 和 VComment。"""
        for key in keys:
            if key in tags:
                val = tags[key]
                # ID3 frame 有 text 属性（列表）
                if hasattr(val, "text") and val.text:
                    return str(val.text[0])
                # VComment 等直接是列表
                if isinstance(val, list) and val:
                    return str(val[0])
                return str(val)
        return None

    metadata = {
        "file_path": str(path.resolve()),
        "title": get("title", "TIT2", "TITLE") or path.stem,  # 没标题用文件名
        "artist": get("artist", "TPE1", "ARTIST"),
        "album": get("album", "TALB", "ALBUM"),
        "duration": int(audio.info.length) if audio.info else None,
        "bitrate": (
            int(audio.info.bitrate / 1000)
            if audio.info and hasattr(audio.info, "bitrate") and audio.info.bitrate
            else None
        ),
        "track_no": _parse_track(get("tracknumber", "TRCK", "TRACKNUMBER")),
    }
    return metadata


def _parse_track(track_str):
    """解析音轨号。可能是 '3' 或 '3/12' 格式，取前面的数字。"""
    if not track_str:
        return None
    try:
        return int(str(track_str).split("/")[0])
    except (ValueError, IndexError):
        return None


def scan_directory(dir_path):
    """递归扫描目录，返回所有音乐文件的元数据列表。

    用法：
        metas = scan_directory("D:/Music")
        for m in metas:
            print(m["title"], m["artist"])
    """
    root = Path(dir_path)
    if not root.is_dir():
        return []

    results = []
    for path in root.rglob("*"):  # rglob 递归遍历所有子目录
        if path.suffix.lower() in SUPPORTED_EXTS:
            meta = read_metadata(path)
            if meta:
                results.append(meta)
    return results


def import_to_database(session, dir_path):
    """扫描目录并把所有音乐导入数据库。

    按 file_path 去重：已存在的文件会跳过，不会重复导入。
    返回新增的歌曲数量。
    """
    from music_manager.models import Song

    metas = scan_directory(dir_path)
    count = 0
    for meta in metas:
        # 按文件路径判断是否已入库
        existing = session.query(Song).filter_by(file_path=meta["file_path"]).first()
        if existing:
            continue

        crud.add_song(
            session,
            title=meta["title"],
            artist_name=meta["artist"] or "未知艺术家",
            duration=meta["duration"],
            file_path=meta["file_path"],
            album_title=meta["album"],
            track_no=meta["track_no"],
        )
        count += 1
    session.commit()
    return count
