#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re
from jinja2 import Environment, PackageLoader
import os
import json
import threading
import multiprocessing
import math
import sys


THREADS = 2
CPUS = 4
TESTRANG = 6


class HtmlDocStr(object):
	help_ = ""
	code = ""
	def __init__(self,help_,code=""):
		self.code = code
		self.help = help_
		pass
	def update_help(self,new_help):
		self.help_ = self.help_ + new_help
		pass
	def set_code(self,code):
		self.code = code
		pass
	pass
class Handler(object):
	url = ''#"http://www.runoob.com/bootstrap/bootstrap-responsive-utilities.html"
	htmldocs = []
	codes = []
	title = ""
	env = None
	template = None
	sess = None
	count_demo_ = 0
	tar = None
	def __init__(self,url,title,env,template):
		self.url = url
		self.sess = requests.Session()
		self.res = self.sess.get(url)
		self.res.encoding = 'utf-8'
		self.html_doc = self.res.text
		self.env = env
		self.title = title
		self.template = template
		self.soup = BeautifulSoup(self.html_doc, 'html.parser');print("soup init")
		if self._init_tar() != None:
			#self._hand_title_();print("_hand_title_")
			self._hand_codes_();print("_hand_codes_")
			self._hand_help_();print("_hand_help_")
			self._hand_generate_temp_();print("_hand_generate_temp_")
	def _init_tar(self):
		self.tar = self.soup.find_all(id="content")
		if self.tar != None:
			self.tar = self.tar[0]
			return True
		else:
			print("self.tar is None")
			return None
	def _hand_title_(self):
		if len(self.tar.find_all('h1')) == 0:
			ll = self.url.split("/")
			self.title = ll[len(ll)-1].strip().strip(".html").strip(".htm")
		else:
			self.title = self.tar.find_all('h1')[0].string.strip(" ")
			self.title = re.sub(re.compile(" "),"",self.title)
	def _hand_codes_(self):
		name_reg = re.compile("菜鸟教程")
		lt_reg = re.compile("<")
		gt_reg = re.compile(">")
		examples = self.soup.find_all(class_="example")
		for exam in examples:
			example_codes = exam.find_all(class_="example_code")
			for excode in example_codes:
				example_title = excode.find_all('h2')[0].string if len(excode.find_all('h2'))>0 else 'default.title'
				spans = excode.find_all('span')
				tarspan =""
				for span in spans:
					xstr = re.sub(name_reg,"元路由",str(span.string))
					xstr = re.sub(lt_reg,"&lt;",xstr)
					xstr = re.sub(gt_reg,"&gt;",xstr)
					tarspan = tarspan + xstr
				self.codes.append(tarspan)
		pass
	def handle_s(self,txt:str):
		if self.count_demo_ >= len(self.codes):
			return 
		regx = re.compile("实例")
		if re.match(regx,txt):
			xx = self.codes[self.count_demo_]
			self.htmldocs[len(self.htmldocs)-1].set_code(xx)
			self.count_demo_ = self.count_demo_ + 1
			self.htmldocs.append(HtmlDocStr(help_=""))	
		else:
			self.htmldocs[len(self.htmldocs)-1].update_help(txt)
		pass

	def _hand_help_(self):			
		self.htmldocs.append(HtmlDocStr(help_=""))
		count_demo_ = 0
		h2s = self.tar.find_all('h2')
		for i in h2s:
			self.handle_s(str(i.string))
		pps = self.tar.find_all('p')
		for i in pps:
			self.handle_s(str(i.string))
		pass
	def _hand_generate_temp_(self):
		content = self.template.render(htmldocs=self.htmldocs)
		path_ = os.path.join('contents',self.title+".htm")
		print("start write")
		with open(path_,"a+",encoding="utf-8") as f:
 			f.write(content)

class PageHand(object):
	def __init__(self,urls):
		envi = Environment(loader=PackageLoader('testmodule'))
		temp = envi.get_template('demo.htm')
		self.urls = urls
		for url in self.urls:
			Handler(url=url,env=envi,template=temp)

class UrlCollec(object):
	soup = None
	sess = None
	urlinfo = []
	ttile = ""
	def __init__(self,home,did):
		self.sess = requests.Session();print("start run home %s"%home)
		res = self.sess.get(home)
		self.ttile = home.split("/")[1].strip()
		res.encoding = "utf-8"
		self.html_doc = res.text
		self.soup = BeautifulSoup(self.html_doc, 'html.parser')
		urltars = self.soup.find_all(id="leftcolumn")
		#print(True if len(urltars)>0 else False)
		for tar in urltars:
			a = tar.find_all("a")
			for ai in a:
				tittlle = ai.text;print(ai['href'])
				self.urlinfo.append({"href":"http://www.runoob.com"+ai['href'],"title":tittlle})
		self.__write_in_json_(self.ttile,did)
	def __write_in_json_(self,title,did):
		fp = open("urlinfojsons-%s-%s.json"%(title,did),"a+",encoding="utf-8")
		json.dump(self.urlinfo,fp)
		fp.close()
