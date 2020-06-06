# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

with open('VERSION', 'r') as file:
    version_number = file.readline().strip()

a = Analysis(['src/hexsheets.py'],
             pathex=[''],
             binaries=[],
             datas=[('src/docs', 'docs')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=('hexsheets-'+ version_number),
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='hexsheets')
