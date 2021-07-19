from contextlib import nullcontext
from os import system
from time import process_time, process_time_ns, sleep, time
from typing import Counter
import requests
import re
from fake_useragent import UserAgent
import random
import time
from pathlib import Path
from requests.sessions import session, to_key_val_list
import fitz
import glob
url = input('请输入要获取的资料地址（原创力文档）：')
total = []
def Response(url):
	return requests.session().get(url,headers={'user-agent':UserAgent().random})
session = Response(url)
content = session.text
aid = re.findall('(?<=aid: )\d+', content)[1]
t = re.findall('(?<=senddate: \\\')\w+', content)[0]
title = re.findall(r'(?<=title: \').*(?=\')', content)[0]
view_token = re.findall(r'(?<=view_token: \').*(?=\')', content)[0]
actual_page = re.findall(r'(?<=actual_page: )\d+', content)[0]
preview_page = re.findall(r'(?<=preview_page: )\d+', content)[0]
print('请等候，预计需要'+str(int(preview_page)*2)+'秒.....')
for pn in range(1, int(preview_page)+1, 6):
	if(int(preview_page)-pn < 6):
		pn = int(preview_page)
	httpurl = 'https://openapi.book118.com/getPreview.html?&project_id=1&aid={0}&t={1}&view_token={2}&page={3}&	callback=jQuery183015317846379791566_1626347504605&_=1626347506997'.format(str(aid), str(t), str(view_token), str(pn))
	fileResponse = requests.session().get(httpurl).text
	imgurl1 = re.findall(r'(?<="\d{1}":")(.*?)(?=")', fileResponse)
	imgurl2 = re.findall(r'(?<="\d{2}":")(.*?)(?=")', fileResponse)
	if len(imgurl1) == 0:
	    total.append(imgurl2)
	elif len(imgurl2) == 0:
	    total.append(imgurl1)
	else:
		total.append(imgurl1)
		total.append(imgurl2)
	time.sleep(2)
dir = r'C:\Users\X\Desktop\新建文件夹\pyimg\{0}'.format(str(title).split('.')[0])
pdfdir=dir+r'\{0}.pdf'.format(str(title))
m=1
p = Path(dir)
try:
	p.mkdir()
	for i in total:
		for j in i:
				imgurl = re.sub(r'\\', '', str(j))
				response = requests.session().get('https:'+imgurl).content
				with open(dir+'\\'+str(m)+'.png', 'wb') as f:
						f.write(response)
				print('第'+str(m)+'张图片已获取！')
				m = m+1
except FileExistsError as e:
	print(e)
system('pause')
