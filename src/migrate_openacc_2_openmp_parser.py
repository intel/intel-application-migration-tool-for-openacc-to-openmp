#
# Code generation module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP*"
#

import migrate_openacc_2_openmp_constants as CONSTANTS
import migrate_openacc_2_openmp_convert as OACC2OMP
import migrate_openacc_2_openmp_tools as TT
import re
import sys

#
# findEndOfLoop_C (lines, startline)
#  find the statement than closes the for loop found in startline
#  CAUTION:
def findEndOfLoop_C (lines, startline):

	curline = startline
	l = lines[curline]

	# TODO: might need to jump some lines to find the opening parenthesis
	# Search for the current for (..) statement to explore.
	if l.find ("for") >= 0 and l.find ("(") > l.find("for"):
		# Now, we have to identify whether this is a for with a one-liner (non-block) stmt,
		# or if it is a for with a code block { }. One way to find between the
		# two is to find the earliest opening block char "{" and/or the
		# statement finish char ";" (semicolon).
		# The one that appears earlier indicates how where is the end of the
		# statement/block
		# NOTE: TODO the semicolon also appears within a for (;;) statement but should
		# be considered as the continuation of a one-liner
		endforstmt_pos,endforstmt_line = TT.findClosingParenthesis (l, l.find ("("), curline, lines)
		# Reload line from the end of the for statement
		curline = endforstmt_line
		l = lines[curline]

		endofstmt = l.find (";", endforstmt_pos)
		begincodeblock = l.find("{", endforstmt_pos)
		forstmt = l.find ("for", endforstmt_pos)

		while True:

			# If we found an end of statement alone, return its line
			if endofstmt >= 0 and begincodeblock == -1 and forstmt == -1:
				return curline
			# If we found the beginning of a code block, search for the block end
			elif endofstmt == -1 and begincodeblock >= 0 and forstmt == -1:
				return TT.findClosingBrackets (curline, begincodeblock, lines)
			# If we found the beginning of a new for statement, apply this recursively
			elif endofstmt == -1 and begincodeblock == -1 and forstmt >= 0:
				return findEndOfLoop_C (lines, curline)
			# Since for statements have semicolon (end-of-statement) characters
			# endofstmt and forstmt might be positive
			elif endofstmt >= 0 and begincodeblock == -1 and forstmt >= 0:
				# If so, which happened first?
				if forstmt < endofstmt:
					return findEndOfLoop_C (lines, curline)
				else:
					return curline
			# Nothing was found, search on subsequent lines
			elif endofstmt == -1 and begincodeblock == -1 and forstmt == -1:
				curline = curline + 1
			else:
				print ("Error parsing fors on line no = {}!\nContents = '{}' (endofstmt = {} begincodeblock = {} forstmt = {})".format(curline, l.strip(), endofstmt, begincodeblock, forstmt))

			if curline >= len(lines):
				break
			l = lines[curline]
			endofstmt = l.find (";")
			begincodeblock = l.find("{")
			forstmt = l.find ("for")

	return -1

# findEndOfLoop_FTN (lines, startline)
#  find the statement than closes the do loop found in startline
#  CAUTION: this might need some rework given the simple parsing. For instance,
#  if do/enddo statements are broken into several lines this is unlikely to work.
#  Also, if the statement after startline is empty, this might not work
def findEndOfLoop_FTN (lines, startline):
	curline = startline
	# Now balance dos and enddos
	balance = 0
	while curline < len(lines):
		l = re.sub('[\\s\\t]+', ' ', lines[curline].lower())
		l = re.sub('\\s\\(', '(', l) # Suppress spaces before parenthesis to help parsing
		# Identifying enddos is easy
		if l.find("enddo") >= 0 or l.find ("end do") >= 0:
			balance = balance - 1
		# We accept dos such as "do VAR = 1,N" or "do VAR = 1, N, S"
		elif l.find ("do ") >= 0 and \
		     l.count ('=') == 1 and l.find ("=") > l.find ("do ") and \
		     l.count (',') >= 1 and l.find (",") > l.find ("="):
			balance = balance + 1
		# Finish the parsing when we have balanced dos and enddos
		if balance == 0:
			break
		curline = curline + 1
	if balance == 0:
		return curline
	else:
		return -1

