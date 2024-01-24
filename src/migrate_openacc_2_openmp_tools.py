#
# Helper tools module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP*"
#

import migrate_openacc_2_openmp_constants as CONSTANTS
import re

# findClosingParenthesis (s, pos, line, lines)
#  finds the matching closing parenthesis for the open parenthesis that is on
#  position "pos" or beyond that. If line and lines are given, then continue
#  the search on the following lines
#  CAUTION: IGNORES COMMENTS!
def findClosingParenthesis (s, pos, line, lines):
	res = -1
	nopenparenthesis = 0

	# Search in the string for the parenthesis
	for i in range(pos, len(s)):
		# Check for closing parenthesis that matches this opening parenthesis
		if s[i] == '(':
			nopenparenthesis = nopenparenthesis + 1
		elif s[i] == ')':
			nopenparenthesis = nopenparenthesis - 1
			if nopenparenthesis == 0:
				res = i
				break

	# If we have consumed the line, and still have open parenthesis and we have
	# more lines to consume, then search on next lines
	if nopenparenthesis > 0 and line is not None and lines is not None:
		currentline = line+1
		while currentline < len(lines) and nopenparenthesis > 0:
			s = lines[line]
			pos = 0
			# Search in the string for the parenthesis
			for i in range(pos, len(s)):
				# Check for closing parenthesis that matches this opening parenthesis
				if s[i] == '(':
					nopenparenthesis = nopenparenthesis + 1
				elif s[i] == ')':
					nopenparenthesis = nopenparenthesis - 1
					if nopenparenthesis == 0:
						res = i
						break
		# If we were not able to find the closing parenthesis, return failure
		if nopenparenthesis > 0:
			return -1, None
		else:
		# If we were able to find the closing parenthesis, return current char
		# and current line
			return res, currentline
	else:
		# If we were not able to find the closing parenthesis, return failure
		if nopenparenthesis > 0:
			return -1, None
		else:
		# If we were able to find the closing parenthesis, return current char
		# and current line
			return res, line

# findClosingBrackets (line, pos, lines)
#  finds the matching closing brackets for the open parenthesis that is on
#  position "pos" in line "line". If the closing bracket is not on that line,
#  keep searching in subsequent "lines"
#  CAUTION: IGNORES COMMENTS!
def findClosingBrackets (line, pos, lines):
	res = -1
	nopenbrackets = 1
	s = lines[line][pos+1:]
	while nopenbrackets > 0:
		# Check for closing bracket that matches this opening bracket
		for i in range(0, len(s)):
			if s[i] == '{':
				nopenbrackets = nopenbrackets + 1
			elif s[i] == '}':
				nopenbrackets = nopenbrackets - 1
				if nopenbrackets == 0:
					res = line
					break
		# Process next line if there are pending open brackets
		if nopenbrackets > 0:
			line = line + 1
			s = lines[line]
	return res

#
# searchForEndOfDeclarationOrImplementation_C (startline, lines)
#  checks from startline whether the following symbol is a declaration symbol
#  or an function implementation
#
def searchForEndOfDeclarationOrImplementation_C (startlineno, lines):
	endlineno = startlineno

	l = lines[startlineno]
	# Search for end of declaration (;) or begin of implementation ({) chars.
	# If this is an implementation, then we have to identify where the
	# implementation finishes
	declaration_pos = l.find (";")
	implementation_pos = l.find ("{")

	if declaration_pos >= 0 and implementation_pos >= 0:
		if declaration_pos > implementation_pos:
			endlineno = findClosingBrackets (startlineno, implementation_pos, lines)
		else:
			pass
	elif declaration_pos >= 0 and implementation_pos < 0:
		pass
	elif declaration_pos < 0 and implementation_pos >= 0:
		endlineno = findClosingBrackets (startlineno, implementation_pos, lines)
	elif declaration_pos < 0 and implementation_pos < 0:
		if startlineno+1 < len(lines):
			return searchForEndOfDeclarationOrImplementation_C (startlineno+1, lines)
		else:
			pass
	return endlineno

#
# extractArraySectionComponents_C(var_component)
#   given a variable component (variable name, plus array section), the routine
#   generates a tuple consisting of the variable name and a list of rangemin/rangemax
#   pairs of the sectioned array dimensions
#   e.g.
#     _filter[0:_size][0:_size] --> [ ('_filter', [('0', '_size'), ('0', '_size') ]
#     _var[1:_size1][2:_size2][3:_size3] --> [('_var', [('1', '_size1'), ('2', '_size2'), ('3', '_size3')])]
#
def extractArraySectionComponents_C(var_component):
	var_regex = re.compile(r'\w+(\[[-/\+\*\w]*:[-/\+\*\w]+\])+', re.IGNORECASE) # varname[x*:y]
	array_sections_regex = re.compile(r'\[[-/\+\*\w]*:[-/\+\*\w]+\]', re.IGNORECASE) # [x*:y]
	result = []
	if '[' in var_component:
		v = var_regex.findall (var_component)
		if '[' in var_component:
			varname = var_component[0:var_component.find ("[")]
			array_sections = array_sections_regex.findall (var_component[var_component.find("["):])
			sections_result = []
			for s in array_sections:
				offset = s[s.find("[")+1 : s.find(":")]
				length = s[s.find(":")+1 : s.find("]")]
				sections_result.append ( (offset, length) )
			result.append ( (varname, sections_result) )
		else:
			pass # Ignore non-array variables
	return result
