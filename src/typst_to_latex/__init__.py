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
        showInfo("Please select the field (e.g. \"Front\") containing the code to convert.")
        return
    
    # Find current field by comparing note fields against editor.currentField
    fields = editor.note.col.models.current()["flds"]
    field_names = [f["name"] for f in fields]
    current_field = field_names[editor.currentField]

    try:
        # We first convert from HTML to plaintext (which will be valid Typst code), and then convert from Typst to LaTeX.
        new_note_text = re.sub(r"\$.*?\$",
                            lambda match: pypandoc.convert_text(
                                prepend_preamble(pypandoc.convert_text(match.group(0), "plain", "html")),
                                "latex",
                                "typst"),
                            editor.note[current_field])

        editor.note[current_field] = new_note_text
        editor.setNote(editor.note)
    except RuntimeError as err:
        error_info = f"<p>An error occurred while converting your Typst code. This may be because your code has issues, or it may be due to a bug in the Typst to LaTeX add-on.</p><p>Error details:</p><code>{str(err)}</code><p>Note: some error messages may suggest installing TinyTeX. <i>You do not need to do this.</i></p></details>"
        showInfo(error_info, type="warning", title="Typst to LaTeX")

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