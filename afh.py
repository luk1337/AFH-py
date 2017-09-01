#!/usr/bin/env python3
import json, os
from urllib.parse import urlencode
from urllib.request import Request, urlopen, HTTPError
from ftplib import FTP, error_perm
from tqdm import tqdm

class AFH:
    cookie = None
    username = None

    def __init__(self, cookie, username):
        self.cookie = cookie
        self.username = username

    def isCookieValid(self):
        url = 'https://androidfilehost.com'
        headers = {
            'cookie': self.cookie
        }

        try:
           request = Request(url, None, headers)
           data = urlopen(request).read().decode()
           data = "/user/?w=logout" in data
        except HTTPError as error:
            data = error.read()

        return data

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
        global json, cookie

        url = 'https://androidfilehost.com/libs/otf/files.otf.php'
        postData = {
            'action': 'preadd',
            'submit': 'save',
            'filename': fileName,
            'flid': folderId
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

        with tqdm(unit = 'blocks', unit_scale = True, leave = False, miniters = 1, total = os.path.getsize(filePath)) as tqdm_instance:
            ftp.storbinary('STOR {}'.format(os.path.basename(filePath)), open(filePath, 'rb'), 2048, callback = lambda sent: tqdm_instance.update(len(sent)))

        ftp.quit()

    def updateFile(self, fileId, fileName, folderId, md5sum, uploadDate, fileSize):
        global json, cookie

        url = 'https://androidfilehost.com/libs/otf/files.otf.php'
        postData = {
            'action': 'add',
            'submit': 'save',
            'fid': fileId,
            'flid': folderId,
            'filename': fileName,
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