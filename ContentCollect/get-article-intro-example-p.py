#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup


#url = "http://www.runoob.com/html/html-editors.html"
url = "http://www.runoob.com/java/java-polymorphism.html"
sess = requests.Session()
res = sess.get(url)
res.encoding = 'utf-8'
html_doc = res.text
soup = BeautifulSoup(html_doc, 'html.parser')
# result  = soup.find_all(href=re.compile("elsie"), id='xiaodeng')
article = soup.find_all(class_= "article-intro",id="content")
title = article[0].find_all("h1")
ps = article[0].find_all("p")

print(title[0].text)
print(ps[0].text)