from bs4 import BeautifulSoup

def parseCase(html):
	# Import into BS
	soup = BeautifulSoup(html, 'html.parser')

	# Extract all headers, spans, and breaks
	rows = soup.find_all(['span', 'h5', 'h6', 'hr'])
	data = {}
	outdata = {}
	output = []
	for row in rows:
		if row.has_attr('class'):
			classes = row['class']
			if 'AltBodyWindowDcCivil' not in classes:
				# Get attribute name
				if 'FirstColumnPrompt' in classes or 'Prompt' in classes:
					headerval = row.get_text()
				# Get corresponding value
				elif 'Value' in classes:
					dataval = row.get_text()
					if headerval:
						data[headerval] = dataval
				else:
					if 'InfoChargeStatement' not in classes:
						# TODO: clean this up
						checkH5 = re.findall("h5", str(row))
						checkH6 = re.findall("h6", str(row))
						checkHR = re.findall("hr", str(row))
						checki = re.findall("i", str(row))
						if len(checkH5) > 0 or len(checkH6) > 0	or len(checki) > 0:
							if len(outdata) > 0:
								output.append(outdata)
								outdata = {}
							tablehead = row.get_text().strip().replace('/', '-')
							tablehead = re.sub('\s+', ' ', tablehead)
							if len(tablehead) > 0:
								output.append(tablehead)
						if len(checkHR) > 0:
							if len(outdata) > 0:
								output.append(outdata)
								outdata = {}
							else:
								continue

	return data

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
