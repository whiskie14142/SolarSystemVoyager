# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

mkl_dlls = [
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_avx.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_avx2.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_avx512.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_ilp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_intelmpi_ilp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_intelmpi_lp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_lp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_mpich2_ilp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_mpich2_lp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_msmpi_ilp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_blacs_msmpi_lp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_cdft_core.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_core.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_def.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_intel_thread.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_mc.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_mc3.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_msg.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_pgi_thread.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_rt.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_scalapack_ilp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_scalapack_lp64.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_sequential.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_tbb_thread.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_avx.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_avx2.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_avx512.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_cmpt.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_def.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_mc.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_mc2.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\mkl_vml_mc3.1.dll', '.'),
 ('C:\\Users\\shush\\anaconda3\\envs\\ssvg\\Library\\bin\\libiomp5md.dll', '.')
 ]



added_files = [
    ('SSVG_data/*.*', 'SSVG_data'),
    ('SSVG_i18n/*.*', 'SSVG_i18n'),
    ('SSVG_log/*.*', 'SSVG_log'),
    ('SSVG_plan/*.*', 'SSVG_plan'),
    ('ssvgicon.ico', '.'),
    ('SSVGconfig.json', '.'),
    ('SSVG_UsersGuide-en.pdf', '.'),
    ('SSVG_UsersGuide-ja.pdf', '.'),
    ('ipaexg.ttf', 'mpl-data/fonts/ttf')
    ]


a = Analysis(['SSVG.py'],
             pathex=['U:\\Shushi\\Development\\PyInstaller'],
             binaries=mkl_dlls,
             datas=added_files,
             hiddenimports=['scipy.spatial.transform._rotation_groups'],
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
               upx_exclude=[],
               name='SSVG')