def findEndOfLoop (txConfig, lines, startline):
	if txConfig.Lang == CONSTANTS.FileLanguage.C or txConfig.Lang == CONSTANTS.FileLanguage.CPP:
		return findEndOfLoop_C (lines, startline)
	elif txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed or txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
		return findEndOfLoop_FTN (lines, startline)

# parseBlockComments_C (s, isCommentOpen)
#  Skip the comments from a given statement (s). The routine also considers whether
#  a previous block comment was already opened, and if so, ignore until the close block
#  comment is found
def parseBlockComments_C(s, isCommentOpen):
	if not isCommentOpen:
		commentOpen = False
		if s.find ("/*") == -1: # Return same string if no start-of block comments found
			return s, commentOpen
		# Iteratively remove block comments, until we don't find start-of block comments
		sblock = s.find ("/*")
		eblock = s.find ("*/", sblock)
		if eblock >= 0:
			res = s[:sblock] + s[eblock+len("*/"):]
			while res.find ("/*") >= 0:
				sblock = res.find ("/*")
				eblock = res.find ("*/", sblock)
				if eblock >= 0:
					commentOpen = False
					res = res[:sblock] + res[eblock+len("*/"):]
				else:
					commentOpen = True
					res = res[:sblock]
					break
		else:
			commentOpen = True
			res = s[:sblock]
		return res, commentOpen
	else:
		commentOpen = True
		if s.find ("*/") == -1: # Skip the string if we haven't closed the block comments
			return "", commentOpen
		# find terminating block comment first, and skip till there
		eblock = s.find ("*/")
		res = s[eblock+len("*/"):]
		commentOpen = False
		# Iteratively remove block comments, until we don't find start-of block comments
		while res.find ("/*") >= 0:
			sblock = res.find ("/*")
			eblock = res.find ("*/", sblock)
			if eblock >= 0:
				comentOpen = False
				res = res[:sblock] + res[eblock+len("*/"):]
			else:
				commentOpen = True
				res = res[:sblock]
				break
		return res, commentOpen

