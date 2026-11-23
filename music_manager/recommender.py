"""AI 推荐（Phase 6）。

两个增强方向：

1. 基于音频特征的内容推荐（本阶段实现）
   - 用 librosa 提取每首歌的特征（BPM、能量、频谱质心、过零率）
   - 存入 Song.features 字段（JSON）
   - 基于余弦相似度推荐相似歌曲
   - 这是「懂算法」的体现

2. 大模型生成歌单（后续扩展）
   - 用户说「今晚想安静学习」
   - 大模型理解意图，从库里选歌组成歌单
   - 需要接入大模型 API（OpenAI / 智谱 / 通义千问等）
"""
import json
from pathlib import Path

import numpy as np
import librosa

from music_manager.models import Song


def extract_features(file_path):
    """提取音频特征。

    用 librosa 分析音频文件，提取 4 个特征：
    - tempo: BPM（节奏速度，越大越快）
    - rms: 均方根能量（响度，越大越响）
    - spectral_centroid: 频谱质心（音色亮度，越高越明亮）
    - zero_crossing_rate: 过零率（音色特征，越高越尖锐）

    只分析前 30 秒，加快速度。
    返回字典，失败返回 None。
    """
    try:
        # 加载音频：duration=30 只取前30秒，sr=22050 采样率
        y, sr = librosa.load(file_path, duration=30, sr=22050)

        # 提取节奏（BPM）
        # librosa 1.0+ 的 beat_track 可能返回 numpy 数组，统一转成标量
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(np.atleast_1d(tempo)[0])

        # 提取其他特征（都是 numpy 数组，取均值变成单个数）
        rms = float(np.mean(librosa.feature.rms(y=y)))
        spectral_centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
        zcr = float(np.mean(librosa.feature.zero_crossing_rate(y=y)))

        return {
            "tempo": float(tempo),
            "rms": rms,
            "spectral_centroid": spectral_centroid,
            "zero_crossing_rate": zcr,
        }
    except Exception as e:
        print(f"  提取失败 {Path(file_path).name}: {e}")
        return None


def features_to_vector(features):
    """把特征字典转成 numpy 向量，用于相似度计算。"""
    if not features:
        return None
    return np.array([
        features["tempo"],
        features["rms"],
        features["spectral_centroid"],
        features["zero_crossing_rate"],
    ])


def compute_similarity(vec1, vec2):
    """计算两个特征向量的余弦相似度。

    返回 0~1 的值，越接近 1 表示越相似。
    余弦相似度 = 两向量夹角的余弦 = 归一化后的点积。
    不受特征数值大小影响（因为归一化了）。
    """
    if vec1 is None or vec2 is None:
        return 0.0
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))


def extract_all_features(session):
    """为数据库里所有歌曲提取特征，存入 features 字段。

    已有特征的会跳过（避免重复提取）。
    返回新提取的数量。
    """
    songs = session.query(Song).all()
    count = 0
    total = len(songs)
    for i, song in enumerate(songs, 1):
        if song.features:
            continue
        print(f"  [{i}/{total}] {song.title}...", end=" ", flush=True)
        features = extract_features(song.file_path)
        if features:
            song.features = json.dumps(features)
            count += 1
            print("OK")
        else:
            print("跳过")
    session.commit()
    return count


def recommend(session, song_id, n=5):
    """基于特征相似度推荐 n 首相似的歌曲。

    找出与指定歌曲特征最相似的其他歌曲。
    返回 [(song, similarity), ...] 列表，按相似度降序。
    """
    target = session.query(Song).filter(Song.id == song_id).first()
    if not target or not target.features:
        return []

    target_vec = features_to_vector(json.loads(target.features))
    if target_vec is None:
        return []

    # 计算与所有其他歌的相似度
    all_songs = session.query(Song).filter(
        Song.id != song_id, Song.features.isnot(None)
    ).all()
    similarities = []
    for song in all_songs:
        vec = features_to_vector(json.loads(song.features))
        sim = compute_similarity(target_vec, vec)
        similarities.append((song, sim))

    # 按相似度排序，取前 n
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:n]
