from bs4 import BeautifulSoup

def parseCase(html):
	# Import into BS
	soup = BeautifulSoup(html, 'html.parser')

	# Temporary KVP store
	data = {}
	# Full data list
	output = []

	# Get KVPs, headers, and separators
	rows = soup.find_all(['span', 'h5', 'h6', 'hr'])
	# Iterate thru page rows
	for row in rows:
		# Save class list
		classes = row.attrs.get('class', [])

		if 'AltBodyWindowDcCivil' not in classes:
			# Field names
			if 'FirstColumnPrompt' in classes or 'Prompt' in classes:
				headerval = row.get_text().strip()
			# Values
			elif 'Value' in classes:
				dataval = row.get_text().strip()
				if headerval:
					data[headerval] =  dataval
			# Headers and separators
			else:
				if 'InfoChargeStatement' not in classes:
					if row.name in {'hr', 'h5', 'h6', 'i'}:
						# Append the KVPs and reset the temporary dict
						if data:
							output.append(data)
							data = {}
						# Add the header to the data list
						if row.name != 'hr':
							header = row.get_text().strip()
							if header:
								output.append(header)

	# Append any remaining KVPs
	if data:
		output.append(data)
		data = {}

	return output

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
