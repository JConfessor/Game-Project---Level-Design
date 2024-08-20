# -- mode: python ; coding: utf-8 --

block_cipher = None

a = Analysis(
    ['game.py'],
    pathex=[''], 
    binaries=[],
    datas=[
        ('assets/background.jpeg', 'assets'),
        ('assets/spaceship.png', 'assets'),
        ('assets/enemyship.png', 'assets'),
        ('assets/bullet.png', 'assets'),
        ('assets/bonus.png', 'assets'),
        ('assets/life.png', 'assets'),
        ('assets/life-bonus.png', 'assets'),
        ('assets/speed-bonus.png', 'assets'),
        # Adicione mais arquivos conforme necessário
    ],
    hiddenimports=[],  
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Desabilite o UPX
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Modo janela
    icon='Icone.ico',  # Certifique-se de que o arquivo 'Icone.ico' esteja disponível
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
