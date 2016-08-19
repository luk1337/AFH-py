#!/usr/bin/env python3
from afh import AFH
import config, sys

if not len(sys.argv) == 4:
    exit("Usage: afh-url [folder-id] [download-url] [file-name]")

folderId = sys.argv[1]
downloadUrl = sys.argv[2]
fileName = sys.argv[3]

afh = AFH(config.cookie, config.uid, config.ftpUsername)
queue = afh.addToQueue(folderId, downloadUrl)
fileId = afh.getFileId(folderId, fileName)
importData = afh.importFileURL(folderId, fileId['DATA']['fid'], downloadUrl)
uploadData = afh.updateFile(fileId['DATA']['fid'], importData['md5hash'], importData['upload_date'], importData['file_size'])

''' Cool debug stuff :3
print('queue :', queue)
print('fileId :', fileId)
print('importData :', importData)
print('uploadData :', uploadData)
'''

print('https://www.androidfilehost.com/?fid=' + fileId['DATA']['fid'])
