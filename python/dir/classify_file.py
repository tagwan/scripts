import os
import shutil
from time import strftime

"""
扫描脚本目录，并给出不同类型脚本的计数
"""

logsdir="c:\logs\puttylogs"
zipdir="c:\logs\puttylogs\zipped_logs"
zip_program="zip.exe"

for files in os.listdir(logsdir):
	if files.endswith(".log"):
		files1=files+"."+strftime("%Y-%m-%d")+".zip"
		os.chdir(logsdir)
		os.system(zip_program + " " +  files1 +" "+ files)
		shutil.move(files1, zipdir)
		os.remove(files)