# parseFile_C (filename)
#  parses a C/C++ file and collects OpenACC and OpenMP constructs
#  (not considering those in commented blocks)
def parseFile_C(filename):
	ACCconstructs = dict()
	OMPconstructs = dict()
	lines = []
	try:
		with open (filename, "r") as f:
			lines = f.readlines()
			f.close()
	except IOError:
		print (f"Error! File {filename} is not accessible for reading.")
		sys.exit(-1)

	curline = 0
	isCommentLeftOpen = False
	while curline < len(lines):
		construct = ""

		# Read the following code block
		original = lines[curline].strip()
		multiline = lines[curline].strip().endswith("\\")
		bline = curline
		while multiline:
			curline = curline + 1
			original = original[:-1] + lines[curline].strip() # Skip ending \ char
			multiline = lines[curline].strip().endswith("\\")
		eline = curline
		original = re.sub('[\\s\\t]+',' ', original) # Suppress multiple spaces and tabs
		original = re.sub('\\s\\(','(', original) # Suppress spaces before parenthesis to help parsing

		# Process block comments first
		statements, isCommentLeftOpen = parseBlockComments_C (original, isCommentLeftOpen)

		# Check for one-liner comments, if they exist do not process anything beyond that point
		if statements.find ("//") >= 0:
			statements = statements[:statements.find ("//")]

		# Check for OpenACC statements now - preC99 pragmas
		if '#' in statements:
			tmp = statements[statements.find("#")+len("#"):].strip()
			# ... followed by pragma
			if tmp.find ("pragma") >= 0:
				tmp = tmp[tmp.find ("pragma")+len("pragma"):].strip()
				# ... and acc
				if tmp.find ("acc") >= 0:
					construct = tmp[tmp.find("acc")+len("acc"):].strip()
					# Append to construct to be processed
					ACCconstructs[eline] = OACC2OMP.accConstruct( [ original ], construct, bline+1, eline+1)
					# print (bline+1, eline+1, construct)
				elif tmp.find ("omp") >= 0:
					construct = tmp[tmp.find("omp")+len("omp"):].strip()
					# Add two construct "markers", one on begin and one on end lines
					OMPconstructs[bline] = OACC2OMP.ompConstruct( [ original ], construct, bline+1, eline+1)
					OMPconstructs[eline] = OACC2OMP.ompConstruct( [ original ], construct, bline+1, eline+1)
					# print (bline+1, eline+1, construct)

		# Check for OpenACC statements now - C99 pragmas
		if statements.find('_Pragma') >= 0:
			# Search for the open-parenthesis after the _Pragma(
			op = statements.find("(", statements.find('_Pragma'))
			# Search for the close parenthesis matching the open parenthesis
			cp,_ = TT.findClosingParenthesis (statements, op, None, None)
			if cp == -1:
				print (f"Error! Cannot find closing parenthesis on _Pragma around line {curline+1}.")
				sys.exit (-1)
			tmp = statements[op+1:cp]
			# Now search for the starting/ending quotation marks
			oq = tmp.find ("\"")
			cq = tmp.rfind ("\"")
			if cq >= 0 and oq >= 0 and oq < cq:
				tmp = tmp[oq+1:cq].strip()
				# ... and acc
				if tmp.find ("acc") >= 0:
					construct = tmp[tmp.find("acc")+len("acc"):].strip()
					# Append to construct to be processed
					ACCconstructs[eline] = OACC2OMP.accConstruct( [ original ], construct, bline+1, eline+1)
					# print (bline+1, eline+1, construct)
				elif tmp.find ("omp") >= 0:
					construct = tmp[tmp.find("omp")+len("omp"):].strip()
					# Add two construct "markers", one on begin and one on end lines
					OMPconstructs[bline] = OACC2OMP.ompConstruct( [ original ], construct, bline+1, eline+1)
					OMPconstructs[eline] = OACC2OMP.ompConstruct( [ original ], construct, bline+1, eline+1)
					# print (bline+1, eline+1, construct)

		curline = curline + 1

	return lines, ACCconstructs, OMPconstructs, None # Last None refers to UDT definitions

# getNextStatement_FTN_FX (lines, curline):
#  parses a fortran statement, which can be splitted in multiple lines on a FTN FX form
def getNextStatement_FTN_FX(lines, curline):

	l = lines[curline].lower()

	# if this is a commented line, skip it
	if len(l) == 0 or (len(l) > 0 and l[0] in ['c', 'C', '!', '*']):
		return "", curline+1
	else:
		l = l[6:] # Skip fixed cols
		# Ignore whatever comes next the comment
		comment_pos = l.find ('!')
		if comment_pos >= 0: 
			l = l[:comment_pos]

	if len(l) > 0:
		# Process continuation lines
		while True:
			tmp = lines[curline+1]

			if len(tmp) > 0 and tmp[0] in ['c', 'C', '!', '*']:
				# If this is a comment, search for next line
				curline = curline + 1
				continue
			else:
				# Is next line a continuation line?
				if len(tmp) > 5 and not (tmp[5] in [' ', '0']):
					comment_pos = tmp.find ('!')
					if comment_pos < 0:
						l = l + tmp[6:] # Append full line into statement
					else:
						l = l + tmp[6:comment_pos] # Append up to comment position
					curline = curline + 1
				else:
					# If not and stop
					break

	l = l.strip()
	l = re.sub ('[\\s\\t]+', ' ', l.lower())
	l = re.sub ('\\s\\(', '(', l)

	return l, curline+1

