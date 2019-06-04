# coding: utf-8

import unittest2
loader = unittest2.TestLoader()
tests = loader.discover('test/')
testRunner = unittest2.runner.TextTestRunner()
testRunner.run(tests)