#
# extractArraySectionComponents_Fortran(var_component)
#   given a variable component (variable name, plus array section), the routine
#   generates a tuple consisting of the variable name and a list of rangemin/rangemax
#   pairs of the sectioned array dimensions
#   e.g.
#     _filter(0:_size,0:_size) --> [ ('_filter', [('0', '_size'), ('0', '_size') ]
#     _var(1:_size1,2:_size2,3:_size3) --> [('_var', [('1', '_size1'), ('2', '_size2'), ('3', '_size3')])]
#
def extractArraySectionComponents_Fortran(var_component):
	var_regex = re.compile(r'\w+\([-/\+\*\w]*:[-/\+\*\w]+(,\([-/\+\*\w]*:[-/\+\*\w]+)\)*', re.IGNORECASE) # varname (x1*:y1,x2*:y2)
	result = []
	if '(' in var_component:
		v = var_regex.findall (var_component)
		if '(' in var_component:
			varname = var_component[0:var_component.find ("(")]
			sections = var_component[var_component.find("(")+1:-1]
			sections_result = []
			cnt = 1
			for s in sections.split(","):
				offset = s[:s.find(":")]
				length = s[s.find(":")+1:]
				sections_result.append ( (offset, length) )
				cnt = cnt + 1
			result.append ( (varname, sections_result) )
		else:
			pass # Ignore non-array variables
	return result

#
# extractArraySections_C
#   extracts the array (name), the direction [map-type modifier] and information
#   about the array sections provided by the developer. For each direction, it
#   generates a list of tuples of variable names and the array sections indicated.
#   For instance:
#     map(to:_filter[0:_size][0:_size]) map(alloc:_var[1:_size1][2:_size2][3:_size3],_var2[10:20])
#   gets splitted into two components (one for to and for alloc directions), and then each
#   record it generates a tuple of variable + list of rangemin/rangemax pairs
#     1) [('to', [('_filter', [('0', '_size'), ('0', '_size')])])
#     2) ('alloc', [('_var', [('1', '_size1'), ('2', '_size2'), ('3', '_size3')])]), ('alloc', [('_var2', [('10', '20')])])]
#
def extractArraySections_C (omp_construct):
	result = []
	# e.g.  map(to:_filter[0:_size1][0:_size2],_filter2[1:N])
	for portion in omp_construct:
		portion_begin = portion.find ("(")
		# Search for closing parenthesis -- but within the line, so we don't pass
		# subsequent lines
		portion_end,_ = findClosingParenthesis (portion, portion_begin, None, None)
		portion_direction = portion[portion_begin+1:portion.find(":")]
		remaining = portion[portion.find(":")+1:portion_end]
		for s in remaining.split(","):
			result.append ( (portion_direction, extractArraySectionComponents_C (s) ) )
	return result
#
# extractArraySections_Fortran
#   extracts the array (name), the direction [map-type modifier] and information
#   about the array slices provided by the developer. For each direction, it
#   generates a list of tuples of variable names and the array slices indicated.
#   For instance:
#     map(to:_filter(0:_size,0:_size)) map(alloc:_var(1:_size1,2:_size2,3:_size3),_var2(10:20))
#   gets splitted into two components (one for to and for alloc directions), and then each
#   record it generates a tuple of variable + list of rangemin/rangemax pairs
#     1) [('to', [('_filter', [('0', '_size'), ('0', '_size')])])
#     2) ('alloc', [('_var', [('1', '_size1'), ('2', '_size2'), ('3', '_size3')])]), ('alloc', [('_var2', [('10', '20')])])]
#
def extractArraySections_Fortran (omp_construct):
	result = []
	# e.g.  map(to:_filter[0:_size1][0:_size2],_filter2[1:N])
	for portion in omp_construct:
		portion_begin = portion.find ("(")
		# Search for closing parenthesis -- but within the line, so we don't pass
		# subsequent lines
		portion_end,_ = findClosingParenthesis (portion, portion_begin, None, None)
		portion_direction = portion[portion_begin+1:portion.find(":")]
		remaining = portion[portion.find(":")+1:]
		while '(' in remaining:
			section_begin = remaining.find("(")
			section_end,_ = findClosingParenthesis (remaining, section_begin, None, None)
			s = remaining[:section_end+1]
			result.append ( (portion_direction, extractArraySectionComponents_Fortran (s) ) )
			remaining = remaining[section_end+1:]
			if ',' not in remaining:
				break
			remaining = remaining[remaining.find(",")+1:]
	return result

# vim:set noexpandtab tabstop=4:
