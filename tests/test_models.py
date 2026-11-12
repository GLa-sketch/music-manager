"""数据模型与 CRUD 的单元测试。

用内存数据库（sqlite:///:memory:）做测试，不污染主数据库。
每个测试函数运行前都会重新建表，保证环境干净、互不影响。

类似 Java JUnit 的 @BeforeEach：fixture 在每个测试前准备环境。
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from music_manager.database import Base
from music_manager.models import Artist, Album, Song, Playlist
from music_manager import crud


@pytest.fixture
def session():
    """每个测试用的内存数据库 session。

    - 创建内存数据库（不写文件，测试完即消失）
    - 建所有表
    - 测试函数运行
    - 自动关闭清理
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # 这一行把 session 交给测试函数用
    session.close()


# ========== 模型测试 ==========

def test_create_artist(session):
    """测试创建艺术家。"""
    artist = Artist(name="测试歌手", country="中国")
    session.add(artist)
    session.commit()
    assert artist.id is not None          # id 应该自动生成
    assert artist.name == "测试歌手"


def test_create_song_with_artist(session):
    """测试创建歌曲并关联艺术家（一对多）。"""
    artist = Artist(name="周杰伦")
    song = Song(title="夜曲", artist=artist, duration=235, file_path="/test/夜曲.mp3")
    session.add_all([artist, song])
    session.commit()
    # 双向关联都能访问
    assert song.artist.name == "周杰伦"        # 歌 -> 艺术家
    assert artist.songs[0].title == "夜曲"      # 艺术家 -> 歌


def test_playlist_many_to_many(session):
    """测试歌单和歌曲的多对多关系。"""
    artist = Artist(name="周杰伦")
    song1 = Song(title="夜曲", artist=artist, file_path="/test/1.mp3")
    song2 = Song(title="晴天", artist=artist, file_path="/test/2.mp3")
    playlist = Playlist(name="我的歌单")
    playlist.songs = [song1, song2]
    session.add_all([artist, song1, song2, playlist])
    session.commit()
    # 正向：歌单 -> 歌
    assert len(playlist.songs) == 2
    # 反向：歌 -> 歌单
    assert playlist in song1.playlists


def test_song_default_added_at(session):
    """测试 added_at 字段自动填充时间。"""
    song = Song(title="测试", file_path="/test.mp3")
    session.add(song)
    session.commit()
    assert song.added_at is not None       # 应该自动填了当前时间


# ========== CRUD 测试 ==========

def test_crud_add_song(session):
    """测试 crud.add_song：加歌并自动关联艺术家。"""
    song = crud.add_song(
        session, title="七里香", artist_name="周杰伦",
        duration=296, file_path="/test/七里香.mp3", genre="流行",
    )
    session.commit()
    assert song.id is not None
    assert song.title == "七里香"
    assert song.artist.name == "周杰伦"     # 艺术家自动关联了


def test_crud_search_songs(session):
    """测试 crud.search_songs 模糊搜索。"""
    crud.add_song(session, title="夜曲", artist_name="周杰伦", file_path="/test/1.mp3")
    crud.add_song(session, title="夜的第七章", artist_name="周杰伦", file_path="/test/2.mp3")
    crud.add_song(session, title="晴天", artist_name="周杰伦", file_path="/test/3.mp3")
    session.commit()
    results = crud.search_songs(session, "夜")   # 搜含"夜"的
    assert len(results) == 2                      # 应该找到 2 首


def test_crud_update_song_title(session):
    """测试 crud.update_song_title。"""
    song = crud.add_song(session, title="老标题", artist_name="歌手", file_path="/test.mp3")
    session.commit()
    crud.update_song_title(session, song.id, "新标题")
    session.commit()
    refreshed = crud.get_song(session, song.id)
    assert refreshed.title == "新标题"


def test_crud_delete_song(session):
    """测试 crud.delete_song。"""
    song = crud.add_song(session, title="要删的歌", artist_name="歌手", file_path="/test.mp3")
    session.commit()
    result = crud.delete_song(session, song.id)
    session.commit()
    assert result is True
    assert crud.get_song(session, song.id) is None   # 删完应该查不到了


def test_crud_playlist_operations(session):
    """测试歌单操作：创建 + 加歌 + 查询。"""
    song = crud.add_song(session, title="歌1", artist_name="歌手", file_path="/test.mp3")
    playlist = crud.create_playlist(session, "测试歌单", "描述")
    session.commit()
    crud.add_song_to_playlist(session, playlist.id, song.id)
    session.commit()
    songs = crud.get_playlist_songs(session, playlist.id)
    assert len(songs) == 1
    assert songs[0].title == "歌1"
