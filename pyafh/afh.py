import json
from typing import BinaryIO

import requests


class AFH:
    URL_BASE = 'https://androidfilehost.com'
    URL_BASE_UPLOADS = 'https://uploads.androidfilehost.com'
    USER_AGENT = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

    cookie: str = None
    proxies: dict = None

    def __init__(self, **kwargs):
        self.cookie = kwargs.get('cookie')
        self.proxies = kwargs.get('proxies')

    def _api_get(self, url_base: str, method: str = '', **kwargs):
        return requests.get(f'{url_base}/{method}', data=kwargs, headers={'cookie': self.cookie},
                            proxies=self.proxies).content

    def _api_post(self, url_base: str, method: str = '', files: dict = None, **kwargs):
        return requests.post(f'{url_base}/{method}', data=kwargs, headers={'cookie': self.cookie},
                             files=files, proxies=self.proxies).content

    def is_cookie_valid(self):
        return b'/user/?w=logout' in self._api_get(self.URL_BASE)

    def create_folder(self, parent_id: int, folder_name: str):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                                         action='update-folder',
                                         submit='save',
                                         flid=None,
                                         parent_id=parent_id,
                                         folder_name=folder_name))

    def delete_folder(self, flid: int):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/delete.otf.php',
                                         action='del-folder',
                                         submit='delete',
                                         flid=flid))

    def rename_folder(self, flid: int, folder_name: str):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                                         action='update-folder',
                                         submit='save',
                                         flid=flid,
                                         folder_name=folder_name))

    def move_folder(self, flid: int, deviceid: int, folderid: int):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                                         action='move-folder',
                                         submit='save',
                                         flid=flid,
                                         deviceid=deviceid,
                                         folderid=folderid))

    def delete_file(self, fid: int):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/delete.otf.php',
                                         action='del-file',
                                         submit='delete',
                                         fid=fid))

    def rename_file(self, fid: int, filename: str):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/files.otf.php',
                                         action='update',
                                         submit='save',
                                         filename=filename,
                                         fid=fid))

    def move_file(self, fid: int, deviceid: int, folderid: int):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                                         action='move-file',
                                         submit='save',
                                         fid=fid,
                                         deviceid=deviceid,
                                         folderid=folderid))

    def preadd(self, flid: int, filename: str):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/files.otf.php',
                                         action='preadd',
                                         submit='save',
                                         filename=filename,
                                         flid=flid))

    def add(self, fid: int, flid: int, filename: str, file_size: int, upload_date: int, md5hash: str):
        return json.loads(self._api_post(self.URL_BASE, 'libs/otf/files.otf.php',
                                         action='add',
                                         submit='save',
                                         fid=fid,
                                         filename=filename,
                                         flid=flid,
                                         md5hash=md5hash,
                                         uploaded=1,
                                         upload_date=upload_date,
                                         file_size=file_size))

    def upload_remote(self, fid: int, filename: str, qqfilename: str, qqfile: BinaryIO, qqtotalfilesize: int):
        return json.loads(self._api_post(self.URL_BASE_UPLOADS, 'libs/upload-remote.php',
                                         {'qqfile': qqfile},
                                         fid=fid,
                                         filename=filename,
                                         loc='files',
                                         qquuid=fid,
                                         qqfilename=qqfilename,
                                         qqtotalfilesize=qqtotalfilesize))