origin =[
{'href':"http://www.runoob.com/html/html-tutorial.html","id":"0"},
{'href':"http://www.runoob.com/html/html5-intro.html","id":"1"},
{'href':'http://www.runoob.com/css/css-tutorial.html','id':'2'},
{'href':"http://www.runoob.com/css3/css3-tutorial.html","id":"3"},
{'href':"http://www.runoob.com/bootstrap/bootstrap-tutorial.html","id":"4"},
{'href':"http://www.runoob.com/bootstrap4/bootstrap4-tutorial.html","id":"5"},
{'href':'http://www.runoob.com/font-awesome/fontawesome-tutorial.html','id':"6"},
{'href':'http://www.runoob.com/foundation/foundation-tutorial.html','id':"7"},
{'href':'http://www.runoob.com/js/js-tutorial.html','id':"8"},
{'href':'http://www.runoob.com/htmldom/htmldom-tutorial.html','id':"9"},
{'href':'http://www.runoob.com/jquery/jquery-tutorial.html','id':"10"},
{'href':'http://www.runoob.com/angularjs/angularjs-tutorial.html','id':'11'},
{'href':'http://www.runoob.com/angularjs2/angularjs2-tutorial.html','id':'12'},
{'href':'http://www.runoob.com/vue2/vue-tutorial.html','id':'13'},
{'href':'http://www.runoob.com/react/react-tutorial.html','id':'14'},
{'href':'http://www.runoob.com/jqueryui/jqueryui-tutorial.html','id':'15'},
{'href':'http://www.runoob.com/nodejs/nodejs-tutorial.html','id':'16'},
{'href':'http://www.runoob.com/ajax/ajax-tutorial.html','id':'17'},
{'href':'http://www.runoob.com/json/json-tutorial.html','id':'18'},
{'href':'http://www.runoob.com/highcharts/highcharts-tutorial.html','id':'19'},
{'href':'http://www.runoob.com/googleapi/google-maps-basic.html','id':'19'},
{'href':'http://www.runoob.com/python/python-tutorial.html','id':'20'},
{'href':'http://www.runoob.com/python3/python3-tutorial.html','id':'21'},
{'href':'http://www.runoob.com/django/django-tutorial.html','id':'22'},
{'href':'http://www.runoob.com/linux/linux-tutorial.html','id':'23'},
{'href':'http://www.runoob.com/docker/docker-tutorial.html','id':'24'},
{'href':'http://www.runoob.com/ruby/ruby-tutorial.html','id':'25'},
{'href':'http://www.runoob.com/java/java-tutorial.html','id':'26'},
{'href':'http://www.runoob.com/cprogramming/c-tutorial.html','id':'27'},
{'href':'http://www.runoob.com/cplusplus/cpp-tutorial.html','id':'28'},
{'href':'http://www.runoob.com/perl/perl-tutorial.html','id':'28'},
{'href':'http://www.runoob.com/servlet/servlet-tutorial.html','id':'29'},
{'href':'http://www.runoob.com/jsp/jsp-tutorial.html','id':'30'},
{'href':'http://www.runoob.com/lua/lua-tutorial.html','id':'31'},
{'href':'http://www.runoob.com/scala/scala-tutorial.html','id':'32'},
{'href':'http://www.runoob.com/go/go-tutorial.html','id':'33'},
{'href':'http://www.runoob.com/regexp/regexp-tutorial.html','id':'34'},
{'href':'http://www.runoob.com/numpy/numpy-tutorial.html','id':'35'},
{'href':'http://www.runoob.com/asp/asp-tutorial.html','id':'36'},
{'href':'http://www.runoob.com/vbscript/vbscript-tutorial.html','id':'36'},
{'href':'http://www.runoob.com/sql/sql-tutorial.html','id':'37'},
{'href':'http://www.runoob.com/mysql/mysql-tutorial.html','id':'38'},
{'href':'http://www.runoob.com/sqlite/sqlite-tutorial.html','id':'39'},
{'href':'http://www.runoob.com/mongodb/mongodb-tutorial.html','id':'40'},
{'href':'http://www.runoob.com/redis/redis-tutorial.html','id':'41'},
{'href':'http://www.runoob.com/Memcached/Memcached-tutorial.html','id':'42'},
{'href':'http://www.runoob.com/jquerymobile/jquerymobile-tutorial.html','id':'43'},
{'href':'http://www.runoob.com/xml/xml-tutorial.html','id':'44'},
{'href':'http://www.runoob.com/dtd/dtd-tutorial.html','id':'45'},
{'href':'http://www.runoob.com/dom/dom-tutorial.html','id':'46'},
{'href':'http://www.runoob.com/xsl/xsl-tutorial.html',"id":'47'},
{'href':'http://www.runoob.com/xpath/xpath-tutorial.html',"id":'48'},
{'href':'http://www.runoob.com/xquery/xquery-tutorial.html',"id":'49'},
{'href':'http://www.runoob.com/xlink/xlink-tutorial.html','id':'50'},
{'href':'http://www.runoob.com/svg/svg-tutorial.html','id':'51'},
{'href':'http://www.runoob.com/aspnet/mvc-intro.html','id':'52'},
{'href':'http://www.runoob.com/webservices/webservices-tutorial.html','id':'53'},
{'href':'http://www.runoob.com/git/git-tutorial.html','id':'54'},
{'href':'http://www.runoob.com/svn/svn-tutorial.html',"id":"55"},
{'href':'http://www.runoob.com/http/http-tutorial.html',"id":"56"},
{'href':'http://www.runoob.com/browsers/browser-information.html',"id":"56"},
{'href':'http://www.runoob.com/tcpip/tcpip-tutorial.html','id':'57'},
{'href':'http://www.runoob.com/w3c/w3c-tutorial.html','id':'58'},
]
class HandTempLL(object):
	test = False
	objs = None
	def __init__(self,test):
		self.test = test
		try:
			if self.test:
				for i in range(TESTRANG):
					af="urlinfojsons--%s.json"%(str(i))
					f = open(af,"r",encoding="utf-8")
					#self.objs = json.load(f,encoding="utf-8")
					temp = json.load(f,encoding="utf-8")
					print("hello")
					f.close()
		except Exception as e:
			print(e)
		#self.showResult()
	def showResult(self):
		for i in objs:
			print(i['href'])
			print(i['title'])

