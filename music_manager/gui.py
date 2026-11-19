"""图形界面（Phase 5）。

使用 PyQt6 实现桌面 GUI。
主窗口：工具栏 + 歌曲列表表格 + 状态栏。

这是程序第一次有图形界面——能点开用、能点击操作。

运行方式：
    python -m music_manager.gui
"""
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QWidget,
    QFileDialog, QLabel, QHeaderView,
)

from music_manager.database import init_db, get_session
from music_manager import crud
from music_manager.metadata_scanner import import_to_database


class MainWindow(QMainWindow):
    """主窗口。

    布局：
      ┌──────────────────────────────────┐
      │ [扫描文件夹] [搜索框________] [刷新] │  ← 工具栏
      ├──────────────────────────────────┤
      │ ID | 标题 | 艺术家 | 专辑 | 时长   │
      │ 1  | ...  | ...    | ...  | ...  │  ← 歌曲表格
      │ 2  | ...  | ...    | ...  | ...  │
      │ ...                              │
      ├──────────────────────────────────┤
      │ 共 82 首歌                        │  ← 状态栏
      └──────────────────────────────────┘
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Manager")
        self.resize(800, 600)

        init_db()
        self._build_ui()
        self._load_songs()

    def _build_ui(self):
        """构建界面布局。"""
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # 顶部工具栏：扫描按钮 + 搜索框 + 刷新按钮
        toolbar = QHBoxLayout()

        self.btn_scan = QPushButton("扫描文件夹")
        self.btn_scan.clicked.connect(self._on_scan)  # 点击时调用 _on_scan
        toolbar.addWidget(self.btn_scan)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("输入关键词搜索歌曲...")
        self.search_box.textChanged.connect(self._on_search)  # 输入变化时触发
        toolbar.addWidget(self.search_box)

        self.btn_refresh = QPushButton("刷新")
        self.btn_refresh.clicked.connect(self._load_songs)
        toolbar.addWidget(self.btn_refresh)

        layout.addLayout(toolbar)

        # 歌曲表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "标题", "艺术家", "专辑", "时长"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # 只读
        layout.addWidget(self.table)

        # 状态栏（QMainWindow 自带的状态栏）
        self.status_label = QLabel("就绪")
        self.statusBar().addWidget(self.status_label)

    def _fill_table(self, songs):
        """把歌曲列表填充到表格。

        提取成公共方法，_load_songs 和 _on_search 都复用它。
        """
        self.table.setRowCount(len(songs))
        for row, song in enumerate(songs):
            self.table.setItem(row, 0, QTableWidgetItem(str(song.id)))
            self.table.setItem(row, 1, QTableWidgetItem(song.title))
            artist = song.artist.name if song.artist else "未知"
            self.table.setItem(row, 2, QTableWidgetItem(artist))
            album = song.album.title if song.album else ""
            self.table.setItem(row, 3, QTableWidgetItem(album))
            duration = f"{song.duration // 60}:{song.duration % 60:02d}" if song.duration else ""
            self.table.setItem(row, 4, QTableWidgetItem(duration))

    def _load_songs(self):
        """加载所有歌曲到表格。"""
        session = get_session()
        songs = crud.list_songs(session)
        session.close()
        self._fill_table(songs)
        self.status_label.setText(f"共 {len(songs)} 首歌")

    def _on_search(self, text):
        """搜索过滤（搜索框文字变化时实时触发）。"""
        session = get_session()
        if text:
            songs = crud.search_songs(session, text)
        else:
            songs = crud.list_songs(session)
        session.close()
        self._fill_table(songs)
        self.status_label.setText(f"找到 {len(songs)} 首")

    def _on_scan(self):
        """扫描文件夹入库。点按钮弹出文件夹选择对话框。"""
        directory = QFileDialog.getExistingDirectory(self, "选择音乐文件夹")
        if not directory:
            return

        self.status_label.setText(f"扫描中: {directory}")
        QApplication.processEvents()  # 让界面刷新一下，避免界面卡住

        session = get_session()
        count = import_to_database(session, directory)
        session.close()

        self.status_label.setText(f"新增 {count} 首")
        self._load_songs()


def main():
    """启动 GUI 应用。"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