# getUserDerivedType_FTN_FX (lines, curline):
#  parses a fortran (in fixed) for a user derived type
def getUserDerivedType_FTN_FX (lines, curline):

	bline = curline
	typename = None
	members = []

	stmt, curline = getNextStatement_FTN_FX (lines, curline)

	# Is this an extended derived type using type :: format ?
	if stmt.find ("::") >= 0:
		typename = stmt[stmt.find("::")+len("::"):].strip()
	else:
		typename = stmt[len("type "):].strip()

	while curline < len(lines):
		stmt, curline = getNextStatement_FTN_FX (lines, curline)
		if len(stmt) >= len("end type") and stmt.lower().startswith ("end type"):
			break
		elif len(stmt) > 0:
			members.append (stmt)

	eline = curline

	return typename, members, bline, eline

# getConstructOnMultiline_FTN_FX(sentinel, lines, curline)
# sentinel = "acc" or "omp"
# lines = lines read from input file
# curline = current/starting line to process
#
def getConstructOnMultiline_FTN_FX(sentinel, lines, curline):

	construct = ""
	original = [ ]
	begin_line = curline
	last_line_with_contents = curline # We keep track of the last line with contents of interest
	                                  # This will help us ingnore trailing commented / empty lines

	multiline = True
	while multiline:
		l = lines[curline].strip()
		original.append (l)
		l_no_spaces = re.sub('[\\s\\t]+', '', l)
		l = re.sub('[\\s\\t]+', ' ', l.lower()) # Suppress extra spaces and tabs, plus lowercase
		l = re.sub('\\s\\(', '(', l) # Suppress spaces before parenthesis to help parsing

		# If non-empty line
		if len(l_no_spaces) > 0:
			# Check if line begins with proper leading section
			if not (l.startswith("c$" + sentinel) or \
			        l.startswith ("!$" + sentinel) or \
			        l.startswith("*$" + sentinel)) and \
			    l[0] not in ['c','!','*']:
				print (f"Error! Ill-formed construct around line {begin_line+1} when looking for '{sentinel}' sentinel")
				sys.exit(-1)
			# Append into the construct if it contain the sentinel, otherwise the
			# line refers to a comment
			if l.startswith ("c$" + sentinel) or \
			   l.startswith ("!$" + sentinel) or \
			   l.startswith ("*$" + sentinel):
				start_pos = 6
				end_pos = len(l)
				# Skip any possible comment in the line, but skip first which may
				# belong to the sentinel
				if l.find ('!', 1) >= 0:
					end_pos = l.find ('!', 1)
				construct = construct + l[start_pos:end_pos]
			# Process fortran multi-line (i.e. text in col 6)
			# and concatenate lines together for processing it once
			multiline = False
			if curline+1 < len(lines):
				# Check if following line consists of a continuation marker with
				# a charater in column 6
				if len(lines[curline+1]) > 5:
					multiline = multiline or \
					  (lines[curline+1].startswith("c$" + sentinel) or \
					   lines[curline+1].startswith("!$" + sentinel) or \
					   lines[curline+1].startswith("*$" + sentinel) ) \
					  and lines[curline+1][5] != " "
					if multiline:
						last_line_with_contents = curline+1
				# Consider commented out lines as continuation lines, but these cannot
				# contain sentinels with continuation markers (see if above)
				# We have to be careful here - we have to check OpenACC and OpenMP
				# sentinels just in case the input file has the two
				if len(lines[curline+1]) > 0:
					multiline = multiline or \
					  (not lines[curline+1].startswith("c$acc") and
					   not lines[curline+1].startswith("!$acc") and
					   not lines[curline+1].startswith("*$acc") and
					   not lines[curline+1].startswith("c$omp") and
					   not lines[curline+1].startswith("!$omp") and
					   not lines[curline+1].startswith("*$omp") ) \
					  and lines[curline+1][0] in ['c','!','*']
		else:
			# If line was completely empty, go to next line
			multiline = True

		if multiline:
			curline = curline + 1

	# Remove superfluous spaces
	construct = re.sub('[\\s\\t]+', ' ', construct)
	construct = re.sub('\\s\\(', '(', construct) # Suppress spaces before parenthesis to help parsing

	return original, construct.strip(), begin_line, last_line_with_contents # curline

