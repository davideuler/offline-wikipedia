# Create your views here.
import class_con
import csv
from django.http import HttpResponse

def req_handler(request, fname):		
	file_csv = 'article_'	
	#this case will work for english only, since for other languages all articles goes into category of special only and this wont hold valid anymore.
	#for unicode type strings, characters of other languages also become alpahbets, accordingly, hence there was problem of special character articles were giving error. Pointed out by Stian.
	page = fname.encode('utf-8')
	print page
	#check if first letter is alphabet or not..
	if page[0].isalpha():
		#to make first letter capital, while in links it is smaller but in table/xml, it is always Capital
		link = page[0].upper()+page[1:len(page)]
		file_reader = csv.reader(open(file_csv+link[0]))
	elif page[0].isdigit():
		#first character is digit
		link = page
		file_reader = csv.reader(open(file_csv+'0'))
	else:
		#first character is special character
		link = page
		file_reader = csv.reader(open(file_csv+'special'))
	print link

	#looking through csv file is different then db.
	#again this sorting of articles might not work in case of lang other then english
	for r in file_reader:
		if link == r[0]:
			break		
		r = None			

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
					#redirection link is initialized
					Obj = class_con.Xml_Html(r[1],r[2],r[3])
					break
				r = None
			if r == None:
				return HttpResponse('No page available!')
		return HttpResponse(Obj.Process())
	else:
		return HttpResponse('No page available!')
