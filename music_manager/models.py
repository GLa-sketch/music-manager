"""数据模型定义。

定义音乐管理系统的 5 个核心数据结构：
- Artist: 艺术家
- Album: 专辑
- Song: 歌曲（核心实体）
- Playlist: 歌单
- playlist_song: 歌单与歌曲的多对多关联表

设计要点：
1. 每个类对应数据库一张表（__tablename__）
2. Column 定义字段，类似 Java JPA 的 @Column
3. ForeignKey 定义外键，类似 @ManyToOne
4. relationship 定义对象关联，自动管理关联对象
5. Song.features 为 Phase 6 AI 推荐预留（存 librosa 提取的音频特征 JSON）
"""
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, Text, ForeignKey, Table
)
from sqlalchemy.orm import relationship

from music_manager.database import Base


# 多对多关联表：歌单 <-> 歌曲
# 这是一张独立的表，不对应模型类，只记录关联关系
# 类似 Java JPA 的 @JoinTable
playlist_song = Table(
    "playlist_song",
    Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("position", Integer),  # 歌曲在歌单中的播放顺序
)


class Artist(Base):
    """艺术家。一个艺术家有多张专辑、多首歌曲。"""
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    country = Column(String(50))  # 国籍，可选

    # 关系：artist.albums 能直接拿到这个艺术家的所有专辑
    albums = relationship("Album", back_populates="artist")
    songs = relationship("Song", back_populates="artist")

    def __repr__(self):
        return f"<Artist {self.name}>"


class Album(Base):
    """专辑。属于一个艺术家，包含多首歌曲。"""
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    year = Column(Integer)  # 发行年份
    cover_path = Column(String(500))  # 封面图路径，可选

    # 关系
    artist = relationship("Artist", back_populates="albums")
    songs = relationship("Song", back_populates="album")

    def __repr__(self):
        return f"<Album {self.title}>"


class Song(Base):
    """歌曲。系统的核心实体。

    features 字段为 Phase 6 AI 推荐预留：
    用 librosa 提取音频特征（BPM、能量、频谱），存成 JSON 字符串。
    这样后期做推荐时不用重新分析音频，直接从数据库取特征向量。
    """
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))
    duration = Column(Integer)  # 时长（秒）
    file_path = Column(String(500), nullable=False)  # 音频文件路径
    bitrate = Column(Integer)  # 比特率（kbps）
    genre = Column(String(50))  # 流派
    track_no = Column(Integer)  # 音轨号（在专辑中的序号）
    features = Column(Text)  # 音频特征 JSON（Phase 6 启用）
    added_at = Column(DateTime, default=datetime.now)  # 入库时间

    # 关系
    artist = relationship("Artist", back_populates="songs")
    album = relationship("Album", back_populates="songs")
    # 多对多：一首歌可以在多个歌单里
    playlists = relationship(
        "Playlist", secondary=playlist_song, back_populates="songs"
    )

    def __repr__(self):
        return f"<Song {self.title}>"


class Playlist(Base):
    """歌单。一个歌单包含多首歌曲（多对多）。"""
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))  # 歌单描述
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 多对多关系：playlist.songs 直接拿到歌单里所有歌
    songs = relationship(
        "Song", secondary=playlist_song, back_populates="playlists"
    )

    def __repr__(self):
        return f"<Playlist {self.name}>"
