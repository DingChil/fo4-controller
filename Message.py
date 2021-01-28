#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Author: DingChil
'''

try:
	import sys
	import os
	import re
	import time
	import codecs
	import socket
	import urllib.request
	from urllib.error import URLError, HTTPError

except ImportError:
		print(sys.stderr, """

There was a problem importing one of the Python modules required.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:

%s

""" % (sys.exc_info(), sys.version))
		sys.exit(1)

NOW = ""
TARGET = {}
STATE = {}
PATH = ""
HEADER = {}
DELEY = 0
FORE = ""
BACK = ""

def init_arg():
	global TARGET, PATH, STATE, DELEY, HEADER, NOW, FORE, BACK
	get_time()
	print (u"启动时间: " + NOW)
	HEADER = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	DELEY = 0
	FORE = 'osascript -e \'display notification "「'
	BACK = '」 有了最新的动态~" with title "通知" subtitle "根据 上次发表时间" sound name "Sound Name"\''
	print (u"报头延时、终端命令设置完毕，变量初始化完毕！\n")

def get_time():
	global NOW
	now_all = time.localtime()
	now_hour = str(now_all[3])
	now_min = str(now_all[4])
	now_day = str(now_all[0]) + "-" + str(now_all[1]) + "-" + str(now_all[2])
	num_min = int(now_min)
	num_hour = int(now_hour)
	if num_min == 0:
		num_hour = num_hour - 1
		num_min = 59
	else :
		num_min = num_min - 1
	now_min = str(num_min)
	now_hour = str(num_hour)
	if len(now_hour) == 1:
		now_hour = "0" + now_hour
	if len(now_min) == 1:
		now_min = "0" + now_min
	NOW = now_day + " " + now_hour + ":" + now_min

def start_run():
	global NOW, TARGET, FORE, BACK
	for keyword in TARGET:
		website = TARGET[keyword]
		print (u"现在执行的页面是 " + keyword + u" 的主页\n具体地址：" + website)
		if grab_web(website):
			if contrast_time(keyword, handle_data()):
				com_message = FORE + keyword + BACK
				print (com_message)
				os.system(com_message)
		print ("本页执行结束，此刻时间为：" + NOW)
		time.sleep(DELEY)

def grab_web(tar_url):
	global PATH, HEADER
	try:
		tar_req = urllib.request.Request(tar_url, headers = HEADER)
		tar_res = urllib.request.urlopen(tar_req).read()
		unicode_data = tar_res.decode('gbk')
	except HTTPError as e:
		print (u"发生网络错误，跳过此次执行。错误代码：" + str(e.code))
		return False
	except URLError as e:
		if hasattr(e, 'reason'):
			print(u"无法连接服务器，跳过此次执行。错误说明：" + str(e.reason))
			return False
		elif hasattr(e, 'code'):
			print(u"服务器无法完成请求，跳过此次执行。错误代码：" + str(e.code))
			return False
		else:
			print(u"发生未知错误，跳过此次执行。")
			return False
	except socket.error as e:
		print (u"发生socket错误，跳过此次执行，错误代码：" + str(e.code))
		return False
	except socket.timeout:
		print(u"发生socket超时错误，跳过此次执行。")
		return False
	else:
		with codecs.open(PATH, 'w', 'utf-8') as write_file:
			write_file.write(unicode_data)
		return True

def handle_data():
	global PATH
	with codecs.open(PATH, 'r', 'utf-8') as read_file:
		data = read_file.read()
	ext_publish = re.compile('<li>上次发表时间: (.*?)</li>')
	pub_time = ext_publish.findall(data)
	print ("本次获取到的最新发表时间为: " + pub_time[0])
	return pub_time[0]

def contrast_time(tar_name, latest_time):
	global NOW
	get_time()
	if latest_time == NOW:
		if STATE[tar_name] != latest_time:
			STATE[tar_name] = latest_time
			return True
		else:
			return False
	else:
		return False

if __name__ == '__main__':
	global DELEY, STATE
	init_arg()
	while True:
		start_run()
		for fcous_id in STATE:
			str_result = fcous_id + u" : " + STATE[fcous_id]
			print (str_result.rjust(43))
		print (u"\n本轮执行结束，准备延迟" + str(DELEY) + u"秒。\n")
		time.sleep(DELEY)
	sys.exit(0)