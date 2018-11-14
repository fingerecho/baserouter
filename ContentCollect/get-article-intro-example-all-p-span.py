#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re

#url = "http://www.runoob.com/html/html-editors.html"
#url = "http://www.runoob.com/java/java-polymorphism.html"
#url = "http://www.runoob.com/html/html-tutorial.html"
#url = "http://www.runoob.com/html/html5-canvas.html"
#url = "http://www.runoob.com/html/html5-form-input-types.html"
url = "http://www.runoob.com/vue2/vue-class-style.html"
sess = requests.Session()
res = sess.get(url)
res.encoding = 'utf-8'
html_doc = res.text
soup = BeautifulSoup(html_doc, 'html.parser')
regx = re.compile("实例")
def handle(txt:str,name='default.log'):
	if re.match(regx,txt):
		print(txt)
tar = soup.find_all(id="content")[0]
title = "default"
title = tar.find_all('h1')[0]
title = re.sub(" ","",title.string)
h2s = tar.find_all('h2')
for i in h2s:
	handle(str(i.string),title)
print('title is %s'%title)