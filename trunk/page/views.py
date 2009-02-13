# Create your views here.
import class_con
import sqlite3
from django.http import HttpResponse

def first(request):
	front_page = ''
	con = sqlite3.connect('english-xml-db')
	cur = con.cursor()
	cur.execute('select name from articles')
	template = open('data/en_template').read().decode('utf-8')			
	front_page = template[0:template.find('<title>')]
	front_page += '<title>List of all Articles</titile>\n'
	front_page += template[template.find('<title>')+7:template.find('<h1 class="firstHeading">')+len('<h1 class="firstHeading">')]
	front_page += 'Article List</h1>'
	front_page += template[template.find('<div id="bodyContent">'):template.find('<!-- start content -->')+len('<!-- start content -->')]+'\n'
	counter = 0
	front_page += '<table>\n<tr>\n'
	for row in cur:
		if counter == 3:
			front_page += '</tr>\n<tr>\n'
			counter = 0
		front_page += '<td><a href="/wiki/'+row[0]+'/">'+row[0]+'</a></td>\n'
		counter += 1
	if counter != 0:
		front_page += '</tr>\n</table>'
	else:
		front_page += '</table>'		
	front_page += template[template.find('<!-- start content -->')+len('<!-- start content -->'):len(template)]
	return HttpResponse(front_page)

def req_handler(request, fname):		
	#please replase xxx and others with proper parameters to make it working.
	con = sqlite3.connect('english-xml-db')
	cur = con.cursor()	
	page = fname.split('/')
	print page[-1]
	#to make first letter capital, while in links it is smaller but in table/xml, it is always Capital
	link = page[-1][0].upper()+page[-1][1:len(page[-1])]		
	print link
	cur.execute('select * from articles where name = (?)',[link])
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
			cur.execute('select * from articles where name = (?)',[Obj.link_red])
			r = cur.fetchone()
			if r != None:
				Obj = class_con.Xml_Html(r[1],r[2],r[3])
			else:
				break
		return HttpResponse(Obj.Process())	 
	else:
		return HttpResponse('No page available!')
