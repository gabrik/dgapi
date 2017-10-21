#!/usr/bin/python

import os
 
virtenv = 'virtual/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.7/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
	execfile(virtualenv, dict(__file__=virtualenv))
except IOError as e:
	print ("Error %s" % e)
 
from dgapi import app as application

application.run()