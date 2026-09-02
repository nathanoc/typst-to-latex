import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *
from anki.hooks import addHook
from aqt.editor_legacy import Editor

import re
import pypandoc

def onButtonPress(editor: Editor):
    if editor.currentField is None:
        showInfo("You need to select a field")
        return

    # Find current field by comparing note fields against editor.currentField
    fields = editor.note.col.models.current()["flds"]
    field_names = [f["name"] for f in fields]
    current_field = field_names[editor.currentField]
    
    new_note_text = re.sub("\$(.*?)\$",
                           lambda match: pypandoc.convert_text(match.group(0), "latex", "typst"),
                           editor.note[current_field])

    editor.note[current_field] = new_note_text
    editor.setNote(editor.note)

def addMyButton(buttons, editor: Editor):
    editor._links["convert"] = onButtonPress
    return buttons + [editor.addButton(
        None,
        "convert",
        onButtonPress,
        "Convert Typst to LaTeX",
        "Typst to LaTeX")]

addHook("setupEditorButtons", addMyButton)