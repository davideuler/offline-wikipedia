#stand alone script which can be used for testing parser.
#will need a wiki-format file as input and convert it to result.html as output.


import bz2
import re
from elementtree import ElementTree

class Xml_Html:	
	xml_html = ''
	Toc = ''
	title = ''
	def __init__(self):
		#make entries of all heading in table in case number of headings are more then 4 
		#put local refrence to heading
		#make the linking proper
		#consider case of <nowiki>
		#try to get those hindi fonts working		
		self.Toc = '<table id="toc" class="toc" summary="Contents">\n<tr>\n<td>\n<div id="toctitle">\n<h2>Contents</h2>\n</div>\n'
		#replace xxx with wiki-file you want to convert to html file
		file = open('xxx')		
		tree = ElementTree.parse(file).getroot()		
		for it in tree.getiterator():
        		print it.tag
			if it.tag == 'title':
				self.title = it.text
        		if it.tag == 'text':
        	        	self.xml_html=it.text
		file.close()				
			
	def Process(self):	
		#make sure the location of en_template file			
		template = open('en_template').read().decode('utf-8')
		self.xml_html = self.blocks(self.xml_html)
		self.Toc += '</ol>\n</td>\n</tr>\n</table>'
		#print self.Toc
		page_html = ''
		page_html = template[0:template.find('<title>')]
		page_html += '<title>'+self.title+'</titile>\n'
		page_html += template[template.find('<title>')+7:template.find('<h1 class="firstHeading">')+len('<h1 class="firstHeading">')]
		page_html += self.title+'</h1>'
		page_html += template[template.find('<div id="bodyContent">'):template.find('<!-- start content -->')+len('<!-- start content -->')]+'\n'
		page_html += self.xml_html[0:self.xml_html.find('<h2>')]
		page_html += self.Toc
		page_html += self.xml_html[self.xml_html.find('<h2>'):len(self.xml_html)]
		page_html += template[template.find('<!-- start content -->')+len('<!-- start content -->'):len(template)]		
		return page_html

	#for creating (ex/in)ternal links in a page
	def ref_tag( self, match ):
		#check out the links to image also
		#rather then using localhost use relative paths using ../ or something like that.
		#nah it is not proper :(
		target = ''
		tag = match.group()
		cnt = tag.count('[')
		tag = tag.replace('[','')	
		tag = tag.replace(']','')
		if cnt == 2:
			if tag.find('|') != -1 :
				link = tag.split('|')			
				if len(link[1]) == 0:
					#it is for hiding stuff!
					if link[0].find(':') != -1 and link[0].find('(') != -1:
						target += link[0][link[0].find(':'):link[0].find('(')-1]
					elif link[0].find(':') != -1:
						target += link[0][link[0].find(':'):len(link[0])]	
					elif link[0].find('(') != -1:
						target += link[0][0:link[0].find('(')]
					# to make all the offline links work which are interwiki, external links will remain normal, and no need to change them	
					return '<a href=\"http://localhost:8000/wiki/'+link[0]+'\">'+target+'</a>'
				else:
					#normal [[]] link with refrence and name tag
					return '<a href=\"http://localhost:8000/wiki/'+link[0]+'\">'+link[-1]+'</a>'
			else :				
				return '<a href=\"http://localhost:8000/wiki/'+tag+'\">'+tag+'</a>'
		else:	
			#for creating external links 	
			if tag.find(' ') != -1:
				return '<a href=\"'+tag[0:tag.find(' ')]+'\">'+tag[tag.find(' '):len(tag)]+'</a>'
			else:
				return '<a href=\"'+tag+'\">'+tag+'</a>'
		
	# for converting bold and italics wiki text to html equivalent
	def bold_it( self, match ):
		quote = match.group().count('\'')
		if quote == 4:			
			return '<i>'+match.group().replace('\'','')+'</i>'
		elif quote == 6:
			return '<b>'+match.group().replace('\'','')+'</b>'
		else:
			return '<b><i>'+match.group().replace('\'','')+'</i></b>' 
	
	#this takes care of headings
	#create table of all the headings, in case number of topics go beyond 4 and create TOC for it.
	def heading(self,head_tag,level_toc):	
		level = head_tag.count('=')/2
		head_tag = head_tag.replace('=','')
		if level_toc < level:
			#new subtopic is opened
			self.Toc += '<ol>\n<li><a href ="#'+head_tag+'">'+head_tag+'</a></li>\n'
		elif level_toc > level:
			#sublists are closed
			while level < level_toc:
				self.Toc += '</ol>\n'
				level_toc -= 1
			self.Toc += '<li><a href ="#'+head_tag+'">'+head_tag+'</a></li>\n'
		else:
			#new item in list	
			self.Toc += '<li><a href ="#'+head_tag+'">'+head_tag+'</a></li>\n'
		return '<p><a name="'+head_tag+'" id="'+head_tag+'"></a></p>\n<h'+str(level)+'>'+head_tag+'</h'+str(level)+'>'
	
	#this block takes care of tables
	def parser_table(self,table_wiki):
	        #consider case when list is in table, then line start with *#; inbetween two rows or column
	        line = table_wiki.splitlines()
	        opened = 0
	        list_block = ''
	        tr = 0
	        out = ''
	        for each in line:
			#if each.find('{|') == 0:
	                if each.find('{|') != -1:
	                        out += each.replace('{|','<table ')+'>\n'
	                elif each.find('|}') == 0:
	                        if opened == 1:
	                                self.blocks(list_block)
	                                opened = 0
	                        if tr == 1:
	                                out += '</tr>\n'
	                                tr = 0
	                        out += each.replace('|}','</table>\n')
	                elif each.find('|+') == 0:
	                        if opened == 1:
	                                self.blocks(list_block)
	                                opened = 0
	                        out += each.replace('|+','<caption>')+'</caption>\n'
	                elif each.find('|-') == 0:
	                        if opened == 1:
	                                self.blocks(list_block)
	                                opened = 0
	                        if tr == 1:
	                                out += '</tr>\n'
	                                tr = 0
	                        out += each.replace('|-','<tr ')+'>\n'
	                        tr = 1
	                elif each.find('|') == 0 or each.find('!') == 0:
	                        if opened == 1:
	                                self.blocks(list_block)
	                                opened = 0
	                        tag = 'td'
	                        cell = ['']
		                each = each[1:len(each)]
                        	if each.find('!') == 0:
					each = each.replace('!!','||')
	                                tag = tag.replace('td','th')
	                        if each.find('||') != -1:
	                                cell = each.split('||')
	                        else :
	                                cell[0] = each
	                        for one in cell:
	                                sp_cel = one.split('|')
	                                if len(sp_cel) == 2:
	                                        out += '<'+tag+' '+sp_cel[0]+'>'+sp_cel[1]+'</'+tag+'>\n'
	                                else:
	                                        out += '<'+tag+'>'+sp_cel[0]+'</'+tag+'>\n'
	                        del cell[1:len(cell)] #check other way to initialize a string list :P
	                elif each.find('*') ==0 or  each.find(';') ==0 or  each.find('#') ==0:
	                        if opened == 1:
	                                list_block += each+'\n'
	                        else:
	                                opened = 1
	                                list_block = ''
	                                list_block = each
	        return out
	
	#this is special case existing in wikipedia which has link for not existing articles
	#here only highligting it with different color no links are fixed for it
	def no_page(self, match):
		link = match.group()
		link = link.replace('{','')
		link = link.replace('}','')
		if link.find('|') != -1:
			return '<font color=\"FF0000\">'+link[link.find('|')+1:len(link)]+'</font>' 
		else:
			return '<font color=\"FF0000\">'+link+'</font>'

	#to avoid/manage references..........
	def avoid_ref(self, match):
		#print match.group()
		return ''
	
	#this block is for fixing tags of lists ol, ul, dl
	def tag_fixer(self, token):
	        tags = ['','','','']
	        if token == '#':
	                tags[0] = '<ol>'
	                tags[1] = '<li>'
	                tags[2] = '</li>'
	                tags[3] = '</ol>'
	        elif token == '*':
	               tags[0] = '<ul>'
	               tags[1] = '<li>'
	               tags[2] = '</li>'
	               tags[3] = '</ul>'
	        elif token == ';':
	               tags[0] = '<dl>'
	               tags[1] = '<dt>'
	               tags[2] = '</dt>'
	               tags[3] = '<dd>'
	               tags.append('</dd>')
	               tags.append('</dl>')
	       	return tags
	
	def find_col(self, defin):
		#argh it is all messed up right now :(
	        #also consider the case when <nowiki is mentioned>, change case for <a> tag, and other things like no links etc
		#is this case possible that ; and : comes in two seprate lines, in that case this wont work, and return value will be -1 or rather this function wont even be called:(
	        position = 0
	        ptr = 0
	        while position < len(defin):
	                position = defin.find(':',ptr)
	                if defin.find('<a href',ptr) != -1 and position < defin.find('<a href',ptr):
				if position < defin.find('<nowiki',ptr):			
	                        	break		
				else :	
	                		ptr = defin.find('</nowiki>',ptr+len('</nowiki>'))
			if defin.find('<nowiki>',ptr) != -1 and position < defin.find('<nowiki>',ptr):
				if position < defin.find('<a href',ptr):
	                                break
	                        else :
					ptr = defin.find('</a>',ptr+4)		
			if defin.find('<a href',ptr) == -1 and defin.find('<nowiki>',ptr) == -1:
					break
	        return position	
	
	#this is main funstion which calls other funstions, fixes <p> tags, lists, links tables and all
	def blocks(self, data):
	        #check the case when the list is in between table :P		
		level_toc = 0
	        html = ''
	        list_opened = 0
	        present_tag = ''
	        previous_tag = ''
	        list_tag = ['','','','','','']
	        data = data.split('\n')
	        table_counter = 0
	        got_table = 0
	        table = ''
	        start_p = 0
		#to check for references
		ref_open = 0
		reference_data = ''
		#for info/texo boxes .......
		box_open = 0
		box_text = ''
	        for lines in data:
	                if len(lines) == 0:
				#to see opening of new paragragh	                        
	                        if start_p == 0:
	                                html += '<p>\n'
	                                start_p = 1
	                        elif start_p == 1:
	                                html += '</p>\n'
	                                start_p = 0
				continue
				
			#finish all the tags for a,b,h1 etc here itself
	
			#to avoid/manage refrences and citation 
			rg_ref = re.compile(r'<ref.*?/>')
			rg_nonclosingref = re.compile(r'<ref.*?>.*?</ref>')
			if ref_open == 1 and lines.find('</ref>') == -1:
				reference_data += lines
				continue
			lines = rg_nonclosingref.sub(self.avoid_ref, lines)
			lines = rg_ref.sub(self.avoid_ref, lines)		
			#end of cited data
			if ref_open == 1 and lines.find('</ref>') != -1:
				reference_data += lines[0:lines.find('</ref>')+6]
				#print reference_data	
				reference_data = ''
				lines = lines[lines.find('</ref>')+6:len(lines)]
				lines = rg_ref.sub(self.avoid_ref, lines)
				lines = rg_nonclosingref.sub(self.avoid_ref, lines)
				ref_open = 0
			#start of cited data
			if lines.find('<ref') != -1 and lines.find('</ref>') == -1:
				ref_open = 1
				reference_data = lines[lines.find('<ref'):len(lines)]
				lines = lines[0:lines.find('<ref')]	

			#Info/texo boxes and all.....
			#okay so this regex will remove all the nonexisting links also, so need to figure out how to jump this block
			rg_cite = re.compile(r'\{\{[^\{]*?\}\}')
			lines = rg_cite.sub(self.avoid_ref, lines)
			if box_open != 0 and lines.find('}}') == -1:
				box_text += lines
				box_open += lines.count('{{')
				#print box_open
				continue
			if box_open != 0 and lines.find('}}') != -1:								
				box_open -= lines.count('}}')				
				box_open += lines.count('{{')
				#print box_open
				if box_open == 0:
					box_text += lines[0:lines.find('}}')]+'}}'
					#print box_text
					box_text = ''
					lines = lines[lines.find('}}')+2:len(lines)]
				else:
					box_text += lines
					continue							
			if lines.find('{{') != -1 and lines.find('}}') == -1:
				box_open = 1
				box_text = lines[lines.find('{{'):len(lines)]
				lines = lines[0:lines.find('{{')]								
	
			#for normal html refrence
	                rg_href = re.compile(r'\[{1,2}([^\]]*)\]{1,2}')
	                lines = rg_href.sub(self.ref_tag, lines)
	                
	                #for links to pages which do not exsist(right now just making the color red nothing else,
	                #as of now this wikipedia does not support editing)
	                rg_dneref = re.compile(r'\{\{([^\}]*)\}\}')
	                lines = rg_dneref.sub(self.no_page, lines)
	                rg_bold_it = re.compile(r'\'{2,5}([^\']*)\'{2,5}')
	                lines = rg_bold_it.sub(self.bold_it, lines)
	
	                if lines.find('==') == 0: 
				old_line = lines
				#close opened <p> if any
				if start_p == 1:
					html +=  '</p>\n'
					start_p = 0
	                	lines = self.heading(lines,level_toc)
				level_toc = old_line.count('=')/2
	
	                if lines.find('{|') == 0 or table_counter != 0:
				#to check table in text
				#consider case when there is nesting of tables :(
				#to close already opened <p> tag
	                        if start_p == 1: 
					html += '</p>\n'
	                                start_p = 0
	                        table += lines+'\n'
	                        got_table = 1
	                        if lines.find('{|') == 0:
	                                table_counter += 1
	                        elif lines.find('|}') == 0:				
	                                table_counter -= 1
					if table_counter != 0 :
						#here is nesting of table :P
						table = table.replace(table[table.rfind('{|'):len(table)],self.parser_table(table[table.rfind('{|'):len(table)]))
	                        continue
	                if got_table == 1:
	                        html += self.parser_table(table)
				table = ''
	                        got_table = 0
	
	                if lines.find('#') == 0 or lines.find('*') == 0 or lines.find(';') == 0:
	                        if start_p == 1:
	                                html += '</p>\n'
					start_p = 0                        
	                        list_opened = 1                                                               
	                        text = lines.lstrip('#*;')
				if text == '':
					continue
	                        present_tag = lines[0:lines.find(text)]
				#print present_tag, text
	                        if len(present_tag) > len(previous_tag):
	                                #this is starting of new list                           
	                                list_tag = self.tag_fixer(present_tag[-1])
	                                if present_tag[-1] != ';':
	                                        html += list_tag[0]+'\n'+list_tag[1]+text+list_tag[2]+'\n'
	                                else:
	                                        col_pos = self.find_col(text)
						if col_pos != -1:
	                                        	html += list_tag[0]+'\n'+list_tag[1]+text[0:col_pos-1]+list_tag[2]+'\n'
	                                        	html += list_tag[3]+text[col_pos+1:len(text)]+list_tag[4]+'\n'
	                        elif len(previous_tag) == len(present_tag):
	                                #this is new item
	                                if present_tag[-1] != ';':
	                                        html += list_tag[1]+text+list_tag[2]+'\n'
	                                else:
	                                        col_pos = self.find_col(text)
						if col_pos != -1:
	                                        	html += list_tag[1]+text[0:col_pos-1]+list_tag[2]+'\n'
	                                        	html += list_tag[3]+text[col_pos+1:len(text)]+list_tag[4]+'\n'
	                        else:
	                                #close all opened lists nested in this list
	                                counter = len(previous_tag)
	                                while counter != len(present_tag):
	                                        list_tag = self.tag_fixer(previous_tag[counter-1])
	                                        html += list_tag[-1]+'\n'
	                                        counter -= 1
	                                #make entry in present list					
	                                list_tag = self.tag_fixer(present_tag[-1])
	                                if present_tag[-1] != ';':
	                                       	html += list_tag[1]+text+list_tag[2]+'\n'
	                                else:
	                                       	col_pos = self.find_col(text)
						if col_pos != -1:
	                                       		html += list_tag[1]+text[0:col_pos-1]+list_tag[2]+'\n'
	                                       		html += list_tag[3]+text[col_pos+1:len(text)]+list_tag[4]+'\n'
	                        previous_tag = present_tag
			else:
	                	if list_opened == 1:
	                        	html += list_tag[-1]+'\n'                                
	                                list_opened = 0
	                                previous_tag = ''						
	                        html += lines+'<br />\n'
		#print refrence
		return html	
def main():
	Obj = Xml_Html()
	op = open('result.html','w')
	op.write(Obj.Process().encode('utf-8'))
	op.close()

if __name__ == "__main__":
    main()		
