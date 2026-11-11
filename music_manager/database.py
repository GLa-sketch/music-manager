"""数据库连接与初始化。

使用 SQLAlchemy + SQLite，提供数据库基础设施：
- engine: 数据库引擎（连接 SQLite 文件）
- SessionLocal: 会话工厂（生成数据库会话）
- Base: 模型基类（所有 ORM 模型继承它）
- init_db(): 建表（创建所有模型对应的表）
- get_session(): 获取一个数据库会话

类比 Java JPA：
- engine ≈ DataSource
- Session ≈ EntityManager
- Base ≈ 所有 @Entity 的基类
- init_db() ≈ hibernate.hbm2ddl.auto=update
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from music_manager.config import DB_PATH

# SQLite 数据库 URL（指向本地文件）
DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建引擎
# echo=False：不打印 SQL 日志（调试时改成 True 能看到实际执行的 SQL）
engine = create_engine(DATABASE_URL, echo=False)

# 会话工厂：调用 SessionLocal() 生成一个会话
SessionLocal = sessionmaker(bind=engine)

# 模型基类：所有 ORM 模型继承 Base
Base = declarative_base()


def init_db():
    """初始化数据库：创建所有表。

    第一次运行或模型变更后调用。
    会先导入 models，确保所有模型注册到 Base.metadata。
    """
    from music_manager import models  # noqa: F401，确保模型被加载
    Base.metadata.create_all(engine)


def get_session():
    """获取一个数据库会话。

    用法：
        session = get_session()
        # 增删改查操作...
        session.commit()    # 提交事务
        session.close()     # 关闭会话
    """
    return SessionLocal()
