"""命令行界面。

用 typer 提供命令行交互，复用 crud 和 metadata_scanner 的功能。
这是程序第一次"能被使用"——敲命令就能操作音乐库。

运行方式：
    python -m music_manager.cli list
    python -m music_manager.cli search "Alarm"
    python -m music_manager.cli scan "C:/Windows/Media"
    python -m music_manager.cli stats
    python -m music_manager.cli playlist list
    python -m music_manager.cli playlist create "我的歌单"
"""
import typer

from music_manager.database import init_db, get_session
from music_manager import crud
from music_manager.metadata_scanner import import_to_database

# 创建 typer 应用（相当于命令行程序的入口）
app = typer.Typer(help="音乐管理系统命令行工具")

# 歌单子命令组：playlist create / playlist list / playlist add ...
playlist_app = typer.Typer(help="歌单管理")
app.add_typer(playlist_app, name="playlist")


@app.command("list")
def list_songs():
    """列出所有歌曲。"""
    init_db()
    session = get_session()
    songs = crud.list_songs(session)
    if not songs:
        typer.echo("数据库里还没有歌曲。用 scan 命令扫描音乐文件夹。")
    else:
        typer.echo(f"共 {len(songs)} 首歌：\n")
        typer.echo(f"{'ID':<5} {'标题':<30} {'艺术家':<20} {'时长'}")
        typer.echo("-" * 70)
        for s in songs:
            artist = s.artist.name if s.artist else "未知"
            duration = f"{s.duration // 60}:{s.duration % 60:02d}" if s.duration else "?"
            typer.echo(f"{s.id:<5} {s.title:<30} {artist:<20} {duration}")
    session.close()


@app.command("search")
def search_songs(keyword: str):
    """搜索歌曲（按标题模糊匹配）。

    用法：python -m music_manager.cli search "Alarm"
    """
    init_db()
    session = get_session()
    songs = crud.search_songs(session, keyword)
    if not songs:
        typer.echo(f"没找到标题含「{keyword}」的歌曲。")
    else:
        typer.echo(f"找到 {len(songs)} 首含「{keyword}」的歌曲：\n")
        for s in songs:
            artist = s.artist.name if s.artist else "未知"
            duration = f"{s.duration // 60}:{s.duration % 60:02d}" if s.duration else "?"
            typer.echo(f"  {s.id}: {s.title} - {artist} ({duration})")
    session.close()


@app.command("scan")
def scan_directory(directory: str):
    """扫描音乐文件夹，导入数据库。

    用法：python -m music_manager.cli scan "C:/Windows/Media"
    """
    init_db()
    session = get_session()
    typer.echo(f"扫描目录: {directory}")
    count = import_to_database(session, directory)
    typer.echo(f"新增 {count} 首歌曲。")
    session.close()


@app.command("stats")
def show_stats():
    """显示音乐库统计信息。"""
    init_db()
    session = get_session()
    artists = crud.list_artists(session)
    songs = crud.list_songs(session)
    playlists = crud.list_playlists(session)
    typer.echo("音乐库统计：")
    typer.echo(f"  艺术家: {len(artists)}")
    typer.echo(f"  歌曲:   {len(songs)}")
    typer.echo(f"  歌单:   {len(playlists)}")
    session.close()


# ========== 歌单子命令 ==========

@playlist_app.command("create")
def playlist_create(name: str, description: str = ""):
    """创建歌单。

    用法：python -m music_manager.cli playlist create "我的歌单"
    """
    init_db()
    session = get_session()
    playlist = crud.create_playlist(session, name, description or None)
    session.commit()
    typer.echo(f"创建歌单「{playlist.name}」(id={playlist.id})")
    session.close()


@playlist_app.command("list")
def playlist_list():
    """列出所有歌单。"""
    init_db()
    session = get_session()
    playlists = crud.list_playlists(session)
    if not playlists:
        typer.echo("还没有歌单。用 playlist create 创建。")
    else:
        typer.echo(f"共 {len(playlists)} 个歌单：\n")
        for p in playlists:
            typer.echo(f"  {p.id}: {p.name}（{len(p.songs)} 首）- {p.description or ''}")
    session.close()


@playlist_app.command("add")
def playlist_add(playlist_id: int, song_id: int):
    """往歌单里加歌。

    用法：python -m music_manager.cli playlist add 1 5
    （把歌曲 id=5 加入歌单 id=1）
    """
    init_db()
    session = get_session()
    result = crud.add_song_to_playlist(session, playlist_id, song_id)
    if result:
        session.commit()
        typer.echo(f"歌曲 {song_id} 已加入歌单 {playlist_id}")
    else:
        typer.echo("失败：歌单或歌曲不存在")
    session.close()


@playlist_app.command("songs")
def playlist_songs(playlist_id: int):
    """查看歌单里的歌。

    用法：python -m music_manager.cli playlist songs 1
    """
    init_db()
    session = get_session()
    songs = crud.get_playlist_songs(session, playlist_id)
    if not songs:
        typer.echo(f"歌单 {playlist_id} 里没有歌，或歌单不存在。")
    else:
        typer.echo(f"歌单 {playlist_id} 里有 {len(songs)} 首：\n")
        for s in songs:
            typer.echo(f"  {s.id}: {s.title}")
    session.close()


if __name__ == "__main__":
    app()
