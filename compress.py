import zipfile
import os

temp_zip = zipfile.ZipFile("temp.zip", "w")

original_dir = os.getcwd()
os.chdir("src/typst_to_latex")

for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        filename = os.path.join(dirpath, filename).replace("\\", "/")
        temp_zip.write(filename)

os.chdir(original_dir)

if os.path.exists("typst_to_latex.ankiaddon"):
    os.remove("typst_to_latex.ankiaddon")

temp_zip.close()

os.rename("temp.zip", "typst_to_latex.ankiaddon")