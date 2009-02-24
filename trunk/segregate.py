#for creating seprae csv files for each alphabet and number, and sperate file with non-eng alphabet in random csv..
import csv

list_read = csv.reader(open('mod'))
last_alpha = 'A'
csv_file = 'article_'
file_special = open(csv_file+'special','wb')
file_char = open(csv_file+'A','wb')
file_digit = open(csv_file+'0','wb')
csv_writer_digit = csv.writer(file_digit)
csv_writer_special = csv.writer(file_special)
csv_writer_char = csv.writer(file_char)
print last_alpha
for row in list_read:
	try:
		if row[0][0].isalpha():
			if row[0][0] != last_alpha:
				print row[0]
				file_char.close()
				file_char = open(csv_file+row[0][0],'wb')
				csv_writer_char = csv.writer(file_char)
			last_alpha = row[0][0]
			csv_writer_char.writerow([row[0],row[1],row[2],row[3]])			
		elif row[0][0].isdigit():
			csv_writer_digit.writerow([row[0],row[1],row[2],row[3]])
		else:
			csv_writer_special.writerow([row[0],row[1],row[2],row[3]])
	except:
		continue
file_char.close()
file_digit.close()
file_special.close()
