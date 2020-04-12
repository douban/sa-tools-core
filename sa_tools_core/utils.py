# coding: utf-8

from __future__ import print_function

import os
import sys
import six
import pwd
import socket
import binascii
import importlib
from functools import wraps

from sa_tools_core.consts import CONFIG_DIR

HOSTS_FILE = '/etc/hosts'
HOSTS_WAN_FILE = '/etc/hosts.wan'

ip_hostname_cache = {}


def get_os_username():
    return pwd.getpwuid(os.getuid()).pw_name


def get_config(config_name):
    try:
        with open(os.path.join(CONFIG_DIR, config_name)) as f:
            config = f.read()
    except IOError as e:
        if e.errno == 2:
            print('Error: get config failed, you shall not execute this program on this machine!', file=sys.stderr)
            sys.exit(1)
        raise
    return config.strip()


def resolve_hostname(hostname):
    return socket.gethostbyname(hostname)


def resolve_ip(ip):
    from sh import grep

    if ip_hostname_cache.get(ip):
        return ip_hostname_cache[ip]
    hostname = ip
    # tricky
    if ip.startswith('192.') or ip.startswith('10.'):
        hosts_files = (HOSTS_FILE,)
    else:
        hosts_files = (HOSTS_WAN_FILE,)
    for hosts_file in hosts_files:
        try:
            out = grep('^[^#]*%s[^0-9]' % ip, hosts_file, E=True)
            if out:
                hostname = out.split()[-1]
                break
        except Exception:
            pass
    ip_hostname_cache[ip] = hostname
    return hostname


def reverse_func(f):
    """ reverse function Boolean result """
    @wraps(f)
    def wrapper(*args, **kwargs):
        return not f(*args, **kwargs)

    return wrapper


def ipv6_addr_to_tinydns_generic(ipv6_addr):
    rdata = ''
    hexlify_ipv6_addr = binascii.hexlify(socket.inet_pton(socket.AF_INET6, ipv6_addr))
    split_hexlify_ipv6_addr = [hexlify_ipv6_addr[i:i + 2] for i in range(0, len(hexlify_ipv6_addr), 2)]
    for part in split_hexlify_ipv6_addr:
        rdata += '\\%03o' % int(part, 16)
    return rdata


def to_unicode(s, encoding='utf-8', errors='strict'):
    return six.ensure_text(s, encoding=encoding, errors=errors)


def to_str(s, encoding='utf-8', errors='strict'):
    '''
    in python2, convert s to str if s is unicode
    in python3, convert s to str if s is bytes
    '''
    return six.ensure_str(s, encoding=encoding, errors=errors)


def output(*args, **kw):
    '''
    try to output as UTF-8 encoding strings, to a terminal or a file
    '''
    print(*[to_str(a) for a in args], **kw)


def prompt_input(prompt=None):
    six.moves.input(prompt)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)

    def __getattr__(self, attr):
        return self.get(attr, self.get('_default_value'))

    def __setattr__(self, attr, value):
        self[attr] = value


def props(cls):
    return [i for i in cls.__dict__ if not i.startswith('_')]


def i2ip(i):
    i = int(i)
    return '%s.%s.%s.%s' % ((i >> 24) % 256, (i >> 16) % 256, (i >> 8) % 256, i % 256)


def import_string(s):
    mod, attr = s.split(':')
    mod = importlib.import_module(mod)
    return getattr(mod, attr) if attr else mod
