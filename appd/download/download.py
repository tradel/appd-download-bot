#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
from zone import Zone


def status_callback(src, status):
    if not args.quiet:
        print status + ' . . .',
        sys.stdout.flush()


def success_callback(src):
    if not args.quiet:
        print


def size(nbytes):
    if nbytes >= 1024*1024*1024:
        return '{0:5.1f}GB'.format(float(nbytes) / float(1024*1024*1024))
    if nbytes >= 1024*1024:
        return '{0:5.1f}MB'.format(float(nbytes) / float(1024*1024))
    if nbytes >= 1024:
        return '{0:5d}KB'.format(nbytes / 1024)


def save_callback(src, eargs):
    if not args.quiet:
        pct = int(float(eargs['bytes_read']) / float(eargs['total_bytes']) * 100.0)
        kbps = long(float(eargs['bytes_read']) / (eargs['now_time'] - eargs['start_time']))
        bar = '=' * (pct / 4)

        print '\r{0:<20} [{1:<25}] {2:3d}% | {3:>6} | {4:>6}ps'.format(eargs['filename'], bar, pct,
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
                      required=True,
                      help='Credentials to use for logging into AppDynamics SSO server.')

    argp.add_argument('-p', '--password',
                      required=True,
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

    args = parse_args()
    z = Zone(args.zone, args.version,
             username=args.username, password=args.password, debug=args.debug)

    if args.no_download:
        print z.get_url(args.product, platform=args.os, bits=args.bits, package=args.format)
    else:
        z.download_product(args.product, platform=args.os, bits=args.bits, package=args.format, output=args.output)

    if not args.quiet:
        print 'Done!'

    sys.exit(0)


if __name__ == '__main__':
    main()