# parseFile_FTN_FX (filename)
#  parses a Fortran file (in fixed format) and collects the OpenACC and OpenMP constructs
#  (not considering those in commented blocks)
def parseFile_FTN_FX(filename):
	ACCconstructs = dict()
	OMPconstructs = dict()
	UDTdefinitions = dict()
	ListFunctionsSubroutines = []

	# We need to take care of functions and subroutines for a good conversion of !$acc routine
	# since !$omp declare target() have to go after implicit/use/import statements
	BeginFunction, EndFunction = None, None
	BeginSubroutine, EndSubroutine = None, None
	LastImplicit, LastUse, LastImport = None, None, None

	lines = []
	try:
		with open (filename, "r") as f:
			lines = f.readlines()
			f.close()
	except IOError:
		print (f"Error! File {filename} is not accessible for reading.")
		sys.exit(-1)

	curline = 0
	while curline < len(lines):
		construct = ""
		l = lines[curline].strip()
		original = [ l ]
		# Convert to lower case and suppress multiple spaces
		l = re.sub('[\\s\\t]+', ' ', l.lower())
		l = re.sub('\\s\\(', '(', l) # Suppress spaces before parenthesis to help parsing

		if len(l) > len("c$acc ") and \
		  l.startswith ("c$acc") or l.startswith ("!$acc") or l.startswith("*$acc"):
			original, construct, begin_line, end_line = getConstructOnMultiline_FTN_FX("acc", lines, curline)
			# Append to construct to be processed
			ACCconstructs[end_line] = OACC2OMP.accConstruct(original, construct, begin_line+1, end_line+1)
			# print (begin_line+1, original)
			# print (begin_line+1, construct[begin_line+1])
			# print (begin_line+1, curline+1, construct)

			# Continue processing from end_line
			curline = end_line

		elif len(l) > len("c$omp ") and \
		  l.startswith ("c$omp") or l.startswith ("!$omp") or l.startswith("*$omp"):
			original, construct, begin_line, end_line = getConstructOnMultiline_FTN_FX("omp", lines, curline)
			# Append to construct to be processed
			OMPconstructs[begin_line] = OACC2OMP.ompConstruct(original, construct, begin_line+1, end_line+1)
			OMPconstructs[end_line] = OACC2OMP.ompConstruct(original, construct, begin_line+1, end_line+1)
			# print (begin_line+1, original)
			# print (begin_line+1, construct[begin_line+1])
			# print (begin_line+1, curline+1, construct)

			# Continue processing from end_line
			curline = end_line

		elif len(l) > len("type") and l.startswith("type") \
		    and not l.startswith ("type("): # skip typed variable creation
			typename, members, begin_line, end_line = getUserDerivedType_FTN_FX (lines, curline)
			UDTdefinitions[end_line] = OACC2OMP.UDTdefinition(typename, members, begin_line+1, end_line+1)

		elif l.find ("end function") >= 0 or l.find ("endfunction") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("end function") or l.find (" end function") >= 0 or \
			   l.startswith ("endfunction") or l.find (" endfunction"):
				EndFunction = curline + 1
				x = generateFunctionSubroutineLimits_FTN_FR(BeginFunction, EndFunction, LastImplicit, LastUse, LastImport)
				ListFunctionsSubroutines.append (x)
				BeginFunction, EndFunction = None, None
				LastImplicit, LastUse, LastImport = None, None, None

		elif l.find ("function") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("function") or l.find (" function ") >= 0:
				BeginFunction = curline + 1

		elif l.find("end subroutine") >= 0 or l.find ("endsubroutine") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("end subroutine") or l.find (" end subroutine") >= 0 or \
			   l.startswith ("endsubroutine") or l.find (" endsubroutine") >= 0:
				EndSubroutine = curline + 1
				x = generateFunctionSubroutineLimits_FTN_FR(BeginSubroutine, EndSubroutine, LastImplicit, LastUse, LastImport)
				ListFunctionsSubroutines.append (x)
				BeginFunction, EndFunction = None, None
				LastImplicit, LastUse, LastImport = None, None, None

		elif l.find("subroutine") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("subroutine") or l.find (" subroutine ") >= 0:
				BeginSubroutine = curline + 1

		elif l.startswith ("use"):
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			LastUse = curline + 1

		elif l.startswith ("implicit"):
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			LastImplicit = curline + 1

		elif l.startswith ("import"):
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			LastImport = curline + 1

		curline = curline + 1

	return lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFunctionsSubroutines


