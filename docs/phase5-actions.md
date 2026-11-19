# Phase 5 动作表 · GUI 图形界面

目标：做成能点开用的桌面应用。
助手已写好 gui.py，用 PyQt6 实现主窗口 + 歌曲表格 + 搜索 + 扫描。

---

## Day 1 · 装 PyQt6 + 启动 GUI

```powershell
# 激活 venv
.\venv\Scripts\Activate.ps1

# 装 PyQt6
pip install PyQt6

# 启动 GUI
python -m music_manager.gui
```

**预期**：弹出一个窗口，标题「Music Manager」，显示歌曲列表表格。

试操作：
- 在搜索框输入「Alarm」，表格实时过滤
- 点「扫描文件夹」，选一个文件夹扫描入库
- 点「刷新」重新加载

跑通后提交：
```powershell
git add .
git commit -m "phase5: GUI图形界面"
git push
```

---

## Day 2 · 读 gui.py

理解 PyQt6 的核心概念：
- QMainWindow：主窗口
- 布局（QVBoxLayout / QHBoxLayout）：控件怎么排列
- 信号与槽（clicked.connect）：按钮点击怎么触发函数
- QTableWidget：表格控件

---

## Day 3 · 收尾

---

## Phase 5 完成标志

- [ ] 能启动 GUI 窗口
- [ ] 表格显示歌曲列表
- [ ] 搜索框实时过滤
- [ ] 能扫描文件夹入库
- [ ] 已提交推送到 GitHub
