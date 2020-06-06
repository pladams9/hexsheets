import subprocess
import os
import shutil

# Build docs
os.chdir('doc_src')
subprocess.run(['mkdocs', 'build', '--clean'])
os.chdir('..')

# Build executable/bundle
subprocess.run(['pyinstaller', '--clean', '--noconfirm', 'hexsheets.spec'])

# Clean up build directories
try:
    shutil.rmtree('build')
except Exception:
    print('Error removing build folders.')
