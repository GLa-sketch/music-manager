"""冒烟测试：确认项目能正常导入和启动。

Phase 1 阶段只跑这个，确保骨架没断。
后续阶段逐步补充各模块的单元测试。
"""
from music_manager import __version__


def test_version_exists():
    """版本号应该存在且是非空字符串。"""
    assert isinstance(__version__, str)
    assert __version__


def test_import_config():
    """config 模块应该能正常导入，且项目根目录存在。"""
    from music_manager import config
    assert config.PROJECT_ROOT.exists()


def test_main_callable():
    """main 入口函数应该可调用。"""
    from main import main
    assert callable(main)
