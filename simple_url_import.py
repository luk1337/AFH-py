#!/usr/bin/env python3
import os
import sys

from config import Config
from pyafh.afh import AFH


def simple_url_import(afh: AFH, flid: int, url_to_import: str):
    filename = os.path.basename(url_to_import)

    preadd = afh.preadd(flid=flid, filename=filename)
    import_remote = afh.import_remote(fid=preadd['DATA']['fid'], url_to_import=url_to_import)

    afh.add(fid=preadd['DATA']['fid'], flid=flid, filename=filename, file_size=import_remote['file_size'],
            upload_date=import_remote['upload_date'], md5hash=import_remote['md5hash'])

    return f'{afh.URL_BASE}/?fid={preadd["DATA"]["fid"]}'


def run():
    _, flid, url_to_import = sys.argv
    afh = AFH(email=Config.Email, password=Config.Password, proxies=Config.Proxies)

    print(simple_url_import(afh=afh, flid=flid, url_to_import=url_to_import))


if __name__ == '__main__':
    run()
