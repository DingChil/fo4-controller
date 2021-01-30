#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
	import os
	import sys
	import time
	from sina_weibo.crawler import sina_weibo_reptile

except ImportError:
		print >> sys.stderr, """\

There was a problem importing one of the Python modules required.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:

%s

""" % (sys.exc_info(), sys.version)
		sys.exit(1)

__path__ = ""
__delay__ = 0
__depth__ = 0

def initialization():
	relative_path = os.path.dirname(__file__)
	global __path__
	__path__ = os.path.join(relative_path, 'temporary_data')
	global __delay__
	__delay__ = 5
	global __depth__
	__depth__ = 5

def sina_weibo_crawling():
	crawler = sina_weibo_reptile(__path__, __delay__, __depth__)
	sina_weibo_state = crawler.crawling()
	failed_frequency = 1
	while sina_weibo_state == False:
		sina_weibo_state = crawler.crawling()
		failed_frequency += 1
		if failed_frequency >= 10:
			break
		time.sleep(__delay__)

def get_time():
	now_time = time.localtime()
	start_time = str(now_time[0]) + "/" + str(now_time[1]) + "/" + str(now_time[2]) + "  " + str(now_time[3]) + ":" + str(now_time[4]) + ":" + str(now_time[5])
	return start_time

if __name__ == '__main__':
	initialization()
	sina_weibo_crawling()
	sys.exit(0)