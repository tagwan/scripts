import shutil
import sys
import time
import os
import argparse

"""
将源目录240天以上的所有文件移动到目标目录
"""

usage = 'python move_files_over_x_days.py -src [SRC] -dst [DST] -days [DAYS]'
description = 'Move files from src to dst if they are older than a certain number of days.  Default is 240 days'

args_parser = argparse.ArgumentParser(usage=usage, description=description)
args_parser.add_argument('-src', '--src', type=str, nargs='?', default='.', help='(OPTIONAL) Directory where files will be moved from. Defaults to current directory')
args_parser.add_argument('-dst', '--dst', type=str, nargs='?', required=True, help='(REQUIRED) Directory where files will be moved to.')
args_parser.add_argument('-days', '--days', type=int, nargs='?', default=240, help='(OPTIONAL) Days value specifies the minimum age of files to be moved. Default is 240.')
args = args_parser.parse_args()

if args.days < 0:
	args.days = 0

src = args.src  # 设置源目录
dst = args.dst  # 设置目标目录
days = args.days # 设置天数
now = time.time()  # 获得当前时间

if not os.path.exists(dst):
	os.mkdir(dst)

for f in os.listdir(src):  # 遍历源目录所有文件
    if os.stat(f).st_mtime < now - days * 86400:  # 判断是否超过240天
        if os.path.isfile(f):  # 检查是否是文件
            shutil.move(f, dst)  # 移动文件