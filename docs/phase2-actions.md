# Phase 2 动作表 · 数据模型与存储

目标：让项目能存取数据。用 SQLAlchemy ORM + SQLite。
助手已写好 database.py / models.py / scripts/demo_db.py，你负责：跑通 -> 理解 -> 测试 -> 提交。

---

## Day 8 · 装 SQLAlchemy + 跑通演示

**目标**：看到数据真的存进数据库。

```powershell
# 确保在 venv 里（没激活就 .\venv\Scripts\Activate.ps1）

# 1. 装 SQLAlchemy
pip install SQLAlchemy

# 2. 跑演示脚本
python scripts/demo_db.py
```

**预期输出**：看到建表、插入周杰伦/范特西/简单爱、查询展示。

跑通后提交：
```powershell
git add .
git commit -m "phase2: 数据模型与数据库初始化"
git push
```

---

## Day 9 · 读代码，理解 ORM

**目标**：看懂 models.py 每个模型在干什么。

打开 `music_manager/models.py`，对照 Java JPA 理解：

| Python (SQLAlchemy) | Java (JPA/Hibernate) |
|---|---|
| `class Song(Base)` | `@Entity class Song` |
| `__tablename__ = "songs"` | `@Table(name="songs")` |
| `Column(Integer, primary_key=True)` | `@Id Integer id` |
| `Column(String(200), nullable=False)` | `@Column(length=200, nullable=false)` |
| `ForeignKey("artists.id")` | `@ManyToOne` |
| `relationship("Album", back_populates=...)` | `@OneToMany` |

理解「关系」是关键：
- `artist.songs` 直接拿到这个艺术家所有歌（不用写 SQL JOIN）
- `song.artist` 直接拿到这首歌的艺术家
- 这就是 ORM 的威力：用对象操作数据库

---

## Day 10 · 用 DB Browser 看数据库

**目标**：直观看到数据库文件里的表和数据。

1. 下载 DB Browser for SQLite（免费）：https://sqlitebrowser.org/dl/
2. 打开 `music-manager/music_manager.db`
3. 点「浏览数据」，能看到 artists / albums / songs / playlists 表

---

## Day 11 · 写 CRUD 封装

新建 `music_manager/crud.py`，封装常用操作（增删改查）。

---

## Day 12 · 写单元测试

新建 `tests/test_models.py`，测试模型创建、查询、关系。
跑 `pytest` 确保全绿。

---

## Day 13 · 收尾提交

```powershell
git add .
git commit -m "phase2: CRUD封装与单元测试"
git push
```

---

## Phase 2 完成标志

- [ ] `python scripts/demo_db.py` 能建表 + 插数据 + 查询
- [ ] 能用 DB Browser 看到 .db 文件里的表
- [ ] 理解 ORM 模型与 Java JPA 的对应关系
- [ ] 有 CRUD 封装和单元测试
- [ ] 已提交推送到 GitHub
