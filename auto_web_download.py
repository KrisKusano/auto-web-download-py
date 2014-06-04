#!python3
# -*- coding: utf-8 -*-
"""
download a file from the web automatically

checks if web file is newer than the local copy, and does not download if the
web file date has not changed

Created on Tue Jun  3 16:05:41 2014

@author: KrisKusano
@email: kusano@vt.edu
"""
import sys
import os
import urllib.request
import urllib.error
import time
import calendar


def ini_log(logpath, URL, dest):
    """create download log with header if it does not exist"""
    if not os.path.exists(logpath):
        with open(logpath, '+w') as f:
            print('File from URL:', URL,
                  'saved to', dest, file=f)
            print('Time', 'Status', sep=',', file=f)


def write_log(logpath, status):
    with open(logpath, '+a') as f:
        print(time.strftime('%a %d %b %Y %H:%M:%S', time.localtime()),
              status,
              sep=',',
              file=f)


def download_file(url, dest_path):
    """download a file from the web and save it to a destination file"""

    # open URL
    try:
        g = urllib.request.urlopen(sys.argv[1])
    except urllib.error.URLError as e:
        print('URL Error: ', e.reason)
        sys.exit()

    # get last-modified/Date from web, convert to unix time
    last_mod = g.headers['last-modified']
    if last_mod is not None:
        web_ctime = time.strptime(last_mod,
                                  '%a, %d %b %Y %H:%M:%S %Z')
    else:
        # try another field
        last_mod = g.headers['Date']
        if last_mod is not None:
            web_ctime = time.strptime(last_mod,
                                      '%a, %d %b %Y %H:%M:%S %Z')
        else:
            # there is no last-modified in the header - use local time instead
            web_ctime = time.localtime()
    web_ctime = calendar.timegm(web_ctime)

    # if file already exists, check created date
    newfile = True  # should we download a new file?
    if os.path.exists(sys.argv[2]):
        orig_stat = os.stat(sys.argv[2])
        if web_ctime <= orig_stat.st_atime:
            # web file is older, no need to replace
            newfile = False
            print('Local file is most recent - exiting')

    # download if necessary, do logging
    logpath = os.path.join(os.path.dirname(dest_path), 'download.log')
    ini_log(logpath, sys.argv[1], sys.argv[2])
    if newfile:
        # download the file and overwrite if exists
        try:
            print('downloading file...')
            with open(sys.argv[2], 'b+w') as f:
                f.write(g.read())
                os.utime(sys.argv[2], times=(web_ctime, web_ctime))
        except OSError as e:
            print('Could not save file "{}": '.format(sys.argv[2]), e.strerror)
            sys.exit()

        write_log(logpath, 'New file downloaded')
    else:
        write_log(logpath, 'Local is most recent - no file downloaded')

    print('done. see log for details')

if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Usage: python3 auto_web_download.py src_url dest_path')
        sys.exit()
    download_file(sys.argv[1], sys.argv[2])
