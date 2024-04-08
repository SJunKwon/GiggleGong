# -*- mode: python ; coding: utf-8 -*-



a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app/createAlarm.html', 'app'),
        ('app/editAlarm.html', 'app'),
        ('app/game.html', 'app'),
        ('app/index.html', 'app'),
        ('app/scripts.js', 'app'),
        ('app/assets/styles.css', 'app/assets'),
        ('app/assets/clock.ico', 'app/assets')
        ('app/GoogleChromePortable', 'app/GoogleChromePortable')
    ],
    hiddenimports=['bottle_websocket'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GiggleGong',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GiggleGong',
)
