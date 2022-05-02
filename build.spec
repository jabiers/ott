# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['jabiott.pyw'],
             pathex=['C:\\repos\\jabi-ott'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.datas += [
    ('ico_coupang_sm.png','C:\\repos\\jabi-ott\\images\\ico_coupang_sm.png', "DATA"), 
    ('ico_disney_sm.png','C:\\repos\\jabi-ott\\images\\ico_disney_sm.png', "DATA"), 
    ('ico_netflix_sm.png','C:\\repos\\jabi-ott\\images\\ico_netflix_sm.png', "DATA"), 
    ('ico_tving_sm.png','C:\\repos\\jabi-ott\\images\\ico_tving_sm.png', "DATA"), 
    ('ico_watcha_sm.png','C:\\repos\\jabi-ott\\images\\ico_watcha_sm.png', "DATA"), 
    ('ico_wavve_sm.png','C:\\repos\\jabi-ott\\images\\ico_wavve_sm.png', "DATA"),
    ('ico_youtube.png','C:\\repos\\jabi-ott\\images\\ico_youtube.png', "DATA"),
    ('ico_appletv_sm.png','C:\\repos\\jabi-ott\\images\\ico_appletv_sm.png', "DATA"),
    ('ico_close.png','C:\\repos\\jabi-ott\\images\\ico_close.png', "DATA"),
    ('img_loading.gif','C:\\repos\\jabi-ott\\images\\img_loading.gif', "DATA"),
    ('loading_bg.png','C:\\repos\\jabi-ott\\images\\loading_bg.png', "DATA"),
    ('bg.png','C:\\repos\\jabi-ott\\images\\bg.png', "DATA"),
    ('ottv.ico','C:\\repos\\jabi-ott\\ottv.ico', "DATA"),
    ('jabiott-firebase-adminsdk-w0rig-5b46a13752.json','C:\\repos\\jabi-ott\\jabiott-firebase-adminsdk-w0rig-5b46a13752.json', "DATA")
]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='jabiott',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
