# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('db', 'db'),
        ('auth', 'auth'),
        ('ui', 'ui'),
        ('utils', 'utils'),
    ],
    hiddenimports=[
        'db', 'db.connection', 'db.schema', 'db.models',
        'auth', 'auth.password',
        'ui', 'ui.theme', 'ui.components', 'ui.login', 'ui.dashboard', 'ui.invoice',
        'utils', 'utils.validators', 'utils.formatters',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RiceMill ERP',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
