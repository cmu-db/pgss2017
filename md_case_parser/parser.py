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
	i = 0
	while i < len(rows):
		row = rows[i]

		# Save class list
		classes = row.attrs.get('class', [])

		if 'AltBodyWindowDcCivil' not in classes:
			# Field names
			if 'FirstColumnPrompt' in classes or 'Prompt' in classes:
				headerval = row.get_text().strip()

				# Parse newer event table format
				if row.parent.name == 'th' and headerval == 'Event Type':
					# Get number of table columns
					headerVals = []
					for j in range(i, len(rows)):
						if rows[j].parent.name != 'th':
							break
						else:
							headerVals.append(rows[j].get_text().strip())
					# Get row values
					rowVals = []
					for j in range(i+len(headerVals), len(rows)):
						if not 'Value' in rows[j].attrs.get('class', []):
							i = j # Skip to the next section after this
							break
						else:
							rowVals.append(rows[j].get_text().strip())
					# Split and append events
					for k in range(0, len(rowVals), len(headerVals)):
						eventData = {x[0]: x[1] for x in zip(headerVals, rowVals[k:k+len(headerVals)])}
						output.append(eventData)
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

		# Increment index
		i += 1

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

	# Assign officers a type to indicate that they're officers
	if 'Defendant' in section or 'Plaintiff' in section or 'Officer' in section:
		d['type'] = section.replace(' Information', '')

	return d

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
