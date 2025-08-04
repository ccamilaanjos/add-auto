from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from worker import DownloadWorker
from data import data_code_path

class DownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Disciplina Downloader")
        self.resize(450, 250)
        self.url_ads = 'https://ads.ifba.edu.br/'
        self.download_path = ""

        self.semester_label = QLabel("Selecione o semestre:")
        self.semester_combo = QComboBox()
        self.subject_label = QLabel("Selecione a disciplina (ou 'Todas'):")
        self.subject_combo = QComboBox()
        self.path_button = QPushButton("Selecionar pasta de download")
        self.download_button = QPushButton("Baixar")

        layout = QVBoxLayout()
        layout.addWidget(self.semester_label)
        layout.addWidget(self.semester_combo)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_combo)
        layout.addWidget(self.path_button)
        layout.addWidget(self.download_button)
        self.setLayout(layout)

        self.semester_combo.addItems(data_code_path.keys())
        self.semester_combo.currentIndexChanged.connect(self.update_subjects_combo)
        self.download_button.clicked.connect(self.download)
        self.path_button.clicked.connect(self.select_download_path)

        self.update_subjects_combo()

    def update_subjects_combo(self):
        selected_semester = self.semester_combo.currentText()
        self.subject_combo.clear()
        self.subject_combo.addItem("Todas")
        subjects = data_code_path[selected_semester]
        self.subject_combo.addItems(subjects.keys())

    def select_download_path(self):
        path = QFileDialog.getExistingDirectory(self, "Selecione a pasta de download")
        if path:
            self.download_path = path
            self.path_button.setText(f"Pasta: {path}")

    def download(self):
        if not self.download_path:
            QMessageBox.warning(self, "Aviso", "Selecione uma pasta de download antes de continuar.")
            return

        if hasattr(self, "worker") and self.worker.isRunning():
            QMessageBox.warning(self, "Aviso", "Já há um download em andamento.")
            return

        semester = self.semester_combo.currentText()
        subject = self.subject_combo.currentText()
        folder = semester

        if subject == "Todas":
            url = self.url_ads + semester
        else:
            subject_code = data_code_path[semester][subject]
            url = self.url_ads + 'file' + subject_code

        self.download_button.setEnabled(False)
        self.download_button.setText("Baixando...")

        self.worker = DownloadWorker(url, self.download_path, folder)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_download_error)
        self.worker.start()

    def on_download_finished(self):
        self.cleanup_worker()
        self.download_button.setEnabled(True)
        self.download_button.setText("Baixar")
        QMessageBox.information(self, "Sucesso", "Download concluído!")

    def on_download_error(self, error_msg):
        self.cleanup_worker()
        self.download_button.setEnabled(True)
        self.download_button.setText("Baixar")
        QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {error_msg}")

    def cleanup_worker(self):
        if hasattr(self, "worker"):
            try:
                self.worker.finished.disconnect(self.on_download_finished)
            except TypeError:
                pass
            try:
                self.worker.error.disconnect(self.on_download_error)
            except TypeError:
                pass
 
