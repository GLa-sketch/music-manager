# Music Manager | Python 音乐管理系统

一个用 Python 从零搭建的本地音乐管理系统：扫描音乐文件、管理歌单、AI 智能推荐。

## 功能

- 📁 **扫描入库**：扫描本地音乐文件夹，自动读取元数据（mp3/flac/m4a/ogg/wav）
- 🎵 **歌曲管理**：增删改查、模糊搜索
- 📋 **歌单管理**：创建歌单、添加歌曲
- 💻 **命令行界面**：typer 驱动的 CLI，8 个命令
- 🖥️ **桌面 GUI**：PyQt6 图形界面，表格展示 + 实时搜索
- 🤖 **AI 推荐**：基于 librosa 音频特征的相似歌曲推荐

## 技术栈

| 层 | 技术 |
|---|---|
| 语言 | Python 3.11+ |
| 数据库 | SQLite + SQLAlchemy ORM |
| 元数据 | mutagen |
| CLI | typer |
| GUI | PyQt6 |
| AI | librosa（音频特征提取 + 余弦相似度推荐） |
| 测试 | pytest |
| CI | GitHub Actions |

## 项目结构

```
music-manager/
├── main.py                      # 入口
├── music_manager/               # 主包
│   ├── config.py                # 配置
│   ├── models.py                # 数据模型（Artist/Album/Song/Playlist）
│   ├── database.py              # 数据库连接
│   ├── crud.py                  # CRUD 封装（DAO 模式）
│   ├── metadata_scanner.py      # 音乐文件扫描入库
│   ├── cli.py                   # 命令行界面
│   ├── gui.py                   # PyQt6 图形界面
│   └── recommender.py           # AI 音频特征推荐
├── tests/                       # 单元测试
├── scripts/                     # 演示脚本
└── docs/                        # 开发文档与路线图
```

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/GLa-sketch/music-manager.git
cd music-manager

# 2. 创建虚拟环境
python -m venv venv
source venv/Scripts/activate    # Windows (Git Bash)
# 或 venv\Scripts\activate       # Windows (PowerShell)

# 3. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. 运行
python -m music_manager.gui       # 启动 GUI
python -m music_manager.cli list  # 或用 CLI
```

## CLI 命令

```bash
python -m music_manager.cli list                    # 列出所有歌曲
python -m music_manager.cli search "关键词"          # 搜索歌曲
python -m music_manager.cli scan "C:/Music"          # 扫描音乐文件夹入库
python -m music_manager.cli stats                   # 统计信息
python -m music_manager.cli playlist list           # 歌单列表
python -m music_manager.cli playlist create "歌单名" # 创建歌单
python -m music_manager.cli playlist add 1 5        # 往歌单加歌
python -m music_manager.cli playlist songs 1        # 查看歌单里的歌
```

## AI 推荐

基于 librosa 提取音频特征（BPM、能量、频谱质心、过零率），用余弦相似度推荐相似歌曲。

```bash
python scripts/demo_ai.py
```

## 测试

```bash
pytest
```

CI 会自动运行测试（GitHub Actions）。

## License

MIT
