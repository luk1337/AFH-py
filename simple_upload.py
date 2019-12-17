import hashlib
import logging
import os
import sys
import time
from typing import BinaryIO

from config import Config
from pyafh.afh import AFH


def simple_upload(afh: AFH, flid: int, file_path: str):
    def md5(f: BinaryIO):
        md5sum = hashlib.md5()

        f.seek(0)

        for chunk in iter(lambda: f.read(4096), b''):
            md5sum.update(chunk)

        return md5sum.hexdigest()

    file = open(file_path, 'rb')
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    preadd = afh.preadd(flid=flid, filename=filename)
    logging.info(f'preadd: {preadd}')

    upload_remote = afh.upload_remote(fid=preadd['DATA']['fid'], filename=preadd['DATA']['new_filename'],
                                      qqfilename=filename, qqfile=file, qqtotalfilesize=filesize)
    logging.info(f'upload_remote: {upload_remote}')

    add = afh.add(fid=preadd['DATA']['fid'], flid=flid, filename=filename, file_size=filesize,
                  upload_date=int(time.time()), md5hash=md5(file))
    logging.info(f'add: {add}')

    return f'{afh.URL_BASE}/?fid={preadd["DATA"]["fid"]}'


def run():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

    _, flid, file_path = sys.argv

    afh = AFH(cookie=Config.Cookie, proxies=Config.Proxies)
    assert (afh.is_cookie_valid())

    logging.info(f'done! [ url: {simple_upload(afh=afh, flid=flid, file_path=file_path)} ]')


if __name__ == '__main__':
    run()