# getConstructOnMultiline_FTN_FR(sentinel, lines, curline)
# sentinel = "!$acc" or "!$omp"
# lines = lines read from input file
# curline = current/starting line to process
# 
def getConstructOnMultiline_FTN_FR(sentinel, lines, curline):

	construct = ""
	original = [ ]
	begin_line = curline

	# Process fortran multi-line (i.e. finished with & // or text in col 6)
	# and concatenate lines together for processing it once
	multiline = True

	while multiline:
		construct = construct[:-1] # do not include multi-line trailing & char in Fortran/Free form

		l = lines[curline].strip()
		original.append (l)

		# Work with lower-case constructs / clauses
		l = l.lower()

		# Remove comments if present, but remind to search after  the sentinel if it exists
		comment_pos = None
		if l.find (sentinel) >= 0:
			comment_pos = l.find ('!', l.find(sentinel)+1)
		else:
			comment_pos = l.find ('!')
		if comment_pos >= 0:
			l = l[:comment_pos]
			l = l.strip()

		l_no_spaces = re.sub('[\\s\\t]+', '', l) # Line without spaces at all

		l = re.sub('[\\s\\t]+', ' ', l) # Suppress extra spaces and tabs
		l = re.sub('\\s\\(', '(', l) # Suppress spaces before parenthesis to help parsing

		# Skip if empty line
		if len(l_no_spaces) > 0:
			# check for continuation construct sentinel
			marker_pos = l.find (sentinel)
			# if found, parse from that point
			if marker_pos >= 0:
				l = l[marker_pos+len(sentinel)+1:]
			else:
				print (f"Error! Missing {sentinel} in line {curline+1}")
				sys.exit(-1)
			# given continuation & multi-line char? -- but exclude last for continuation
			continue_optional_pos = l.find ("&", 0, len(l)-1)
			if continue_optional_pos >= 0:
				start_pos = continue_optional_pos+1 # skip to first &, if given
			else:
				start_pos = 0
			# append to the construct we're processing
			# we may need an extra space, only for subsequent lines
			construct = construct + (" " if curline !=  begin_line else "") + l[start_pos:]
			# If line finishes with & again, process next line
			multiline = construct.endswith ("&")
		else:
			multiline = True

		if multiline:
			curline = curline + 1

	# Remove superfluous spaces
	construct = re.sub('[\\s\\t]+', ' ', construct)
	construct = re.sub('\\s\\(', '(', construct) # Suppress spaces before parenthesis to help parsing

	return original, construct, begin_line, curline

# getNextStatement_FTN_FR (lines, curline):
#  parses a fortran statement, which can be splitted in multiple lines on a FTN FR form
def getNextStatement_FTN_FR(lines, curline):

	l = lines[curline].strip()

	if l.find ("!") >= 0: # Remove comments
		l = l[:l.find("!")].strip()

	if len(l) > 0 and l.endswith("&"):
		l = l[:-1] # Remove the ampersand/continuation line
		# Process continuation lines
		while True:
			curline = curline + 1
			tmp = lines[curline].strip()
			# given continuation & multi-line char? -- but exclude last for continuation
			continue_optional_pos = tmp.find ("&", 0, len(tmp)-1)
			if continue_optional_pos >= 0:
				tmp = tmp[continue_optional_pos+1:]
			if tmp.find ("!") >= 0: # Remove comments
				tmp = tmp[:tmp.find("!")].strip()
			tmp = tmp.strip()
			tmp = re.sub('[\\s\\t]+', ' ', tmp.lower())
			tmp = re.sub('\\s\\(', '(', tmp) # Suppress spaces before parenthesis to help parsing
			if len(tmp) > 0:
				if tmp.endswith("&"):
					l = l + tmp[:-1]
				else:
					l = l + tmp
					break
	return l, curline + 1

