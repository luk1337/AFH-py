import json
from typing import BinaryIO

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor


class AFH:
    URL_BASE = 'https://androidfilehost.com'
    URL_BASE_UPLOADS = 'https://uploads.androidfilehost.com'

    cookie: str = None
    proxies: dict = None
    session: requests.Session = requests.Session()

    def __init__(self, email: str, password: str, **kwargs):
        # Sadly AFH's WAF requires you to have whitelisted ip,
        # therefore using proxies allows you to proxy through /trusted/ IP address (eg. by using an SSH tunnel).
        self.proxies = kwargs.get('proxies')

        # Login
        self._login(email, password)

    def _get(self, url_base: str, method: str = '', **kwargs):
        return self.session.get(f'{url_base}/{method}', params=kwargs, proxies=self.proxies).content

    def _post(self, url_base: str, method: str = '', files: dict = None, **kwargs):
        return self.session.post(f'{url_base}/{method}', data=kwargs, files=files, proxies=self.proxies).content

    def _json_get(self, url_base: str, method: str = '', **kwargs):
        return json.loads(self._get(url_base=url_base, method=method, **kwargs))

    def _json_post(self, url_base: str, method: str = '', files: dict = None, **kwargs):
        return json.loads(self._post(url_base=url_base, method=method, files=files, **kwargs))

    def _login(self, email: str, password: str):
        assert (b'/user/?w=logout' in self._post(self.URL_BASE, 'user/?w=login',
                                                 submit='login',
                                                 email=email,
                                                 password=password,
                                                 remember=1))

    def create_folder(self, parent_id: int, folder_name: str):
        return self._json_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                               action='update-folder',
                               submit='save',
                               flid=None,
                               parent_id=parent_id,
                               folder_name=folder_name)

    def delete_folder(self, flid: int):
        return self._json_post(self.URL_BASE, 'libs/otf/delete.otf.php',
                               action='del-folder',
                               submit='delete',
                               flid=flid)

    def rename_folder(self, flid: int, folder_name: str):
        return self._json_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                               action='update-folder',
                               submit='save',
                               flid=flid,
                               folder_name=folder_name)

    def move_folder(self, flid: int, deviceid: int, folderid: int):
        return self._json_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                               action='move-folder',
                               submit='save',
                               flid=flid,
                               deviceid=deviceid,
                               folderid=folderid)

    def delete_file(self, fid: int):
        return self._json_post(self.URL_BASE, 'libs/otf/delete.otf.php',
                               action='del-file',
                               submit='delete',
                               fid=fid)

    def rename_file(self, fid: int, filename: str):
        return self._json_post(self.URL_BASE, 'libs/otf/files.otf.php',
                               action='update',
                               submit='save',
                               filename=filename,
                               fid=fid)

    def move_file(self, fid: int, deviceid: int, folderid: int):
        return self._json_post(self.URL_BASE, 'libs/otf/modify.otf.php',
                               action='move-file',
                               submit='save',
                               fid=fid,
                               deviceid=deviceid,
                               folderid=folderid)

    def preadd(self, flid: int, filename: str):
        return self._json_post(self.URL_BASE, 'libs/otf/files.otf.php',
                               action='preadd',
                               submit='save',
                               filename=filename,
                               flid=flid)

    def add(self, fid: int, flid: int, filename: str, file_size: int, upload_date: int, md5hash: str):
        return self._json_post(self.URL_BASE, 'libs/otf/files.otf.php',
                               action='add',
                               submit='save',
                               fid=fid,
                               filename=filename,
                               flid=flid,
                               md5hash=md5hash,
                               uploaded=1,
                               upload_date=upload_date,
                               file_size=file_size)

    def import_remote(self, import_type: str, **kwargs):
        return self._json_post(self.URL_BASE_UPLOADS, 'libs/import-remote.php',
                               submit='save',
                               import_type=import_type,
                               ota=0,
                               **kwargs)

    def upload_remote(self, fid: int, filename: str, qqfilename: str, qqfile: BinaryIO, qqtotalfilesize: int,
                      callback: callable = None):
        data = MultipartEncoder(fields={
            'qqfile': (filename, qqfile, 'application/octet-stream'),
            'fid': str(fid),
            'filename': filename,
            'loc': 'files',
            'qquuid': str(fid),
            'qqfilename': qqfilename,
            'qqtotalfilesize': str(qqtotalfilesize)
        })

        if callback is not None:
            data = MultipartEncoderMonitor(data, callback)

        return json.loads(self.session.post(f'{self.URL_BASE_UPLOADS}/libs/upload-remote.php', data=data,
                                            headers={'Content-Type': data.content_type},
                                            proxies=self.proxies).content)

    def get_download_mirrors(self, fid: int):
        return self._json_post(self.URL_BASE, 'libs/otf/mirrors.otf.php',
                               action='getdownloadmirrors',
                               submit='submit',
                               fid=fid)

    def get_waiting_time(self):
        return self._json_post(self.URL_BASE, 'libs/otf/checks.otf.php',
                               w='waitingtime')

    def get_ftp_server_url(self, server: int):
        return self._json_post(self.URL_BASE, 'libs/otf/checks.otf.php',
                               w='get-ftp-server-url',
                               submit='get',
                               server=server)

    def check_email_availability(self, email: str):
        return self._json_post(self.URL_BASE, 'libs/otf/checks.otf.php',
                               w='email',
                               email=email,
                               submit='submit')

    def check_screen_name_availability(self, screenname: str):
        return self._json_post(self.URL_BASE, 'libs/otf/checks.otf.php',
                               w='screenname',
                               screenname=screenname,
                               submit='submit')

    def stats(self, fid: int, w: str, mirror: str):
        return self._json_get(self.URL_BASE, 'libs/otf/stats.otf.php',
                              fid=fid,
                              w=w,
                              mirror=mirror)
