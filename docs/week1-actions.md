# Week 1 动作表 · Phase 1 环境与基础

每天 30 分钟，照着做即可。卡住直接把报错贴给助手。

> 编辑器建议用 VS Code（装好 Python 扩展 + Chinese 语言包），IDEA/PyCharm 也行。
> 以下命令默认在 VS Code 自带终端（Git Bash）里执行。

---

## Day 1 · 打开项目，跑通入口

**目标**：确认骨架能跑。

```bash
# 1. 在 VS Code 中打开文件夹：
#    文件 → 打开文件夹 → 选择 music-manager

# 2. 终端里确认 Python 版本（需 3.11+）
python --version

# 3. 在项目目录创建虚拟环境
python -m venv venv

# 4. 激活虚拟环境
# PowerShell（VS Code 默认终端）：
.\venv\Scripts\Activate.ps1
# Git Bash（如果终端切成了 bash）：
source venv/Scripts/activate
# 如果 PowerShell 报"禁止运行脚本"，先执行一次这条，再激活：
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 5. 跑入口
python main.py
```

**预期输出**：
```
Music Manager v0.1.0
========================================
项目骨架已就绪。
下一步：完成 Phase 1 的 Git 初始化与首次提交。
详见 docs/roadmap.md
```

看到这个就算 Day 1 完成。虚拟环境激活后，终端提示符前会出现 `(venv)`。

---

## Day 2 · 装开发依赖，跑测试

**目标**：让 pytest 跑通，建立「写测试」的习惯。

```bash
# 确保虚拟环境已激活（没激活就再激活一次）
# PowerShell：
.\venv\Scripts\Activate.ps1
# Git Bash：
source venv/Scripts/activate

# 装开发依赖（目前只有 pytest）
pip install -r requirements-dev.txt

# 跑测试
pytest
```

**预期**：3 个测试全部通过（test_version_exists / test_import_config / test_main_callable）。

完成后做一次提交（养成小步提交的习惯）：
```bash
git add .
git commit -m "phase1: 跑通冒烟测试"
```

> 注意：第一次 commit 前需要先 `git init`，详见 Day 3。

---

## Day 3 · Git 初始化与首次提交

**目标**：项目纳入版本控制。

```bash
# 1. 初始化 git 仓库
git init

# 2. 查看状态（应该看到一堆未跟踪文件）
git status

# 3. 设置用户名邮箱（如果之前没设过）
git config user.name "你的名字"
git config user.email "你的邮箱"

# 4. 添加全部文件并提交
git add .
git commit -m "init: 项目骨架搭建完成"
```

提交完用 `git log` 看一眼，能看到那条记录就对了。

---

## Day 4 · 在 GitHub 建仓库

**目标**：有一个线上仓库地址。

1. 登录 github.com
2. 右上角 + → New repository
3. 仓库名填 `music-manager`
4. 选 Public（这是要挂简历的项目）
5. **不要**勾选 README / .gitignore / license（本地已经有了，会冲突）
6. 创建

创建后 GitHub 会给一段命令，复制「…or push an existing repository from the command line」下面的两行。

---

## Day 5 · 推送到 GitHub

**目标**：线上能看到你的代码。

```bash
# 关联远程仓库（把 <你的用户名> 换成自己的）
git remote add origin https://github.com/<你的用户名>/music-manager.git

# 推送
git branch -M main
git push -u origin main
```

刷新 GitHub 页面，能看到所有文件就成功了。

---

## Day 6 · 熟悉项目结构

**目标**：看懂每个文件将来干什么。

打开这些文件读一遍，对照注释理解：

| 文件 | 作用 | 启用阶段 |
|---|---|---|
| `main.py` | 程序入口 | 现在 |
| `music_manager/config.py` | 配置（路径、数据库位置） | 现在 |
| `music_manager/models.py` | 数据模型 | Phase 2 |
| `music_manager/database.py` | 数据库连接 | Phase 2 |
| `music_manager/metadata_scanner.py` | 读音乐元数据 | Phase 3 |
| `music_manager/cli.py` | 命令行 | Phase 4 |
| `music_manager/gui.py` | 图形界面 | Phase 5 |
| `music_manager/recommender.py` | AI 推荐 | Phase 6 |
| `tests/test_smoke.py` | 冒烟测试 | 现在 |

理解「每个文件都是占位，注释里写好了将来要做什么」就够了。

---

## Day 7 · Python 语法快速过（迁移自 Java）

**目标**：把 Java 思维迁移到 Python。

你有 Java 基础，重点看这几个差异点（每个花 5 分钟）：

1. **缩进代替大括号**：Python 用缩进表示代码块，没有 `{}`。
2. **不需要声明类型**（但可以用类型提示）：`name: str = "abc"`。
3. **没有 `new` 关键字**：`Song("title")` 直接调用。
4. **列表 / 字典代替 ArrayList / HashMap**：`[1,2,3]`、`{"k": "v"}`。
5. **`if __name__ == "__main__":`** 相当于 Java 的 `public static void main`。
6. **import 方式**：`from music_manager import config` 类似 Java 的 import。

可以在 `main.py` 里随便写点东西试手感，比如：
```python
songs = ["歌A", "歌B", "歌C"]
for s in songs:
    print(f"正在播放: {s}")
```

跑通就行，不用提交。

---

## Phase 1 完成标志

- [ ] `python main.py` 正常输出
- [ ] `pytest` 全绿
- [ ] Git 仓库已初始化，至少 1 次提交
- [ ] 已推送到 GitHub，线上能看到代码
- [ ] 能说清每个文件将来干什么

全部打勾 → 进入 Phase 2（数据模型与存储），届时找助手展开。
