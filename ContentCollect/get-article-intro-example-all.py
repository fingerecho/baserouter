#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup


#url = "http://www.runoob.com/html/html-editors.html"
#url = "http://www.runoob.com/java/java-polymorphism.html"
#url = "http://www.runoob.com/html/html-tutorial.html"
#url = "http://www.runoob.com/html/html5-canvas.html"
url = "http://www.runoob.com/html/html5-form-input-types.html"
#url = "http://www.runoob.com/vue2/vue-class-style.html"
sess = requests.Session()
res = sess.get(url)
res.encoding = 'utf-8'
html_doc = res.text
soup = BeautifulSoup(html_doc, 'html.parser')

def handle(txt:str,name='default.log'):
	if name.strip(" ") == "":
		name = "defa"
	with open(name,"a+",encoding="utf-8") as f:
		f.write(txt)

tar = soup.find_all(id="content")[0]
flag = False
title = "default"
for child in tar.children:
	if child.string != None:
		#f.write(child.string)
		if flag==False:
			title=child.string.strip("\n").strip()
			flag==True
			continue
		handle(child.string,title)
	else:
		for cc in child:
			if cc.string != None:
				#f.write(cc.string)
				handle(cc.string,title)
			else:
				#f.write("\r\n..........................\r\n")
				handle("aaaaaaaaaaa",title)
#for cont in tar.contents:
#	if cont.string != None:
#		f.write(cont.string)
