# coding: utf-8

import shlex
import importlib

from sa_tools_core.libs.process import Process


class Client(Process):
    def __init__(self, cmds=None, func=None):
        super(Client, self).__init__(cmds)
        self.func = func

    def __str__(self):
        if self.func:
            func_str = '%s:%s' % (self.func.__module__, self.func.__name__)
        else:
            func_str = 'None'
        return '%s(cmds=%s, func=%s)' % (self.__class__.__name__, self.cmds, func_str)

    __repr__ = __str__

    def __getattr__(self, name):
        if not self.func:
            mod = importlib.import_module('sa_tools_core.%s' % name)
            return self.__class__(func=mod.main)

        return super(Client, self).__getattr__(name)

    def bake(self, *a, **kw):
        cmds = list(self.cmds)
        proc = Client(cmds, self.func)
        proc._parse_args(*a, **kw)
        return proc

    def call(self, cmdstr='', env=None):
        extra_cmds = shlex.split(cmdstr)
        return self.func(self.cmds + extra_cmds)


if __name__ == '__main__':
    c = Client()
    print(c.notify(wework='user1', content='hehe'))
    print(c.uptime())
    print(c.notify.test)
    print(c.dns.list(S='@'))
