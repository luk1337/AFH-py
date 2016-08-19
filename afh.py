#!/usr/bin/env python3

class AFH:
    cookie = None
    uid = None
    username = None

    def __init__(self, cookie, uid, username):
        self.importDependencies()

        self.cookie = cookie
        self.uid = uid
        self.username = username

    def importDependencies(self):
        global urlencode, Request, urlopen, HTTPError, FTP, error_perm, json, os

        from urllib.parse import urlencode
        from urllib.request import Request, urlopen, HTTPError
        from ftplib import FTP, error_perm
        import json, os

    def addToQueue(self, folderId, downloadUrl):
        url = 'https://androidfilehost.com/libs/otf/import.otf.php'
        postData = {
            'submit': 'save',
            'import_type': 'size',
            'flid': folderId,
            'url_to_import': downloadUrl
        }
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, urlencode(postData).encode(), headers)
           data = json.loads(urlopen(request).read().decode())
        except HTTPError as error:
            data = error.read()

        return data

    def getFileId(self, folderId, fileName):
        global json, cookie, uid

        url = 'https://androidfilehost.com/libs/otf/files.otf.php'
        postData = {
            'action': 'add',
            'submit': 'save',
            'filename': fileName,
            'flid': folderId,
            'uid': self.uid
        }
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, urlencode(postData).encode(), headers)
           data = json.loads(urlopen(request).read().decode())
        except HTTPError as error:
            data = error.read()

        return data

    def getFileListFTP(self):
        global json, cookie

        url = 'https://qc0.uploads.androidfilehost.com/libs/import-remote.php'
        postData = {
            'import_type': 'ftplist',
            'fldr': self.username + '/'
        }
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, urlencode(postData).encode(), headers)
           data = json.loads(urlopen(request).read().decode())
        except HTTPError as error:
            data = error.read()

        return data

    def importFileURL(self, folderId, fileId, downloadUrl):
        global json, cookie

        url = 'https://fl1.uploads.androidfilehost.com/libs/import-remote.php'
        postData = {
            'submit': 'save',
            'import_type': 'url',
            'flid': folderId,
            'fid': fileId,
            'url_to_import': downloadUrl,
            'ota': '0'
        }
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, urlencode(postData).encode(), headers)
           data = json.loads(urlopen(request).read().decode())
        except HTTPError as error:
            data = error.read()

        return data

    def importFileFTP(self, fileId, filePath):
        global json, cookie

        url = 'https://qc0.uploads.androidfilehost.com/libs/import-remote.php'
        postData = {
            'import_type': 'ftp',
            'fldr': self.username + '/',
            'fid': fileId,
            'file_path': filePath,
            'ota': '0'
        }
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, urlencode(postData).encode(), headers)
           data = json.loads(urlopen(request).read().decode())
        except HTTPError as error:
            data = error.read()

        return data

    def uploadFileFTP(self, host, username, password, filePath):
        ftp = FTP(host)

        ftp.login(username, password)
        ftp.storbinary('STOR %s' % os.path.basename(filePath), open(filePath, 'rb'))

    def updateFile(self, fileId, md5sum, uploadDate, fileSize):
        global json, cookie

        url = 'https://androidfilehost.com/libs/otf/files.otf.php'
        postData = {
            'action': 'update',
            'submit': 'save',
            'fid': fileId,
            'md5hash': md5sum,
            'uploaded': '1',
            'upload_date': uploadDate,
            'file_size': fileSize
        }
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, urlencode(postData).encode(), headers)
           data = json.loads(urlopen(request).read().decode())
        except HTTPError as error:
            data = error.read()

        return data
