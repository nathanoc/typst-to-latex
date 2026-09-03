import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "vendor"))

from aqt.utils import showInfo
from aqt.qt import *
from anki.hooks import addHook

# Was using this for type hints, but seems like some Anki installations don't have aqt.editor_legacy
# from aqt.editor_legacy import Editor

import re
import pypandoc

def onButtonPress(editor):
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
                               pypandoc.convert_text(match.group(0), "plain", "html"),
                               "latex",
                               "typst"),
                           editor.note[current_field])

    editor.note[current_field] = new_note_text
    editor.setNote(editor.note)

def addMyButton(buttons, editor):
    editor._links["convert"] = onButtonPress
    return buttons + [editor.addButton(
        None,
        "convert",
        onButtonPress,
        "Convert Typst to LaTeX",
        "Typst to LaTeX")]

addHook("setupEditorButtons", addMyButton)