class HandALL(threading.Thread):
	test = False
	start_ = 0
	end_ = 0
	def __init__(self,start_,end_,test=False):
		threading.Thread.__init__(self)
		self.test = test
		self.start_ = start_
		self.end_= end_
	def run(self):
		global origin
		ind = 0
		for ori in origin[self.start_:self.end_]:
			UrlCollec(ori['href'],ori['id'])
			if self.test:
				ind = ind + 1
				if ind >=TESTRANG:
					break
class HANDAPI(multiprocessing.Process):
	test = False
	startt = 0
	endd = 0
	def __init__(self,startt=0,endd=8,test=False):
		multiprocessing.Process.__init__(self)
		self.test = test
		self.startt = int(startt)
		self.endd = int(endd)	
	def run(self):
		hda = []
		thceil = math.floor((self.endd-self.startt)/THREADS)
		st_ = 0
		ed_ = thceil
		for i in range(THREADS):
			if i < THREADS-1:
				hda.append(HandALL(test=self.test,start_=st_,end_=ed_));print("开跑range %s ~ %s"%(str(st_),str(ed_)))
				hda[len(hda)-1].start();print("  --某进程下开启新线程")
				hda[len(hda)-1].join()
				st_ = ed_
				ed_ = ed_ + thceil
			else:
				aa = HandALL(test=self.test,start_ = st_ , end_ = self.endd - self.startt - st_);print("开跑range %s ~ %s"%(str(st_),str(ed_)))
if __name__=="__main__":
	
	if len(sys.argv)>1 and sys.argv[1] == "-m":	
		lllsl = len(origin)
		cpcei = math.floor(lllsl/CPUS)
		startt = 0
		endd = cpcei
		hddc=[]
		for ij in range(CPUS):
			if ij < CPUS-1:
				hddc.append(HANDAPI(test=True))
				#hddc[len(hddc)-1].start()#;#print("开启新进程")
				#hddc[len(hddc)-1].join()
				tmpp = endd
				startt = tmpp
				endd = tmpp + cpcei
				#endd = endd + cpcei
				
			else:
			 	hddcdd = HANDAPI(test=True,startt=str(startt),endd=str(lllsl-startt))
			 	hddcdd.start()
			 	hddcdd.join()
		for iis in hddc:
			iis.start();print("开启新进程")
			iis.join()
	else:
		if  len(sys.argv)>1 and sys.argv[1]!="-do" and sys.argv[1]=="-t" and sys.argv[2]=="-t":
			for ori in origin[0:TESTRANG]:
				UrlCollec(ori['href'],ori['id'])
		elif len(sys.argv)>1 and sys.argv[1] == "-do":
			if sys.argv[2]!=None and sys.argv[2] == "-t":
				HandTempLL(test=True)
			else:
				HandTempLL(False)
		else:
			HandTempLL(test=True)
		#else:
			#for ori in origin:
		#		print(ori['href'])
				#UrlCollec(ori['href'],ori['id'])	















