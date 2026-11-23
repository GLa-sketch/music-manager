# Phase 6 动作表 · AI 智能增强

目标：让项目「懂 AI」。
助手已写好 recommender.py 和 scripts/demo_ai.py。

---

## Day 1 · 装 librosa + 跑 AI 推荐

```powershell
# 激活 venv
.\venv\Scripts\Activate.ps1

# 装 librosa（包较大，可能需要几分钟）
pip install librosa

# 跑 AI 推荐演示
python scripts/demo_ai.py
```

**预期**：提取所有歌曲的音频特征 → 选一首歌 → 推荐相似的歌曲。

跑通后提交：
```powershell
git add .
git commit -m "phase6: AI音频特征推荐"
git push
```

---

## Day 2 · 读 recommender.py

理解：
- librosa 怎么提取音频特征（BPM、能量、频谱）
- 余弦相似度怎么算
- 推荐算法的原理

---

## Day 3 · 接入 CLI（可选）+ 收尾

---

## Phase 6 完成标志

- [ ] 能提取音频特征
- [ ] 能基于特征推荐相似歌曲
- [ ] 已提交推送到 GitHub
