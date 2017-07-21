from bs4 import BeautifulSoup

def parseCase(html):
    soup = BeautifulSoup(html, 'html.parser')

	rows = soup.find_all(['span', 'h5', 'h6', 'hr'])
	outdata = {}
	output = []
	for row in rows:
		#with open('rowval32.txt', 'a') as file:
			#file.write("%s\n" % row)
		if "AltBodyWindowDcCivil" not in row.attrs.get('class', []):
			if "FirstColumnPrompt" in row.attrs.get('class', []):
				headerval = row.get_text().strip().strip(':').replace('/', '-')
				headerval = re.sub('\s+', ' ', headerval)
				#print ('** key ** ', headerval)
			elif "Prompt" in row.attrs.get('class', []):
				headerval = row.get_text().strip().strip(':').replace('/', '-')
				headerval = re.sub('\s+', ' ', headerval)
				#print ('** key ** ', headerval)
			elif "Value" in row.attrs.get('class', []):
				dataval = row.get_text().strip().replace('/', '-')
				dataval = re.sub('\s+', ' ', dataval)
				#print ('** value ** ', dataval)
				if headerval:
					outdata[headerval] =  dataval
			else:
				if "InfoChargeStatement" not in row.attrs.get('class', []):
					#print ('**** row ***', row)
					checkH5 = re.findall("h5", str(row))
					CheckH6 = re.findall("h6", str(row))
					checkHR = re.findall("hr", str(row))
					checki = re.findall("i", str(row))
					if len(checkH5) > 0 or len(CheckH6) > 0	or len(checki) > 0:
						if len(outdata) > 0:
							output.append(outdata)
							outdata = {}
						tablehead = row.get_text().strip().replace('/', '-')
						tablehead = re.sub('\s+', ' ', tablehead)
						#print ('** table header ** ', tablehead)
						if len(tablehead) > 0:
							output.append(tablehead)
					if len(checkHR) > 0:
						if len(outdata) > 0:
							output.append(outdata)
							outdata = {}
						else:
							continue

    # For testing only
    FILE_NAME = str(now.year)+'-'+str(now.month)+'-'+ str(now.day)+'-'+str(now.hour)+'-'+str(now.minute)+'-'+str(now.second)+'-'+'DataFile.txt'
    #print('*** File Name is : ***', FILE_NAME)
	if len(outdata) > 0:
		output.append(outdata)
		outdata = {}
	with open(FILE_NAME, 'a') as file:
		file.write("%s\n" % output)

    return {}

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
