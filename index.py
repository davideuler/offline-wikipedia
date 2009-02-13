#File to create index table named enwiki_db with dbname = ...... , from fragmented enwiki bz2 files.
import bz2
from elementtree import ElementTree
import psycopg2
import os

#Replace xxx with proper data
con = psycopg2.connect("dbname='xxx' user='xxx' password='xxx'")
cur = con.cursor()
cur.execute("CREATE TABLE enwiki_db (name text, block text, start_block int4, end_block int4)")
#this variable stores the location of your fragmented wiki-dumps.
#for me the files are of name rec0xxxxxenwiki-20080724-pages-articles.xml.bz2
#name_start will have starting part of location, coming before rec, replace xxx with that
name_start = 'xxx/rec'
#here xxx will correspond to date of dumps you have downladed, for me xxx was 20080724, please replace it accordingly.
name_end = 'enwiki-xxx-pages-articles.xml.bz2'
num = 1
fname = '%(fstart)s%(fnum)05d%(fend)s' %{'fstart':name_start,'fnum':num,'fend':name_end}
block_file = open(fname,'rb')
data = bz2.decompress(block_file.read())
pos = 0
while True:		
	beg = data.find('<page>',pos)
	if beg == -1:
		#perfect end in previous block
		block_file.close()
		num += 1
		fname = '%(fstart)s%(fnum)05d%(fend)s' %{'fstart':name_start,'fnum':num,'fend':name_end}
		print fname
		if os.path.isfile(fname):
			block_file = open(fname,'rb')	
		else:
			break
		data = bz2.decompress(block_file.read())
		beg = data.find('<page>',pos)		
		end = data.find('</page>',beg)
		block = data[beg:end]
	elif beg != -1 and data.find('</page>',beg) == -1:
		#there is a article spanning in two blocks
		block = data[beg:len(data)]
		block_file.close()
		num += 1
		fname = '%(fstart)s%(fnum)05d%(fend)s' %{'fstart':name_start,'fnum':num,'fend':name_end}
		print fname
		if os.path.isfile(fname):
			block_file = open(fname,'rb')	
		else:
			break
		data = bz2.decompress(block_file.read())
		end = data.find('</page>')
		block += data[0:end]
	else:
		end = data.find('</page>',beg)
		#normal case article starts and ends in one block
		block = data[beg:end]		
	pos = end+7
	title_start = block.find('<title>')			
	title = block[title_start+7:block.find('</title>',title_start)].decode('utf-8')					
	print title.encode('utf-8')
	cur.execute('INSERT INTO enwiki_db VALUES (%s,%s,%s,%s)',[title,fname,beg,end])
	con.commit()						

cur.close()
