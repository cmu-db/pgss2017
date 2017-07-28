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
				if headerval.endswith(':'): headerval = headerval[:-1].strip()

				# Parse jail and probation terms
				if headerval in {'Jail Term', 'Suspended Term', 'UnSuspended Term', 'Probation', 'Supervised', 'UnSupervised'}:
					# Generate interval string from yrs+mos+days+hrs fields
					yrs = rows[i+2].get_text().strip() or '0'
					mos = rows[i+4].get_text().strip() or '0'
					days = rows[i+6].get_text().strip() or '0'
					hrs = rows[i+8].get_text().strip() or '0'
					interval = yrs + '-' + mos + ' ' + days + ' ' + hrs + ':00:00'
					# Append as KVP
					data[headerval] = interval
					# Skip to the next section after this
					i += 8
				# Parse newer event table format
				elif row.parent.name == 'th' and headerval == 'Event Type':
					# Get number of table columns
					headerVals = []
					for j in range(i, len(rows)):
						if rows[j].parent.name != 'th':
							break
						else:
							headerVals.append(rows[j].get_text().strip())
					# Get row values
					rowVals = []
					for k in range(i+len(headerVals), len(rows)):
						if not 'Value' in rows[k].attrs.get('class', []):
							i = k # Skip to the next section after this
							break
						else:
							rowVals.append(rows[k].get_text().strip())
					# Split and append events
					for l in range(0, len(rowVals), len(headerVals)):
						eventData = {x[0]: x[1] for x in zip(headerVals, rowVals[l:l+len(headerVals)])}
						output.append(eventData)
			# Values
			elif 'Value' in classes:
				dataval = row.get_text().strip()
				if headerval and dataval != 'MONEY JUDGMENT': # The 'money judgement' header is useless
					data[headerval] = dataval
			# Headers and separators
			else:
				if 'InfoChargeStatement' not in classes:
					if row.name in {'hr', 'h5', 'h6', 'i'}:
						header = row.get_text().strip()
						# Skip over the charge subheadings
						if not (header in {'Disposition', 'Jail', 'Probation', 'Fine', 'Community Work Service'} and row.name == 'i' and row.parent.name == 'left'):
							# Append the KVPs and reset the temporary dict
							if data:
								output.append(data)
								data = {}
							# Add the header to the data list
							if row.name != 'hr':
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

	# Move attorneys listed under parties to attorneys
	parties = output.get('parties', [])
	j = 0
	while j < len(parties):
		partyType = parties[j].get('type')
		# Check if party type is an attorney
		if partyType and partyType.lower().startswith('attorney for '):
			# Remove the party from the parties list
			party = parties.pop(j)
			j -= 1
			# Set the type to the appropriate attorney type
			party['type'] = partyType[13:]
			# Create attorneys key if necessary
			if not output.get('attorneys'):
				output['attorneys'] = []
			# Append this attorney
			output['attorneys'].append(party)
		j += 1

	return output

def formatAttrs(data, section):
	# Formatted output dict
	d = {}

	# Iterate thru fields in input dict
	for field in data:
		# Get proper field names
		formattedName = getAttributeName(field)
		d[formattedName] = data[field]
		# Format heights
		if formattedName == 'height' and ('\'' in data[field] or '"' in data[field]):
			vals = data[field].replace('"', '\'').split('\'')
			d[formattedName] = str(int(vals[0]) * 12 + int(vals[1]))

	# Assign attorneys a type based on what section they're in
	if section.startswith('Attorney(s) for the '):
		if d.get('appearance_date'):
			d['type'] = section[20:]
		# Discard party information in the attorney sections
		else:
			return None
	# Assign officers a type to indicate that they're officers
	elif 'Defendant' in section or 'Plaintiff' in section or 'Officer' in section:
		d['type'] = section.replace(' Information', '')

	return d

# This is only for testing
if __name__ == '__main__': print(parseCase(open('test.html', 'r').read()))
