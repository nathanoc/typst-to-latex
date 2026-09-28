from aqt.qt import *

class PandocPathEditDialog(QDialog):
    def __init__(self, parent: QWidget | None = None, pandoc_path: str | None = None):
        super().__init__(parent)

        self.setWindowTitle("Edit Pandoc path...")

        self.edit = QLineEdit()
        if pandoc_path:
            self.edit.setText(pandoc_path)

        self.button = QPushButton()
        self.button.setText("Choose file...")
        self.button.clicked.connect(self.choose_file)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)

        edit_layout = QHBoxLayout()
        edit_layout.addWidget(self.edit)
        edit_layout.addWidget(self.button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(edit_layout)
        main_layout.addWidget(save_btn)

        self.setLayout(main_layout)

    def choose_file(self):
        pandoc_path, _ = QFileDialog.getOpenFileName(
            self,
            "Locate Pandoc binary...",
        )

        if pandoc_path:
            self.edit.setText(pandoc_path)