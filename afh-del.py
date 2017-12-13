#!/usr/bin/env python3
from afh import AFH
import config, sys, os

if not len(sys.argv) == 2:
    exit("Usage: afh-ftp [file-id]")

fileId = sys.argv[1]

afh = AFH(config.cookie, config.ftpUsername)

if not afh.isCookieValid():
    exit("[ERROR] Cookie is invalid or expired!")

deleteData = afh.deleteFile(fileId)

''' Cool debug stuff :3
print('deleteData :', deleteData)
'''