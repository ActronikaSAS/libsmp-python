#!/usr/bin/python3

import unittest
import pycodestyle
import glob
import sys

tests = unittest.TestLoader().discover('.', '*_test.py')
testRunner = unittest.runner.TextTestRunner(verbosity=2)
ret = not testRunner.run(tests)

python_files = glob.glob("./*.py")
style = pycodestyle.StyleGuide(quiet=False)
result = style.check_files(python_files)

sys.exit(ret + result.total_errors)
