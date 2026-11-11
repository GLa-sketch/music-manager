"""数据库演示脚本。

跑通这个脚本，验证 Phase 2 数据层工作正常：
1. 建表（init_db）
2. 插入测试数据（周杰伦 / 范特西 / 简单爱）
3. 查询并展示
4. 演示多对多（创建歌单，加入歌曲）

运行方式：
    python scripts/demo_db.py
"""
import sys
from pathlib import Path

# 把项目根目录加入搜索路径，确保能导入 music_manager 包
# （因为本脚本在 scripts/ 子目录，直接运行时 Python 找不到上层包）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from music_manager.database import init_db, get_session
from music_manager.models import Artist, Album, Song, Playlist


def main():
    print("=" * 50)
    print("Phase 2 数据层演示")
    print("=" * 50)

    # 第 1 步：建表
    print("\n[1] 初始化数据库（建表）...")
    init_db()
    print("    OK 5 张表已创建: artists / albums / songs / playlists / playlist_song")

    # 第 2 步：插入测试数据
    print("\n[2] 插入测试数据...")
    session = get_session()

    existing = session.query(Song).first()
    if existing:
        print("    数据库已有数据，跳过插入。")
    else:
        # 创建艺术家
        artist = Artist(name="周杰伦", country="中国")
        # 创建专辑，关联到艺术家
        album = Album(title="范特西", artist=artist, year=2001)
        # 创建两首歌，关联到艺术家和专辑
        song1 = Song(
            title="简单爱", artist=artist, album=album,
            duration=269, file_path="D:/Music/简单爱.mp3",
            genre="流行", track_no=2,
        )
        song2 = Song(
            title="双截棍", artist=artist, album=album,
            duration=268, file_path="D:/Music/双截棍.mp3",
            genre="流行", track_no=10,
        )
        # 创建歌单，把两首歌加进去（多对多）
        playlist = Playlist(name="我的最爱", description="循环播放")
        playlist.songs = [song1, song2]

        # 一次性添加所有对象（关联会自动处理）
        session.add_all([artist, album, song1, song2, playlist])
        session.commit()
        print(f"    OK 插入: 艺术家「{artist.name}」/ 专辑「{album.title}」/ 2 首歌 / 1 个歌单")

    # 第 3 步：查询展示
    print("\n[3] 查询数据库...")

    artists = session.query(Artist).all()
    print(f"\n    艺术家（{len(artists)}）:")
    for a in artists:
        print(f"      - {a.name} ({a.country or '未知'})")

    songs = session.query(Song).all()
    print(f"\n    歌曲（{len(songs)}）:")
    for s in songs:
        artist_name = s.artist.name if s.artist else "未知"
        album_title = s.album.title if s.album else "无专辑"
        duration_str = f"{s.duration // 60}:{s.duration % 60:02d}" if s.duration else "?"
        print(f"      - {s.title} | {artist_name} | {album_title} | {duration_str}")

    playlists = session.query(Playlist).all()
    print(f"\n    歌单（{len(playlists)}）:")
    for p in playlists:
        song_titles = [s.title for s in p.songs]
        print(f"      - {p.name}（{len(p.songs)} 首）: {', '.join(song_titles)}")

    session.close()

    print("\n" + "=" * 50)
    print("Phase 2 数据层演示完成！")
    print("数据库文件: music_manager.db")
    print("=" * 50)


if __name__ == "__main__":
    main()
