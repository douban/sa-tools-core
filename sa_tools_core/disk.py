# coding: utf-8

from __future__ import print_function

import os
import re
import json
import fcntl
import logging
import datetime
import argparse

import humanize

from sa_tools_core.libs.permission import require_sa
from sa_tools_core.libs.process import process
from sa_tools_core.libs.ncdu import top_huge_dirs_from_ncdu
from sa_tools_core.utils import get_os_username, to_str, prompt_input
from sa_tools_core.consts import NCDU_EXPORT_DATA_PATH, NCDU_JOB_LOCK_PREFIX

logger = logging.getLogger(__name__)
RE_TIMESTRING = re.compile(r'\d{14}')  # e.g. 20160512153302
DEFAULT_CHECK_PATH = '/'
DATA_STALE_THRESHOLD = datetime.timedelta(hours=1)

NCDU_JOB_LOCK_PATTREN = NCDU_JOB_LOCK_PREFIX + '-{escped_check_path}'


def check_disk(args):
    data_path_avail_cmd = 'df -BM %s' % args.ncdu_data_path
    res = process.call(data_path_avail_cmd)
    stdout, stderr = res['stdout'], res['stderr']
    if stderr:
        raise RuntimeError(stderr)
    else:
        avail = int(stdout.split()[10].strip('M'))
        if avail < 50:
            raise RuntimeError("Not enough space(<50M) for storing datafile on %s, "
                               "disk usage scanning stopped." % args.ncdu_data_path)
        else:
            lock_file = NCDU_JOB_LOCK_PATTREN.format(escped_check_path=args.escaped_check_path)
            job_lock = open(lock_file, 'w')
            try:
                fcntl.flock(job_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                logger.exception("sa-disk check job already in running.")
            else:
                job_lock.close()
                time_now_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                data_file_path = os.path.join(args.ncdu_data_path,
                                              'ncdu-export-%s-%s.gz' % (args.escaped_check_path,
                                                                        time_now_string))
                args.data_file = data_file_path
                with open(data_file_path, 'w'):
                    pass
                check_disk_cmd = ('/usr/bin/flock -n %s ncdu -0xo- %s'
                                  ' | gzip >%s'
                                  % (lock_file, args.check_path, data_file_path))
                logger.debug('Running: %s', check_disk_cmd)
                p = process.call(check_disk_cmd, nonblock=True, shell=True)
                logger.info("Checking %s using ncdu, and exporting datafile %s on background"
                            % (args.check_path, data_file_path))

                if args.block:
                    p.wait()
                    read_data(args)


def read_data(args):
    data_file_path = args.data_file
    read_log_cmd = 'zcat %s | ncdu -f-' % data_file_path  # Security Problem
    if not args.topn:
        logger.info("About to open ncdu ui, read datafile %s" % data_file_path)
        prompt_input("Press any key to continue...")
        process.call(read_log_cmd, shell=True)
    if args.topn:
        logger.info("About to calc top %d huge items in depth %s." % (args.topn, args.max_depth))
        stdout = process.call('zcat %s' % data_file_path)['stdout']
        rawfscontent = json.loads(to_str(stdout, errors='ignore'))[3]
        logger.debug('calc top_huge_dirs_from_ncdu...')
        ret = top_huge_dirs_from_ncdu(args.topn, rawfscontent, max_depth=args.max_depth)
        logger.debug('done top_huge_dirs_from_ncdu')

        print("Top %d huge items in depth %s:" % (args.topn, args.max_depth))
        for k, v in sorted(ret.items(), key=lambda kv: kv[1], reverse=True):
            humanize_size = humanize.naturalsize(v, binary=True)
            print('%s  %s' % (humanize_size, k))


def escape_path(path):
    return os.path.abspath(path).replace('/', '%')


def find_latest_exported_data(args):
    logger.info('Finding lastest ncdu exported data file from %s' % args.ncdu_data_path)
    find_latest_cmd = "ls -lt %s | grep ncdu-export-%s-" % (args.ncdu_data_path,
                                                            args.escaped_check_path)
    res = process.call(find_latest_cmd, shell=True)
    stdout, stderr = res['stdout'], res['stderr']
    if stderr:
        raise RuntimeError(stderr)
    elif not stdout:
        return None
    else:
        latest_file_name = stdout.splitlines()[0].split()[-1]
        data_file = os.path.join(args.ncdu_data_path, latest_file_name)
        logger.info('Found ncdu exported data file %s' % data_file)

        data_file_timestring = RE_TIMESTRING.findall(data_file)[0]
        data_file_timestamp = datetime.datetime.strptime(data_file_timestring, "%Y%m%d%H%M%S")
        if (not args.force_read
                and data_file_timestamp <= datetime.datetime.now() - DATA_STALE_THRESHOLD):
            logger.warning("But data file is out of date.")
            return None
        return data_file


def select_ncdu_data_path(args):
    for p in (NCDU_EXPORT_DATA_PATH, '/data', '/'):
        if os.path.isdir(p):
            args.ncdu_data_path = p
            return


@require_sa
def clean(args):
    """clean disk, including outdated ncdu exported data file"""
    select_ncdu_data_path(args)
    if not args.ncdu_data_path:
        logger.error('select_ncdu_data_path failed: no ncdu_data_path selected')
        return
    cmd = ("find -L %s -maxdepth 1 -type f -name 'ncdu-export-*' -mtime +1 -delete"
           % args.ncdu_data_path)
    if args.debug:
        logger.debug('execute %s', cmd)
    res = process.call(cmd, shell=True)
    stdout, stderr = res['stdout'], res['stderr']
    if stdout:
        print(stdout)
    if stderr:
        logger.error('find command got stderr: %s', stderr)


@require_sa
def usage(args):
    """
    若没有指定 -p,--ncdu-data-path 则自动选择一个 path
    若指定 -f,--force-check 则进行强制进行 check
    若指定 -r,--data-file 则读指定的 ncdu exported data 文件；反之，自动选择最近的 data 文件，若找不到 1 个小时内的文件，则依然会进行 check
    若指定 -R 则不会进行 check
    """
    args.escaped_check_path = escape_path(args.check_path)
    if not args.ncdu_data_path:
        select_ncdu_data_path(args)
    if args.force_check:
        check_disk(args)
    else:
        if not args.data_file:
            args.data_file = find_latest_exported_data(args)

        if not args.data_file:
            if args.force_read:
                logger.warning("No data file found.")
            else:
                logger.warning("Recent data file not found. Checking disk usage.")
                check_disk(args)
        else:
            read_data(args)


def main():
    """
    e.g.
    sa-disk usage
    sa-disk usage -n 5 -d 3
    sa-disk usage -r /data1/ncdu-export-%-20160513142844.gz
    sa-disk usage -c /tmp
    sa-disk usage -p /data
    sa-disk usage --force-check

    sa-disk clean
    """
    parser = argparse.ArgumentParser(epilog=main.__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-u', '--user', help='LDAP username, use your OS user name by default.')
    parser.add_argument('--debug', action='store_true', help='debug.')

    # compatible with py2 & 3
    subparsers = parser.add_subparsers(help='Sub commands', dest='subparser')
    subparsers.required = True

    usage_parser = subparsers.add_parser('usage', help='Disk usage operation.')
    usage_parser.add_argument('-p', '--ncdu-data-path', help='Path to store ncdu exported data',
                              default=None)
    usage_parser.add_argument('-r', '--data-file', metavar='DATA_FILE',
                              help='Read ncdu export data file.')
    usage_parser.add_argument('-n', '--topn', type=int, nargs='?',
                              help='Specify top N huge files for output.', const=5)
    usage_parser.add_argument('-d', '--max-depth', type=int,
                              help='Max path depth to calc top N.', default=3)
    usage_parser.add_argument('-c', '--check-path', metavar='CHECK_PATH',
                              help='Check disk and export ncdu data file.',
                              default=DEFAULT_CHECK_PATH)
    usage_parser.add_argument('-f', '--force-check', action='store_true',
                              help='force check, do not use existing exported file')
    usage_parser.add_argument('-R', '--force-read', action='store_true',
                              help='force read latest exported data file, do not check')
    usage_parser.add_argument('-b', '--block', action='store_true',
                              help='disk usage check block mode.')
    usage_parser.set_defaults(func=usage)

    clean_parser = subparsers.add_parser('clean', help='Clean disk, including outdated ncdu '
                                                       'exported data file.')
    clean_parser.set_defaults(func=clean)

    args = parser.parse_args()
    args.user = args.user or get_os_username()

    log_level = logging.DEBUG if args.debug else logging.INFO
    # logger.setLevel(log_level)
    # ch = logging.StreamHandler()
    # ch.setLevel(log_level)
    # formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    # ch.setFormatter(formatter)
    # logger.addHandler(ch)

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(name)s %(levelname)s %(message)s')

    args.func(args)