# getUserDerivedType_FTN_FR (lines, curline):
#  parses a fortran (in free form) for a user derived type
def getUserDerivedType_FTN_FR (lines, curline):

	bline = curline
	typename = None
	members = []

	stmt, curline = getNextStatement_FTN_FR (lines, curline)

	# Is this an extended derived type using type :: format ?
	if stmt.find ("::") >= 0:
		typename = stmt[stmt.find("::")+len("::"):].strip()
	else:
		typename = stmt[len("type "):].strip()

	while curline < len(lines):
		stmt, curline = getNextStatement_FTN_FR (lines, curline)
		if len(stmt) >= len("end type") and stmt.lower().startswith ("end type"):
			break
		elif len(stmt) > 0:
			members.append (stmt)

	eline = curline

	return typename, members, bline, eline

# generateFunctionSubroutineLimits_FTN_FR
#  generates a triad with information regarding starting and ending line of a function/subroutine
#  and also taking the highest line for IMPLICIT/USE/IMPORT
def generateFunctionSubroutineLimits_FTN_FR(beginline, endline, implicitline, useline, importline):

	maxImplicitUseImport = None
	if implicitline is not None or useline is not None or importline is not None:
		implicitline = 0 if implicitline is None else implicitline
		useline = 0 if useline is None else useline
		importline = 0 if importline is None else importline
		maxImplicitUseImport = max(implicitline, max(useline, importline))

	return beginline, maxImplicitUseImport, endline


