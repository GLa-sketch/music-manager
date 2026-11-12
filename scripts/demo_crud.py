"""CRUD 操作演示脚本。

演示 crud.py 里的增删改查操作。
每次运行后会清理测试数据，可重复运行。

运行方式：
    python scripts/demo_crud.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from music_manager.database import init_db, get_session
from music_manager import crud


def main():
    print("=" * 50)
    print("Phase 2 · CRUD 操作演示")
    print("=" * 50)

    init_db()
    session = get_session()

    # ===== 查（Read）=====
    print("\n[查] 所有歌曲：")
    songs = crud.list_songs(session)
    for s in songs:
        artist = s.artist.name if s.artist else "未知"
        print(f"    {s.id}: {s.title} - {artist}")

    print("\n[查] 搜索标题含「简单」的歌：")
    results = crud.search_songs(session, "简单")
    for s in results:
        print(f"    找到: {s.title}")

    # ===== 增（Create）=====
    print("\n[增] 添加一首新歌「夜曲」：")
    new_song = crud.add_song(
        session, title="夜曲", artist_name="周杰伦",
        duration=235, file_path="D:/Music/夜曲.mp3", genre="流行",
        album_title="十一月的萧邦",
    )
    session.commit()
    print(f"    添加成功: {new_song.title} (id={new_song.id})")

    print("\n[增] 创建歌单「深夜电台」并加入「夜曲」：")
    playlist = crud.create_playlist(session, "深夜电台", "适合深夜听")
    crud.add_song_to_playlist(session, playlist.id, new_song.id)
    session.commit()
    print(f"    歌单「{playlist.name}」现有: {[s.title for s in playlist.songs]}")

    # ===== 改（Update）=====
    print("\n[改] 把「夜曲」标题改成「夜曲(remix)」：")
    crud.update_song_title(session, new_song.id, "夜曲(remix)")
    session.commit()
    refreshed = crud.get_song(session, new_song.id)
    print(f"    修改后: {refreshed.title}")

    # ===== 删（Delete）=====
    print("\n[删] 删除「夜曲(remix)」和歌单「深夜电台」：")
    crud.delete_song(session, new_song.id)
    crud.delete_playlist(session, playlist.id)
    session.commit()
    remaining = crud.list_songs(session)
    print(f"    删除后数据库剩 {len(remaining)} 首歌")

    session.close()

    print("\n" + "=" * 50)
    print("CRUD 演示完成！增删改查全部验证通过。")
    print("=" * 50)


if __name__ == "__main__":
    main()
