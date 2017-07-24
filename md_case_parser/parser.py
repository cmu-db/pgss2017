from bs4 import BeautifulSoup
from attrnames import getAttributeName, getSectionName

def parseCase(html):
	# Import into BS
	soup = BeautifulSoup(html, 'html.parser')

	# Temporary KVP store
	data = {}
	# Full data list
	output = []

	# Get KVPs, headers, and separators
	rows = soup.find_all(['span', 'h5', 'h6', 'i', 'hr'])
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
				if headerval and dataval != 'MONEY JUDGMENT':
					data[headerval] = dataval
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

	return formatOutput(output)

def formatOutput(data):
	# Final output dict
	output = {}

	# Iterate thru data list
	for i in range(len(data)):
		# Check if item is a section header
		if isinstance(data[i], str):
			# Get proper attribute name
			header = getSectionName(data[i])
			# Make sure section is going to be stored
			if header:
				entries = []
				# Find KVP dicts corresponding to this header
				for j in range(i+1, len(data)):
					# Stop looking when we reach a different header
					if isinstance(data[j], str):
						break
					# Get proper attribute names for fields
					attrMap = formatAttrs(data[j], data[i])
					# Save this dict if it hasn't been nullified
					if attrMap:
						entries.append(attrMap)
				# Add all the data we found to the master dict
				if output.get(header):
					output[header] += entries
				else:
					output[header] = entries

	return output

def formatAttrs(data, section):
	# Formatted output dict
	d = {}

	# Get proper field names
	for field in data:
		d[getAttributeName(field)] = data[field]

	# Assign attorneys a type based on what section they're in
	if section.startswith('Attorney(s) for the '):
		if d.get('appearance_date'):
			d['type'] = section[20:]
		# Discard party information in the attorney sections
		else:
			return None

	return d

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
