#!/usr/bin/env python3
import os
import sys

from tqdm import tqdm

from config import Config
from pyafh.afh import AFH


def simple_web_upload(afh: AFH, server: int, flid: int, file_path: str):
    file = open(file_path, 'rb')
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)

    preadd = afh.preadd(flid=flid, filename=filename)
    server = afh.get_server_url(server=server)

    with tqdm(total=filesize, leave=False, unit='blocks', unit_scale=True) as progress_bar:
        upload_remote = afh.upload_remote(server_url=server['URL'], fid=preadd['DATA']['fid'],
                                          filename=preadd['DATA']['new_filename'],
                                          qqfilename=filename, qqfile=file, qqtotalfilesize=filesize,
                                          callback=lambda monitor: progress_bar.update(
                                              monitor.bytes_read - progress_bar.n))

    afh.add(fid=preadd['DATA']['fid'], flid=flid, filename=filename, file_size=upload_remote['file_size'],
            upload_date=upload_remote['upload_date'], md5hash=upload_remote['md5hash'])

    return f'{afh.URL_BASE}/?fid={preadd["DATA"]["fid"]}'


def run():
    if len(sys.argv) != 4:
        sys.exit(f'usage: {sys.argv[0]} [server] [flid] [file_path]]')

    _, server, flid, file_path = sys.argv
    afh = AFH(email=Config.Email, password=Config.Password, proxies=Config.Proxies)

    print(simple_web_upload(afh=afh, server=server, flid=flid, file_path=file_path))


if __name__ == '__main__':
    run()