# parseFile_FTN_FR (filename)
#  parses a Fortran file (in free format) and collects the OpenACC and OpenMP constructs
#  (not considering those in commented blocks)
def parseFile_FTN_FR(filename):
	ACCconstructs = dict()
	OMPconstructs = dict()
	UDTdefinitions = dict()
	ListFunctionsSubroutines = []

	# We need to take care of functions and subroutines for a good conversion of !$acc routine
	# since !$omp declare target() have to go after implicit/use/import statements
	BeginFunction, EndFunction = None, None
	BeginSubroutine, EndSubroutine = None, None
	LastImplicit, LastUse, LastImport = None, None, None

	lines = []
	try:
		with open (filename, "r") as f:
			lines = f.readlines()
			f.close()
	except IOError:
		print (f"Error! File {filename} is not accessible for reading.")
		sys.exit(-1)

	curline = 0
	while curline < len(lines):
		construct = ""
		l = lines[curline].strip()
		original = [ l ]
		# Convert to lower case and suppress multiple spaces and tabs
		l = re.sub('[\\s\\t]+', ' ', l.lower())
		l = re.sub('\\s\\(', '(', l) # Suppress spaces before parenthesis to help parsing

		if len(l) > len("!$acc ") and l.startswith ("!$acc"):
			original, construct, begin_line, end_line = getConstructOnMultiline_FTN_FR("!$acc", lines, curline)
			# Append to construct to be processed
			ACCconstructs[end_line] = OACC2OMP.accConstruct(original, construct, begin_line+1, end_line+1)
			# print (begin_line+1, original)
			# print (begin_line+1, construct[begin_line+1])
			# print (begin_line+1, curline+1, construct)

			# Continue processing from end_line
			curline = end_line

		elif len(l) > len("!$omp ") and l.startswith ("!$omp"):
			original, construct, begin_line, end_line = getConstructOnMultiline_FTN_FR("!$omp", lines, curline)
			# Append to construct to be processed
			OMPconstructs[begin_line] = OACC2OMP.ompConstruct(original, construct, begin_line+1, end_line+1)
			OMPconstructs[end_line] = OACC2OMP.ompConstruct(original, construct, begin_line+1, end_line+1)
			# print (begin_line+1, original)
			# print (begin_line+1, construct[begin_line+1])
			# print (begin_line+1, curline+1, construct)

			# Continue processing from end_line
			curline = end_line

		elif len(l) > len("type") and l.startswith("type") \
		    and not l.startswith ("type("): # skip typed variable creation
			typename, members, begin_line, end_line = getUserDerivedType_FTN_FR (lines, curline)
			UDTdefinitions[end_line] = OACC2OMP.UDTdefinition(typename, members, begin_line+1, end_line+1)

		elif l.find ("end function") >= 0 or l.find ("endfunction") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("end function") or l.find (" end function") >= 0 or \
			   l.startswith ("endfunction") or l.find (" endfunction"):
				EndFunction = curline + 1
				x = generateFunctionSubroutineLimits_FTN_FR(BeginFunction, EndFunction, LastImplicit, LastUse, LastImport)
				ListFunctionsSubroutines.append (x)
				BeginFunction, EndFunction = None, None
				LastImplicit, LastUse, LastImport = None, None, None

		elif l.find ("function") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("function") or l.find (" function ") >= 0:
				BeginFunction = curline + 1

		elif l.find("end subroutine") >= 0 or l.find ("endsubroutine") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("end subroutine") or l.find (" end subroutine") >= 0 or \
			   l.startswith ("endsubroutine") or l.find (" endsubroutine") >= 0:
				EndSubroutine = curline + 1
				x = generateFunctionSubroutineLimits_FTN_FR(BeginSubroutine, EndSubroutine, LastImplicit, LastUse, LastImport)
				ListFunctionsSubroutines.append (x)
				BeginFunction, EndFunction = None, None
				LastImplicit, LastUse, LastImport = None, None, None

		elif l.find("subroutine") >= 0:
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			if l.startswith ("subroutine") or l.find (" subroutine ") >= 0:
				BeginSubroutine = curline + 1

		elif l.startswith ("use"):
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			LastUse = curline + 1

		elif l.startswith ("implicit"):
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			LastImplicit = curline + 1

		elif l.startswith ("import"):
			# We need to take care of functions and subroutines for a good conversion of !$acc routine
			# since !$omp declare target() have to go after implicit/use/import statements
			LastImport = curline + 1

		curline = curline + 1

	return lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFunctionsSubroutines


# parseFile (filename)
#  parses a C/C++ or a Fortran file and collects OpenACC and OpenMP constructs found in the code
#  (not considering those in commented blocks)
def parseFile(filename, txConfig):

	if txConfig.Lang == CONSTANTS.FileLanguage.C or txConfig.Lang == CONSTANTS.FileLanguage.CPP:
		lines, ACCconstructs, OMPconstructs, UDTdefinitions = parseFile_C (filename)
		return lines, ACCconstructs, OMPconstructs, UDTdefinitions, []
	elif txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed:
		lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFortranFunctionsSubroutines = parseFile_FTN_FX (filename)
		return lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFortranFunctionsSubroutines
	elif txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
		lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFortranFunctionsSubroutines = parseFile_FTN_FR (filename)
		return lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFortranFunctionsSubroutines

# areEmptyLines (txConfig, lines, start, end):
def areEmptyLines (txConfig, lines, start, end):

	if start == end:
		return True
	elif start < end and end <= len(lines):
		areEmpty = True
		cpos = start
		while areEmpty and cpos < end:
			# suppress multiple spaces and tabs for current line
			l = re.sub('[\\s\\t]+', '', lines[cpos])
			areEmpty = len(l) == 0
			cpos = cpos + 1
		return areEmpty
	else:
		return False


# vim:set noexpandtab tabstop=4:
