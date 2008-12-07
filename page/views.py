# Create your views here.
import class_con
import psycopg2
from django.http import HttpResponse

def req_handler(request, fname):		
	#please replase xxx and others with proper parameters to make it working.
	con = psycopg2.connect("dbname='baali' user='baali' password='pong'")
	cur = con.cursor()	
	page = fname.split('/')
	print page[-1]
	#to make first letter capital, while in links it is smaller but in table/xml, it is always Capital
	link = page[-1][0].upper()+page[-1][1:len(page[-1])]		
	print link
	cur.execute('select * from enwiki_db where name=%s',[link])
	r = cur.fetchone()	
	if r != None:
		print r[0], r[1], r[2], r[3]
		#print len(r)
		Obj = class_con.Xml_Html(r[1],r[2],r[3])
		while Obj.flag_red == 1:									
			Obj.link_red = Obj.link_red[0].upper()+Obj.link_red[1:len(Obj.link_red)]			
			if r[0] == Obj.link_red:
				print Obj.link_red
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
