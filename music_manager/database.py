"""数据库连接（Phase 2 填充）。

将使用 SQLAlchemy 创建：
- engine: 数据库引擎
- Session: 会话工厂
- init_db(): 初始化数据库（建表）

目前为占位，等待 Phase 2 实现。
"""
from music_manager.config import DB_PATH

# TODO Phase 2:
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from music_manager.models import Base
#
# engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
# Session = sessionmaker(bind=engine)
#
# def init_db():
#     Base.metadata.create_all(engine)
#
# def get_session():
#     return Session()
