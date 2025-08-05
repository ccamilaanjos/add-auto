from PySide6.QtCore import QThread, Signal
from downloader import open_semester

class DownloadWorker(QThread):
    operation_finished = Signal(dict)
    error = Signal(str)

    def __init__(self, url, path, folder, semester):
        super().__init__()
        self.url = url
        self.path = path
        self.folder = folder
        self.semester = semester

    def run(self):
        try:
            stats = open_semester(self.url, self.path, self.folder, self.semester)
            self.operation_finished.emit(stats)
        except Exception as e:
            self.error.emit(str(e))
