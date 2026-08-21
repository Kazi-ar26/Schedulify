from PyInstaller.utils.hooks import collect_submodules


hiddenimports = collect_submodules("models") + [
    "PySide6",
    "sqlalchemy",
]


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("Assets", "Assets"),
        ("styles", "styles"),
        ("config.json", "."),
    ],
    hiddenimports=[
    'passlib.handlers.bcrypt'
    ],
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
    a.binaries,
    a.datas,
    [],
    name="Schedulify",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon="Assets/icons/schedulify.ico",
)