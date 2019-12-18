#!/usr/bin/env python3
import os
import sys

from config import Config
from pyafh.afh import AFH


def simple_ftp_import(afh: AFH, flid: int, fldr: str, file_path: str):
    filename = os.path.basename(file_path)

    preadd = afh.preadd(flid=flid, filename=filename)

    ftplist = afh.import_remote(import_type='ftplist', fldr=fldr)
    _, filesize, upload_date = next((x for x in ftplist['DATA'] if x[0] == filename), None)

    import_remote = afh.import_remote(import_type='ftp', fid=preadd['DATA']['fid'], fldr=fldr, file_path=file_path)

    afh.add(fid=preadd['DATA']['fid'], flid=flid, filename=filename, file_size=filesize, upload_date=upload_date,
            md5hash=import_remote['DATA']['md5hash'])

    return f'{afh.URL_BASE}/?fid={preadd["DATA"]["fid"]}'


def run():
    if len(sys.argv) != 4:
        sys.exit(f'usage: {sys.argv[0]} [flid] [fldr] [file_path]')

    _, flid, fldr, file_path = sys.argv
    afh = AFH(email=Config.Email, password=Config.Password, proxies=Config.Proxies)

    print(simple_ftp_import(afh=afh, flid=flid, fldr=fldr, file_path=file_path))


if __name__ == '__main__':
    run()
