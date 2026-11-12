# 开发路线图

每天 30 分钟，10 周完成。每个阶段完成后做一次 Git 提交并推送到 GitHub。

## Phase 1 · 环境与基础 (Week 1)

目标：跑通骨架，建立 Git 工作流。

- [x] 项目骨架搭建（由助手完成）
- [x] 确认 Python 3.11+ 已安装
- [x] 在项目目录创建 venv 虚拟环境
- [x] 安装开发依赖 `pip install -r requirements-dev.txt`
- [x] 跑通 `python main.py`
- [x] 跑通 `pytest`（冒烟测试通过）
- [x] `git init` + 首次提交
- [x] 在 GitHub 建仓库并推送

## Phase 2 · 数据模型与存储 (Week 2-3)

目标：能用 SQLite 存取歌曲数据。

- [x] 安装 SQLAlchemy，写入 requirements.txt
- [x] 实现 `database.py`：engine / Session / init_db
- [x] 实现 `models.py`：Song / Artist / Album / Playlist 模型
- [x] 编写 `init_db()` 建表脚本
- [x] 封装 CRUD 操作（增删改查）
- [x] 单元测试：模型创建、查询

## Phase 3 · 音乐文件处理 (Week 4)

目标：扫描本地音乐文件夹，自动入库。

- [ ] 安装 mutagen
- [ ] 实现 `read_metadata()`：读取单文件元数据
- [ ] 实现 `scan_directory()`：递归扫描
- [ ] 处理中文标签编码问题
- [ ] 写入数据库（与 Phase 2 衔接）
- [ ] 单元测试：用样本文件测试

## Phase 4 · CLI 命令行界面 (Week 5)

目标：命令行完成所有操作。

- [ ] 安装 typer
- [ ] 实现 add / list / search 命令
- [ ] 实现歌单管理命令
- [ ] 美化输出（rich 表格）
- [ ] 单元测试：命令调用

## Phase 5 · GUI 图形界面 (Week 6-7)

目标：有可用的桌面应用。

- [ ] 安装 PyQt6
- [ ] 主窗口布局（歌单树 + 歌曲表格）
- [ ] 工具栏与菜单
- [ ] 集成播放功能（pygame 或 vlc）
- [ ] 搜索与筛选
- [ ] 歌单管理界面

## Phase 6 · AI 智能增强 (Week 8-9)

目标：让项目「懂 AI」。

- [ ] 安装 librosa
- [ ] 提取音频特征（BPM、能量、频谱）
- [ ] 基于特征相似度的推荐
- [ ] 接入大模型：自然语言生成歌单
- [ ] 把推荐结果接入 CLI / GUI

## Phase 7 · 打包与发布 (Week 10)

目标：能给别人用，简历可挂。

- [ ] PyInstaller 打包成可执行文件
- [ ] GitHub Actions 配置 CI（自动跑 pytest）
- [ ] 完善 README（截图、使用说明）
- [ ] 打 tag，发布 Release
