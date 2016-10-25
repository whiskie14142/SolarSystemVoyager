# -*- mode: python -*-

block_cipher = None
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(['SSVG.py'],
             pathex=['C:\\Users\\shush_000\\Documents\\Python_Development\\SSVoyager\\PyInstaller'],
             binaries=None,
             datas=None,
             hiddenimports = collect_submodules('pkg_resources._vendor'),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SSVG',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SSVG')
