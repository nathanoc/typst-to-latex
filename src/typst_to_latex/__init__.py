import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
from anki.hooks import addHook

# Was using this for type hints, but seems like some Anki installations don't have aqt.editor_legacy
# from aqt.editor_legacy import Editor

import re
import pypandoc

from pathlib import Path

from .preamble_edit_dialog import PreambleEditDialog

config = mw.addonManager.getConfig(__name__) or {
    "preamble": "user_files/preamble.typ"
}

def get_preamble():
    return Path(os.path.join(os.path.dirname(__file__), config["preamble"])).read_text()

def prepend_preamble(text):
    return f"{get_preamble()}\n\n{text}"

def onReplacePress(editor):
    if editor.currentField is None:
        showInfo("You need to select a field")
        return
    
    # Find current field by comparing note fields against editor.currentField
    fields = editor.note.col.models.current()["flds"]
    field_names = [f["name"] for f in fields]
    current_field = field_names[editor.currentField]

    # We first convert from HTML to plaintext (which will be valid Typst code), and then convert from Typst to LaTeX.
    # TODO: Error handling
    new_note_text = re.sub(r"\$.*?\$",
                           lambda match: pypandoc.convert_text(
                               prepend_preamble(pypandoc.convert_text(match.group(0), "plain", "html")),
                               "latex",
                               "typst"),
                           editor.note[current_field])

    editor.note[current_field] = new_note_text
    editor.setNote(editor.note)

def addReplaceButton(buttons, editor):
    editor._links["convert"] = onReplacePress
    return buttons + [editor.addButton(
        None,
        "convert",
        onReplacePress,
        "Convert Typst to LaTeX",
        "Typst to LaTeX")]

def onPreamblePress(editor):
    preamble_settings = PreambleEditDialog(preamble = get_preamble())
    full_preamble_path = Path(
        os.path.join(os.path.dirname(__file__), config["preamble"])
    )

    if preamble_settings.exec():
        input = preamble_settings.input.toPlainText()
        with open(full_preamble_path, "w") as f:
            f.write(input)
            f.flush()

def addPreambleButton(buttons, editor):
    editor._links["preamble"] = onPreamblePress
    return buttons + [editor.addButton(
        None,
        "preamble",
        onPreamblePress,
        "Edit preamble",
        "Preamble"
    )]

addHook("setupEditorButtons", addReplaceButton)
addHook("setupEditorButtons", addPreambleButton)