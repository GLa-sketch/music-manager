# Music Manager | Python 音乐管理系统

一个用 Python 从零搭建的本地音乐管理系统：管理音乐文件、读取元数据、生成歌单、智能推荐。

## 为什么做这个项目

- 练习 Python 全栈开发（数据层 → CLI → GUI → AI 增强）
- 结合 AI 时代：融入音频特征推荐与大模型接入
- 沉淀一个能放到 GitHub 的完整作品

## 技术栈

| 层 | 技术 | 启用阶段 |
|---|---|---|
| 语言 | Python 3.11+ | Phase 1 |
| 存储 | SQLite + SQLAlchemy | Phase 2 |
| 元数据 | mutagen | Phase 3 |
| CLI | typer | Phase 4 |
| GUI | PyQt6 | Phase 5 |
| AI | librosa + 大模型 | Phase 6 |
| 测试 | pytest | 全程 |
| CI/CD | GitHub Actions | Phase 7 |

## 项目结构

```
music-manager/
├── main.py                  # 入口
├── music_manager/           # 主包
│   ├── config.py            # 配置
│   ├── models.py            # 数据模型（Phase 2）
│   ├── database.py          # 数据库连接（Phase 2）
│   ├── metadata_scanner.py  # 元数据扫描（Phase 3）
│   ├── cli.py               # 命令行界面（Phase 4）
│   ├── gui.py               # 图形界面（Phase 5）
│   └── recommender.py       # AI 推荐（Phase 6）
├── tests/                   # 测试
└── docs/roadmap.md          # 开发路线图
```

## 快速开始

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活（Windows Git Bash）
source venv/Scripts/activate

# 3. 安装依赖（目前为空，随阶段增加）
pip install -r requirements.txt

# 4. 运行
python main.py
```

## 开发路线

10 周分 7 个阶段，每天 30 分钟。详见 [docs/roadmap.md](docs/roadmap.md)。

## License

MIT
