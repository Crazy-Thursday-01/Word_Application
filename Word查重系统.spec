# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit()*5)
block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\python\\python_learn\\Engineering_training\\infomation.env','.'),('C:\\Users\\86136\\Desktop\\文件\\shared\\favicon.ico','.')],
    hiddenimports=['sklearn','sklearn.pipeline','sklearn.ensemble._forest','sklearn.utils._typedefs','sklearn.utils._heap','sklearn.utils._sorting','sklearn.utils._vector_sentinel','sklearn.neighbors._partition_nodes','sklearn.metrics._pairwise_distances_reduction._datasets_pair','sklearn.metrics._pairwise_distances_reduction._middle_term_computer'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Word查重系统',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
     icon="F:/下载内容/favicon_logosc/favicon.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Word查重系统',
)
