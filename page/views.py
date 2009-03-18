# Create your views here.
import class_con
import csv
from django.http import HttpResponse

def req_handler(request, fname):		
	file_csv = 'article_'	
	page = fname
	print page
	#check if first letter is alphabet or not..
	if page[0].isalpha():
		#to make first letter capital, while in links it is smaller but in table/xml, it is always Capital
		link = page[0].upper()+page[1:len(page)]
		file_reader = csv.reader(open(file_csv+link[0]))
	elif page[-1][0].isdigit():
		#first character is digit
		link = page
		file_reader = csv.reader(open(file_csv+'0'))
	else:
		#first character is special character
		link = page
		file_reader = csv.reader(open(file_csv+'special'))
	print link
	
	for r in file_reader:
		if link.encode('utf-8') == r[0]:
			break

	if r != None:
		print r[0], r[1], r[2], r[3]
		#print len(r)
		Obj = class_con.Xml_Html(r[1],r[2],r[3])
		while Obj.flag_red == 1:
			if Obj.link_red[0].isalpha():
				Obj.link_red = Obj.link_red[0].upper()+Obj.link_red[1:len(Obj.link_red)]
			if r[0] == Obj.link_red.encode('utf-8'):
				print Obj.link_red
				#self redirecting loop..........
				return HttpResponse('Page redirecting to Itself...')
				break
			if Obj.link_red[0].isalpha():
				file_reader = csv.reader(open(file_csv+Obj.link_red[0]))
			elif Obj.link_red[0].isdigit():
				file_reader = csv.reader(open(file_csv+'0'))
			else:
				file_reader = csv.reader(open(file_csv+'special'))
			for r in file_reader:
				if Obj.link_red.encode('utf-8') == r[0]:
					break				
			#this if else will result in page with redirected text, in case redirection link is not available in db/csv
			#it wont work in case of csv, in case search of article fails, it will return the last article mentioned in scv file...
			if r != None:
				Obj = class_con.Xml_Html(r[1],r[2],r[3])
			else:
				break
		return HttpResponse(Obj.Process())
	else:
		return HttpResponse('No page available!')
