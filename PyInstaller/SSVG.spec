# -*- mode: python -*-
import sys
sys.setrecursionlimit(5000)

block_cipher = None

added_files = [
    ('SSVG_data/*.*', 'SSVG_data'),
    ('SSVG_i18n/*.*', 'SSVG_i18n'),
    ('SSVG_log/*.*', 'SSVG_log'),
    ('SSVG_plan/*.*', 'SSVG_plan'),
    ('ssvgicon.ico', '.'),
    ('SSVG_UsersGuide-en.pdf', '.'),
    ('SSVG_UsersGuide-ja.pdf', '.'),
    ('ipaexg.ttf', 'mpl-data/fonts/ttf')
    ]
a = Analysis(['SSVG.py'],
             pathex=['C:\\Users\\shush_000\\Documents\\Python_Development\\SolarSystemVoyager\\PyInstaller'],
             binaries=[],
             datas=added_files,
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
          name='SSVG',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='ssvgicon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SSVG')
