block_cipher = None

# add templates and static folders to a list
added_files =[
    ('templates/*.html', 'templates'),
    ('static/*.css', 'static'),
    ]

a = Analysis(['web.py'],
             pathex=['./'],
             binaries=[],
             datas = added_files, # set datas = added_files list
             hiddenimports=['jinja2.ext'], # be sure to add jinja2 
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
          name='web',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='web')
