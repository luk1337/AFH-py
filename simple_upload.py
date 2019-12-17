#!/usr/bin/env python3
import hashlib
import os
import sys
import time
from typing import BinaryIO

from tqdm import tqdm

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

    with tqdm(total=filesize, leave=False, unit='blocks', unit_scale=True) as progress_bar:
        afh.upload_remote(fid=preadd['DATA']['fid'], filename=preadd['DATA']['new_filename'],
                          qqfilename=filename, qqfile=file, qqtotalfilesize=filesize,
                          callback=lambda monitor: progress_bar.update(monitor.bytes_read - progress_bar.n))

    afh.add(fid=preadd['DATA']['fid'], flid=flid, filename=filename, file_size=filesize,
            upload_date=int(time.time()), md5hash=md5(file))

    return f'{afh.URL_BASE}/?fid={preadd["DATA"]["fid"]}'


def run():
    _, flid, file_path = sys.argv
    afh = AFH(email=Config.Email, password=Config.Password, proxies=Config.Proxies)

    print(f'done! [ url: {simple_upload(afh=afh, flid=flid, file_path=file_path)} ]')


if __name__ == '__main__':
    run()
