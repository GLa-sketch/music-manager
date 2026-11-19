# Phase 4 动作表 · CLI 命令行界面

目标：程序第一次"能被使用"——敲命令操作音乐库。
助手已写好 cli.py，复用 Phase 2 的 crud 和 Phase 3 的 metadata_scanner。

---

## Day 1 · 装 typer + 跑命令

```powershell
# 激活 venv
.\venv\Scripts\Activate.ps1

# 装 typer（PowerShell 里方括号要加引号）
pip install "typer[all]"

# 试命令
python -m music_manager.cli list
python -m music_manager.cli search "Alarm"
python -m music_manager.cli stats
python -m music_manager.cli playlist list
python -m music_manager.cli playlist create "我的歌单"
```

跑通后提交：
```powershell
git add .
git commit -m "phase4: CLI命令行界面"
git push
```

---

## Day 2 · 读 cli.py

理解 typer 怎么把 Python 函数变成命令行命令。

---

## Day 3 · 测试 + 收尾

---

## Phase 4 完成标志

- [ ] 能用 list 命令列出歌曲
- [ ] 能用 search 命令搜索
- [ ] 能用 scan 命令扫描文件夹
- [ ] 能用 playlist 命令管理歌单
- [ ] 已提交推送到 GitHub
