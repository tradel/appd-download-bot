#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import time
import getpass
import os
import sys

from zone import Zone
from term import get_terminal_size

MAX_FILENAME_WIDTH = 32
last_time = time.time()
term_width = 80


def size(nbytes):
    """
    Converts a raw file size to a human-readable representation, e.g.:
    >>> size(1024 * 1024 * 4)
    '  4.0MB'
    >>> size(1024 * 1024 * 1024 * 3.5)
    '  3.5GB'
    :param nbytes: raw file size in bytes
    :type nbytes: long
    :return: formatted file size
    :rtype: str
    """
    if nbytes >= 1024 * 1024 * 1024:
        return '{0:5.1f}GB'.format(float(nbytes) / float(1024 * 1024 * 1024))
    if nbytes >= 1024 * 1024:
        return '{0:5.1f}MB'.format(float(nbytes) / float(1024 * 1024))
    if nbytes >= 1024:
        return '{0:5d}KB'.format(nbytes / 1024)


# noinspection PyUnusedLocal
def status_callback(src, status):
    if not args.quiet:
        print status + ' . . .',
        sys.stdout.flush()


# noinspection PyUnusedLocal
def success_callback(src):
    if not args.quiet:
        print


# noinspection PyUnusedLocal
def save_callback(src, eargs):
    if not args.quiet:
        pct = int(float(eargs['bytes_read']) / float(eargs['total_bytes']) * 100.0)
        kbps = long(float(eargs['bytes_read']) / (eargs['now_time'] - eargs['start_time']))

        global last_time
        if eargs['now_time'] - last_time < 1.0 and eargs['bytes_read'] < eargs['total_bytes']:
            return
        last_time = eargs['now_time']

        fname_width = (term_width - (4 + 4 + 3 + 8 + 3 + 7 + 2)) / 2
        bar_width = fname_width
        if fname_width > MAX_FILENAME_WIDTH:
            bar_width += fname_width - MAX_FILENAME_WIDTH
            fname_width = MAX_FILENAME_WIDTH

        bar = '=' * (pct * bar_width / 100)

        fmt_string = '\r{0:<' + str(fname_width) + '.' + str(fname_width) + '} ' +\
                     '[{1:<' + str(bar_width) + '.' + str(bar_width) + '}] {2:3d}% | {3:>8} | {4:>.7}ps'

        print fmt_string.format(eargs['filename'], bar, pct,
                                size(eargs['bytes_read']), size(kbps)),

        sys.stdout.flush()

    if eargs['bytes_read'] == eargs['total_bytes']:
        if not args.quiet:
            print
        print '{0} saved to {1}'.format(eargs['filename'], eargs['target'])


def parse_args():
    argp = argparse.ArgumentParser()

    # boolean flags
    argp.add_argument('-q', '--quiet',
                      action='store_true',
                      help='Skip display of progress and status.')

    argp.add_argument('-d', '--debug',
                      action='store_true',
                      help='Display debugging information about HTTP connections, cookies, etc.')

    argp.add_argument('-n', '--no-download',
                      action='store_true',
                      dest='no_download',
                      help='Don\'t download the file, just display the actions to be taken.')

    # authentication arguments
    argp.add_argument('-u', '--username',
                      help='Credentials to use for logging into AppDynamics SSO server.')

    argp.add_argument('-p', '--password',
                      help='Password for SSO login.')

    # platform arguments
    argp.add_argument('-b', '--bits',
                      type=int,
                      choices=[32, 64],
                      default=64,
                      help='Request 32-bit or 64-bit version of the product. Defaults to 64-bit.')

    argp.add_argument('-s', '--os',
                      choices=['linux', 'windows', 'mac'],
                      help='Operating system platform.')

    argp.add_argument('-f', '--format',
                      choices=['tar', 'rpm'],
                      default='tar',
                      help='Packaging format for downloads.')

    # file selection arguments
    argp.add_argument('-z', '--zone',
                      choices=['saas', 'on-premise'],
                      default='on-premise',
                      help='Specify the download zone. Currently this script only supports the "saas" and ' +
                           '"on-premise" zones.')

    argp.add_argument('-v', '--version',
                      default='latest',
                      help='Product version to download. Default: latest version available.')

    # output arguments
    argp.add_argument('-o', '--output',
                      default='.',
                      help='Path to save downloaded file. If the target is a directory, the original filename ' +
                           'will be appended.')

    # positional arguments
    argp.add_argument('product',
                      choices=Zone.PRODUCTS,
                      help='Product to be downloaded.')

    return argp.parse_args()


def main():
    Zone.status += status_callback
    Zone.success += success_callback
    Zone.download_progress += save_callback

    global term_width
    term_width = get_terminal_size()[0]

    global args
    args = parse_args()

    username = args.username
    if not username:
        if 'APPD_SSO_USERNAME' in os.environ:
            username = os.environ['APPD_SSO_USERNAME']
        else:
            print 'Username: ',
            username = sys.stdin.readline().strip()

    password = args.password
    if not password:
        if 'APPD_SSO_PASSWORD' in os.environ:
            password = os.environ['APPD_SSO_PASSWORD']
        else:
            password = getpass.getpass()

    z = Zone(args.zone, args.version,
             username=username, password=password, debug=args.debug)

    if args.no_download:
        print z.get_url(args.product, platform=args.os, bits=args.bits, package=args.format)
    else:
        z.download_product(args.product, platform=args.os, bits=args.bits, package=args.format, output=args.output)

    if not args.quiet:
        print 'Done!'

    sys.exit(0)


if __name__ == '__main__':
    main()
