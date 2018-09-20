# -*- mode: python -*-

block_cipher = None


a = Analysis(['SSVG.py'],
             pathex=['C:\\Users\\shush_000\\Documents\\Python_Development\\SolarSystemVoyager\\PyInstaller'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
a.datas += [('SSVG.ico', '.\\SSVG.ico', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SSVG',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='SSVG.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SSVG')
