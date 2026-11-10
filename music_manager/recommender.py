"""AI 推荐（Phase 6 填充）。

两个增强方向，体现「AI 时代的计算机专业素养」：

1. 基于音频特征的内容推荐
   - 用 librosa 提取每首歌的特征（BPM、能量、音色、频谱）
   - 基于特征相似度做「相似歌曲推荐」
   - 这是「懂算法」的体现

2. 大模型接入：自然语言生成歌单
   - 用户说「今晚想安静学习」
   - 大模型理解意图，从库里选歌组成歌单
   - 这是「会用 AI」的体现

目前为占位，等待 Phase 6 实现。
"""

# TODO Phase 6:
# import librosa
# import numpy as np
#
# def extract_features(file_path) -> np.ndarray:
#     """提取音频特征向量。"""
#     ...
#
# def recommend(song_id: int, n: int = 10) -> list[int]:
#     """基于特征相似度推荐 n 首歌。"""
#     ...
#
# def generate_playlist_by_prompt(prompt: str) -> list[int]:
#     """用大模型根据自然语言描述生成歌单。"""
#     ...
