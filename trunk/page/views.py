# Create your views here.
import class_con
import psycopg2
from django.http import HttpResponse

def req_handler(request, fname):		
	#please replase xxx and others with proper parameters to make it working.
	con = psycopg2.connect("dbname='xxx' user='yyy' password='zzz'")
	cur = con.cursor()	
	page = fname.split('/')
	page[-1] = page[-1].capitalize()
	cur.execute('select * from enwiki_db where name=%s',[page[-1]])
	r = cur.fetchone()	
	if r != None:
		print r[0]
		#print len(r)
		Obj = class_con.Xml_Html(r[1],r[2],r[3])
		while Obj.flag_red == 1:
			print Obj.link_red			
			Obj.link_red = Obj.link_red.capitalize()			
			if r[0] == Obj.link_red:
				#self redirecting loop..........
				return HttpResponse('Page redirecting to Itself...')
				break
			cur.execute('select * from enwiki_db where name=%s',[Obj.link_red])
			r = cur.fetchone()
			if r != None:
				Obj = class_con.Xml_Html(r[1],r[2],r[3])
			else:
				break
		return HttpResponse(Obj.Process())	 
	else:
		return HttpResponse('No page available!')
