"""docx-js writes word/fontTable.xml but never relates it from document.xml,
and the Office validator treats an unrelated part as corruption. Add the one
missing relationship in place. Idempotent.

    python3 postfix.py <file.docx>
"""
import re, shutil, sys, tempfile, zipfile, pathlib

src = pathlib.Path(sys.argv[1])
REL = ('<Relationship Id="rIdFontTable" '
       'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" '
       'Target="fontTable.xml"/>')
tmp = pathlib.Path(tempfile.mkstemp(suffix=".docx")[1])
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/_rels/document.xml.rels" and b"fontTable.xml" not in data:
            data = data.replace(b"</Relationships>", REL.encode() + b"</Relationships>")
        zout.writestr(item, data)
shutil.move(str(tmp), str(src))
print("related fontTable.xml in", src.name)
