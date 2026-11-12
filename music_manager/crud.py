"""CRUD 操作封装（数据访问层）。

把对数据库的增删改查封装成函数，类似 Java 的 DAO/Repository 模式。
所有函数接收 session 参数，由调用方管理 session 的创建和关闭。

为什么封装成函数？
- 不用每次都重复写 session.query(...) 那套
- 操作集中在一处，方便维护
- 后续 Phase 4 的 CLI 会直接调用这些函数

用法：
    from music_manager.database import get_session
    from music_manager import crud

    session = get_session()
    songs = crud.list_songs(session)    # 查
    for s in songs:
        print(s.title, s.artist.name)
    session.close()
"""
from music_manager.models import Artist, Album, Song, Playlist


# ========== 查询（Read）==========

def list_songs(session):
    """列出所有歌曲。"""
    return session.query(Song).all()


def list_artists(session):
    """列出所有艺术家。"""
    return session.query(Artist).all()


def list_playlists(session):
    """列出所有歌单。"""
    return session.query(Playlist).all()


def get_song(session, song_id):
    """按 id 查单首歌，找不到返回 None。"""
    return session.query(Song).filter(Song.id == song_id).first()


def search_songs(session, keyword):
    """按标题搜索歌曲（模糊匹配）。类似 SQL 的 LIKE '%keyword%'。"""
    return session.query(Song).filter(Song.title.contains(keyword)).all()


def get_artist_songs(session, artist_id):
    """获取某艺术家的所有歌。"""
    return session.query(Song).filter(Song.artist_id == artist_id).all()


# ========== 新增（Create）==========

def add_artist(session, name, country=None):
    """新增艺术家。如果同名已存在，直接返回已有的（避免重复）。"""
    existing = session.query(Artist).filter_by(name=name).first()
    if existing:
        return existing
    artist = Artist(name=name, country=country)
    session.add(artist)
    session.flush()  # flush：写入数据库但暂不提交，这样能拿到自动生成的 id
    return artist


def add_song(session, title, artist_name, duration=None, file_path="",
             genre=None, album_title=None, track_no=None):
    """新增歌曲。自动创建或关联艺术家、专辑。

    传入艺术家名字（不是 id），函数内部自动查找或创建。
    这样调用方不用先查艺术家 id，更方便。
    """
    artist = add_artist(session, artist_name)
    album = None
    if album_title:
        album = session.query(Album).filter_by(title=album_title, artist=artist).first()
        if not album:
            album = Album(title=album_title, artist=artist)
            session.add(album)
            session.flush()
    song = Song(
        title=title, artist=artist, album=album,
        duration=duration, file_path=file_path,
        genre=genre, track_no=track_no,
    )
    session.add(song)
    session.flush()
    return song


def create_playlist(session, name, description=None):
    """创建歌单。"""
    playlist = Playlist(name=name, description=description)
    session.add(playlist)
    session.flush()
    return playlist


# ========== 更新（Update）==========

def update_song_title(session, song_id, new_title):
    """修改歌曲标题。"""
    song = get_song(session, song_id)
    if song:
        song.title = new_title
    return song


# ========== 删除（Delete）==========

def delete_song(session, song_id):
    """删除歌曲。"""
    song = get_song(session, song_id)
    if song:
        session.delete(song)
        return True
    return False


def delete_playlist(session, playlist_id):
    """删除歌单（歌单里的歌曲本身不会被删，只是从歌单移除）。"""
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id).first()
    if playlist:
        session.delete(playlist)
        return True
    return False


# ========== 歌单管理 ==========

def add_song_to_playlist(session, playlist_id, song_id):
    """把歌曲加入歌单（多对多关联）。"""
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id).first()
    song = get_song(session, song_id)
    if playlist and song:
        playlist.songs.append(song)  # relationship 自动处理关联表
        return True
    return False


def get_playlist_songs(session, playlist_id):
    """获取歌单里的所有歌。"""
    playlist = session.query(Playlist).filter(Playlist.id == playlist_id).first()
    return playlist.songs if playlist else []
