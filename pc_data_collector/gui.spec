# -*- mode: python -*-
a = Analysis(['gui.py'],
             pathex=['C:\\Users\\frank\\Projects\\power_estimator\\data_collection'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
			 
import glob

imagesList = []
allImages = glob.glob('.\\ui\\*.png')
for eachImage in allImages:
	imageParts = eachImage.split('\\')
	print("%s" % eachImage)
	imagesList.append( (eachImage, eachImage,  'DATA') )
print imagesList
a.datas += imagesList


pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='data_collector.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
