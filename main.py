from PySide6.QtWidgets import QApplication
from gui import DownloaderGUI
from style import apply_system_style
import sys

app = QApplication(sys.argv)
apply_system_style()
window = DownloaderGUI()
window.show()
sys.exit(app.exec())
