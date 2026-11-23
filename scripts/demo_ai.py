"""AI 推荐演示。

演示基于音频特征的推荐：
1. 为所有歌曲提取特征（首次需要几分钟）
2. 选一首歌，展示它的特征
3. 推荐相似的歌曲

运行：python scripts/demo_ai.py
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from music_manager.database import init_db, get_session
from music_manager.models import Song
from music_manager.recommender import extract_all_features, recommend


def main():
    print("=" * 50)
    print("Phase 6 · AI 推荐演示")
    print("=" * 50)

    init_db()
    session = get_session()

    # 第 1 步：提取所有歌曲的特征
    print("\n[1] 提取音频特征（首次可能需要几分钟，请耐心等待）...")
    count = extract_all_features(session)
    total = session.query(Song).filter(Song.features.isnot(None)).count()
    print(f"\n    新提取 {count} 首，共 {total} 首已有特征")

    if total == 0:
        print("    特征提取失败，无法推荐。")
        session.close()
        return

    # 第 2 步：选第一首歌，展示特征
    first = session.query(Song).filter(Song.features.isnot(None)).first()
    features = json.loads(first.features)
    print(f"\n[2] 以「{first.title}」为例，它的音频特征：")
    print(f"    BPM（节奏速度）: {features['tempo']:.0f}")
    print(f"    能量（响度）:    {features['rms']:.3f}")
    print(f"    频谱质心（亮度）: {features['spectral_centroid']:.0f}")
    print(f"    过零率（尖锐度）: {features['zero_crossing_rate']:.4f}")

    # 第 3 步：推荐相似歌曲
    print(f"\n[3] 与「{first.title}」最相似的 5 首歌：")
    results = recommend(session, first.id, n=5)
    if not results:
        print("    没有找到相似歌曲（可能只有一首有特征）。")
    else:
        for song, sim in results:
            print(f"    {song.id}: {song.title} (相似度: {sim:.3f})")

    session.close()

    print("\n" + "=" * 50)
    print("AI 推荐演示完成！")
    print("这就是「基于内容的推荐」——根据音频特征找相似歌曲。")
    print("网易云/Spotify 的「相似歌曲推荐」就是类似原理。")
    print("=" * 50)


if __name__ == "__main__":
    main()
