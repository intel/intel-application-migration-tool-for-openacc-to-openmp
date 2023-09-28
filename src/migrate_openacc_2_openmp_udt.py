#
# Code generation module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP* API"
#

def splitEntities (entities):

	# We will keep in res the found entities
	res = []
	while True:
		open_parenthesis_pos = entities.find ("(")
		comma_pos = entities.find (",")
		if comma_pos >= 0 and open_parenthesis_pos >= 0:
			# There is a comma and a parenthesis at least,
			# check which comes first
			if comma_pos < open_parenthesis_pos:
				# Comma first, process entitiy
				tmp = entities[:comma_pos] # Keep first entitity in comma-separated list
				tmp = tmp.strip()
				if len(tmp) > 0:
					res = res + [tmp]
				entities = entities[comma_pos+1:] # Process remaining part
			elif comma_pos > open_parenthesis_pos:
				# Parenthesis first, process entity with array
				close_parenthesis_pos = entities.find (")") # Find matching () and return entity name + array part
				if close_parenthesis_pos >= 0:
					tmp = entities[:close_parenthesis_pos+1]
					tmp = tmp.strip()
					if len(tmp) > 0:
						res = res + [tmp]
				entities = entities[close_parenthesis_pos+1:]
				# Check for next entity, if any. If there is, continue from there
				#  -- previous comma could be part of multi-dimensional array e.g. (:,:)
				comma_pos = entities.find (",")
				if comma_pos >= 0:
					entities = entities[comma_pos+1:]
				else:
					break
		elif comma_pos >= 0 and open_parenthesis_pos == -1:
			tmp = entities[:comma_pos] # Keep first entitity in comma-separated list
			tmp = tmp.strip()
			if len(tmp) > 0:
				res = res + [tmp]
			entities = entities[comma_pos+1:] # Process remaining part
		elif comma_pos == -1 and open_parenthesis_pos >= 0:
			close_parenthesis_pos = entities.find (")") # Find matching () and return entity name + array part
			if close_parenthesis_pos >= 0:
				tmp = entities[:close_parenthesis_pos+1]
				tmp = tmp.strip()
				if len(tmp) > 0:
					res = res + [tmp]
			break
		else:
			tmp = entities.strip() # There is a single entity
			if len(tmp) > 0:
				res = res + [tmp]
			break

	# Check if members were initialized, and if so, skip that initialization
	for i in range(0,len(res)):
		member = res[i]
		# Member is initialized if it has a =, which we will drop
		member_initialize_pos = member.find ("=")
		if member_initialize_pos >= 0:
			res[i] = member[0:member_initialize_pos].strip()

	return res

# getUDTMembers (UDT)
#  Parses a Fortran user defined type and extracts the entity names and their
#  array sections (if any)
def getUDTMembers (UDT):

	# Process all members found in the user-defined-type
	# Process them line-by-line, and aggregate results into sentitites -- which is a set of splitted entities
	sentities = []
	for m in UDT.members:
		if m.startswith ("#"):
			sentities = sentities + [ m ]
		else:
			if '::' in m:
				parts = m.split ("::")
			else:
				parts = m.split (" ")
			entities = ""
			for e in parts[1:]:
				entities = entities + e
			sentities = sentities + splitEntities(entities)

	return sentities
