import subprocess
import os
import shutil

# Build docs
os.chdir('doc_src')
subprocess.run(['mkdocs', 'build', '--clean'])
os.chdir('..')

# Build executable/bundle
subprocess.run(['pyinstaller', '--clean', '--noconfirm', 'hex-spreadsheet.spec'])

# Clean up build directories
#shutil.rmtree()
