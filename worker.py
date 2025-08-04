from PySide6.QtCore import QThread, Signal

class DownloadWorker(QThread):
    finished = Signal()
    error = Signal(str)

    def __init__(self, url, path, folder):
        super().__init__()
        self.url = url
        self.path = path
        self.folder = folder

    def run(self):
        try:
            from downloader import open_semester
            open_semester(self.url, self.path, self.folder)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))
