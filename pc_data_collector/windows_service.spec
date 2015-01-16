# -*- mode: python -*-
a = Analysis(['windows_service.py'],
             pathex=['C:\\Users\\frank\\Projects\\power_estimator\\data_collection'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
		  a.binaries,
          a.zipfiles,
          a.datas,
          name='data_collector_service.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
