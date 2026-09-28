import os

from aqt.qt import *
from aqt import mw

from .pandoc_path_edit_dialog import PandocPathEditDialog

class PandocMissingDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        self.setWindowTitle("Pandoc not found")

        warning_text = QLabel("<p>The add-on was unable to locate Pandoc on your machine. What would you like to do?</p><p>Note that the add-on will not work without a working Pandoc installation.</p>")

        ignore = QPushButton("Ignore")
        ignore.pressed.connect(self.accept)

        find_pandoc = QPushButton("Locate Pandoc")
        find_pandoc.pressed.connect(self.open_locate_dialog)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(find_pandoc)
        buttons_layout.addWidget(ignore)

        main_layout = QVBoxLayout()
        main_layout.addWidget(warning_text)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

    def open_locate_dialog(self):
        dialog = PandocPathEditDialog()
        if dialog.exec():
            new_path = dialog.edit.text()
            os.environ.setdefault("PYPANDOC_PANDOC", new_path)

            config = mw.addonManager.getConfig(__name__)
            config["pandoc_path"] = new_path
            mw.addonManager.writeConfig(__name__, config)

        self.accept()