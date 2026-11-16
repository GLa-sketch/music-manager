# Phase 3 动作表 · 音乐文件处理

目标：扫描本地音乐文件夹，自动读取元数据入库。
助手已写好 metadata_scanner.py 和 scripts/demo_scan.py。

---

## Day 14 · 装 mutagen + 跑扫描

**目标**：扫描你自己的音乐文件夹，看到真实歌曲入库。

```powershell
# 1. 激活 venv
.\venv\Scripts\Activate.ps1

# 2. 装 mutagen
pip install mutagen

# 3. 扫描你的音乐文件夹（路径换成你自己的）
python scripts/demo_scan.py "C:/Users/18496/Music"
```

**预期**：找到音乐文件 → 读取元数据 → 导入数据库 → 显示新增几首。

跑通后提交：
```powershell
git add .
git commit -m "phase3: 音乐文件扫描入库"
git push
```

---

## Day 15 · 读 metadata_scanner.py

理解三个核心函数：
- `read_metadata()`：读单个文件的元数据
- `scan_directory()`：递归扫描文件夹
- `import_to_database()`：扫描 + 入库（去重）

---

## Day 16 · 用 DB Browser 验证

打开 music_manager.db，确认扫描的歌曲都在 songs 表里。

---

## Day 17 · 收尾提交

---

## Phase 3 完成标志

- [ ] 能扫描一个音乐文件夹
- [ ] 元数据正确读取（歌名、艺术家、专辑、时长）
- [ ] 数据导入数据库，不重复导入
- [ ] 已提交推送到 GitHub
