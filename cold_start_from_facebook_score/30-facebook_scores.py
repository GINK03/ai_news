import requests
import json
from pathlib import Path
from hashlib import sha256
import os
import sys
import time
from datetime import datetime 
import datetime
from datetime import timedelta
import random

def graph_access(url, acc, obj=None):
	query = f'https://graph.facebook.com/?id={url}&fields=og_object{{engagement}},engagement&access_token={acc}'
	r			= requests.get(query)
	try:
		fb_obj	 = json.loads(r.text)
	except Exception as ex:
		print(ex)
		return
	tdatetime = datetime.datetime.now()
	eval_time = tdatetime.strftime('%Y-%m-%d %H:%M:%S')
	
	obj = {} if obj is None else obj
	obj['url']			 = url
	obj[eval_time] = fb_obj
	if fb_obj.get('error'):
		print('error', fb_obj['error']['message'])
		print(fb_obj)
		if 'Cannot specify an empty identifier' == fb_obj['error']['message']:
			path.unlink()
			time.sleep(5.0)
			return
		time.sleep(30.0)
		return
	datum = json.dumps(obj, indent=2, ensure_ascii=False)
	#print(datum) 
	open(f'facebook_score_v2/{url_hash}', 'w').write( datum )

accs = [ line.strip() for line in open('tokens') ]
if '--scan' in sys.argv:
	# make loop
	while True:
		for index, path in enumerate(Path('darturl_clean').glob('*')):
			key = index%len(accs)
			acc = accs[random.randint(0, len(accs)-1)]
			print(acc)
			url		= path.open().read()
			url_hash = sha256(bytes(url,'utf8')).hexdigest() 
			if os.path.exists(f'facebook_score_v2/{url_hash}'):
				obj = json.load(Path(f'facebook_score_v2/{url_hash}').open())
				eval_times = [datetime.datetime.strptime(eval_time, '%Y-%m-%d %H:%M:%S') for eval_time in obj.keys() if eval_time != 'url']
				eval_times = sorted(eval_times) 
				now_datetime = datetime.datetime.now()
				delta_time = now_datetime - eval_times[-1]

				delta_time_head = now_datetime - eval_times[0]	
				print(eval_times, delta_time_head.seconds)
				# 最古のものから48時間以上,古いものはunlinkする
				print(delta_time_head.days)
				if delta_time_head.seconds >= 2: 
					print('remove', url)
					path.unlink()
					#import shutil
					#shutil.move(Path(f'facebook_score_v2/{url_hash}'), f'facebook_score_v2_old/{url_hash}')
					continue
				# 三時間たびにスキャンする
				if delta_time.seconds >= timedelta(seconds=3600 * 3).seconds:
					print('scan', url)
					graph_access(url, acc, obj)
					time.sleep(1.5)
					continue
				continue
			else:
				graph_access(url, acc, None)
				...
			
			time.sleep(1.5)

if '--clean' in sys.argv:
	for path in Path('./facebook_score_v2').glob('*'):
		obj = json.load(path.open())
		if obj.get('error') is not None:
			path.unlink()
		
	
