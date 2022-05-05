#
# Code generation module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP* API"
#

import migrate_openacc_2_openmp_constants as CONSTANTS
import migrate_openacc_2_openmp_tools as TT
import migrate_openacc_2_openmp_parser as PARSER
import migrate_openacc_2_openmp_convert as OACC2OMP

# findFirstSeparator (s, separators, spos)
#  returns the first character matching those in separators list
#  starting at spos position
def findFirstSeparator (s, separators, spos = 0):
	result = len(s)
	for c in separators:
		if c in s[spos:]:
			result = min(result, spos + s[spos:].find(c))
	return result

# splitCodeWords (code, NCOLUMNS)
#  splits a code statement using the comma and space separators with a tenative
#  limit of NCOLUMNS (exception would be a text block without separators longer than NCOLUMNS)
def splitCodeWords (code, NCOLUMNS):
	separators = {" ", ","}
	if len(code) >= NCOLUMNS:
		result = []
		p = findFirstSeparator (code, separators)
		while p != len(code):
			newp = findFirstSeparator (code, separators, p+1)
			if newp > NCOLUMNS:
				result.append (code[:p+1].strip())
				code = code[p+1:]
				p = 0
				if len(code) < NCOLUMNS:
					break
			else:
				p = newp
		result.append (code.strip())
		return result
	else:
		return [code]

#
# removeTargetEndTargetBubbles (txConfig, lines, constructs, suppconstructs)
#
# Removes consecutive $omp target and $omp end target constructs that may be introduced
# when processing $acc kernels constructs.

def removeTargetEndTargetBubbles (txConfig, lines, constructs, supplementaryConstructs):

	# For each "target" construct generated, remove it if the immediate following
	# line is and "end target"
	for line, construct in constructs.items():
		# Check for translated constructs, skip those not translated
		if construct.openmp is not None and "target" in construct.openmp:
			target_line = line
			# Now search for corresponding end target line
			end_target_line = target_line+1
			while end_target_line not in constructs and end_target_line < len(lines):
				end_target_line = end_target_line + 1
			# If lines in between are empty and the next is an end target, we can
			# remove it
			if PARSER.areEmptyLines (txConfig, lines, target_line+1, end_target_line) and \
			    constructs[end_target_line] is not None and \
			    "end target" in constructs[end_target_line].openmp:
				# If we find a bubble, then remove both target and end target from
				# supplementary constructs and then from regular constructs
				c = constructs[target_line].openmp
				c.remove("target")
				supplementaryConstructs[target_line] = c
				c = constructs[end_target_line].openmp
				c.remove("end target")
				constructs[end_target_line].openmp = c

	# For each "target" added through supplementary constructs, check if the immediate
	# subsequent construct is an "end target"
	for line, construct in supplementaryConstructs.items():
		if "target" in construct:
			target_line = line
			# Now search for corresponding end target line
			end_target_line = target_line+1
			while end_target_line not in constructs and end_target_line < len(lines):
				end_target_line = end_target_line + 1
			# If lines in between are empty and the next is an end target, we can
			# remove it
			if PARSER.areEmptyLines (txConfig, lines, target_line+1, end_target_line) and \
			    constructs[end_target_line] is not None and \
			    "end target" in constructs[end_target_line].openmp:
				# If we find a bubble, then remove both target and end target from
				# supplementary constructs and then from regular constructs
				c = supplementaryConstructs[target_line]
				c.remove("target")
				supplementaryConstructs[target_line] = c
				c = constructs[end_target_line].openmp
				c.remove("end target")
				constructs[end_target_line].openmp = c

	return constructs, supplementaryConstructs

#
# generateAlternateMDCode_C (f, c, arraySections)
#  f = file where the alternate code will be dumped
#  c = construct
#  arraySections = description of the array and sections
def generateAlternateMDCode_C(f, c, arraySections):
	enter_or_exit = "enter" if c.startswith ("target enter data") else "exit";
	for part in TT.extractArraySections_C (arraySections):
		direction, varslices = part
		for varslice in varslices:
			varname = varslice[0]
			slices = varslice[1]
			# Skip this code generation if the array is only 1D
			if len(slices) > 1:
				slicesm1 = slices[0:len(slices)-1]
				tailrange = slices[len(slices)-1]
				f.write ("// ATTENTION! The following suggested code is an alternative reference implementation\n")
				f.write ("// ATTENTION! that could be used if {} is a non-contiguous allocated multi-dimensional array\n".format(varname))
				depth = 0;
				sectionprefix = ""
				for r in slicesm1:
					offset, length = r[0], r[1]
					if len(r[0]) == 0:
						offset = 0
					f.write ("// " + " "*2*depth + "#pragma omp target {} data map({}:{}{}[{}:{}])\n".format(enter_or_exit,direction,varname,sectionprefix,offset,length))
					f.write ("// " + " "*2*depth + "for (int _idx{} = 0; _idx{} < {}; ++_idx{})\n".format(depth,depth,length,depth))
					f.write ("// " + " "*2*depth + "{\n")
					sectionprefix = sectionprefix + "[{}+_idx{}]".format(offset, depth)
					depth = depth + 1
				offset, length = tailrange[0], tailrange[1]
				f.write ("// " + " "*2*depth + "#pragma omp target {} data map({}:{}{}[{}:{}])\n".format(enter_or_exit,direction,varname,sectionprefix,offset,length))
				for r in slicesm1:
					depth = depth - 1
					f.write ("// " + " "*2*depth + "}\n")


# generateTranslatedFileC (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename)
#  generates a translation of the input C file.
#   txConfig = tool configuration plus code details (lang, and tool knobs)
#   lines = input file lines
#   ACCconstructs = OpenACC constructs found in lines --> these constructs already have
#       been translated
#   OMPconstructs = OpenMP constructs found in the original code --> to be protected?
#   SupplementaryConstructs = supplementary OpenMP constructs to be added into the translated file (with indices
#       from source file)
#   outfilename = name of the output file
def generateTranslatedFileC (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename):

	openacc_ifdefcondition = txConfig.OpenACCConditionalDefine
	translated_ifdefcondition = txConfig.TranslatedOMPConditionalDefine
	original_ifdefcondition = txConfig.OriginalOMPConditionalDefine
	removeOpenACC = txConfig.SuppressTranslatedOpenACC
	generateAlternateMDCode = txConfig.GenerateMultiDimensionalAlternateCode

	try:
		with open(outfilename, 'w') as f:

			# Process lines one by one
			for i in range(0, len(lines)):
				# If we have to suppress translated OpenACC constructs, check if current line refers to an
				# OpenACC statement
				if removeOpenACC:
					isAnOpenACCConstruct = False
					for k, v in ACCconstructs.items():
						if v.bline <= i+1 and i+1 <= v.eline:
							isAnOpenACCConstruct = True
					if not isAnOpenACCConstruct:
						f.write (lines[i])
				else:
				# If we don't have to suppress OpenACC constructs, emit the line. Potentially with #ifdef
				# guards.
					if openacc_ifdefcondition:
						for k, v in ACCconstructs.items():
							if i+1 == v.bline:
								f.write ("#if defined(" + str(openacc_ifdefcondition) + ")\n")
					f.write (lines[i])
					if openacc_ifdefcondition:
						for k, v in ACCconstructs.items():
							if i+1 == v.eline:
								f.write ("#endif // defined(" + str(openacc_ifdefcondition) + ")\n")

				# If the line refers to an OpenACC construct (indexed by its end line), then emit the translation
				# Make sure we have a translation, if not pass
				# and careful not to emit empty translations
				if i in ACCconstructs and ACCconstructs[i].openmp != None and len(ACCconstructs[i].openmp) > 0:
					# Emit the #ifdef condition if necessary
					if translated_ifdefcondition:
						f.write ("#if defined(" + str(translated_ifdefcondition) + ")\n")
					for c in ACCconstructs[i].openmp:
						# Split the statements for better readability
						splitted_lines = splitCodeWords (c, 72)
						# Emit the statement
						for l in range(0, len(splitted_lines)):
							beginpragma = "#pragma omp " if l == 0 else  ' ' * len("#pragma omp ")
							continuationchar = "\\" if l+1 < len(splitted_lines) else ""
							f.write (beginpragma + splitted_lines[l] + continuationchar + "\n")
						# A 'omp declare target' construct refers to a function offloading. It may
						# be necessary to match this construct with a closing OpenMP construct
						# 'omp end declare target'.
						# So far only implemented for C/C++
						if c.startswith ("declare target"):
							eline = TT.searchForEndOfDeclarationOrImplementation_C (i+1, lines)
							newConstruct = OACC2OMP.accConstruct( [ "**END declare target**" ], "", eline+1, eline+1)
							newConstruct.openmp = [ "end declare target" ]
							ACCconstructs[eline] = newConstruct
						# A 'target enter/exit data' construct might have associated some multi-dimensional
						# data structures. The proposed code should work on contiguous data, but might not
						# work on non-contiguous data. Here, we propose an alternative reference
						# implementation to support non-contiguous data.
						# So far only implemented for C/C++
						if generateAlternateMDCode and \
						    (c.startswith ("target enter data") or c.startswith ("target exit data")):
							generateAlternateMDCode_C(f, c, ACCconstructs[i].AUX)
					# Close the #ifdef condition if it was necessary
					if translated_ifdefcondition:
						f.write ("#endif // defined(" + str(translated_ifdefcondition) + ")\n")
				# Check if next or current lines refer to OpenMP constructs
				#  --> for next, let's add an #if defined(X) BEFORE the construct, so we need
				#      to lookahead of +1 (and +2 when comparing the begin line)
				#  --> on current, let's add an #endif /* X /* AFTER the construct, so
				#      check the current line
				if original_ifdefcondition:
					if i in OMPconstructs and OMPconstructs[i].eline == i+1:
						f.write ("#endif // defined(" + str(original_ifdefcondition) + ")\n")
					if i+1 in OMPconstructs and OMPconstructs[i+1].bline == i+2:
						f.write ("#if defined(" + str(original_ifdefcondition) + ")\n")

				# If we have supplementary lines to be added into the translation, inject them now
				if i in SupplementaryConstructs:
					for s in SupplementaryConstructs[i]:
						f.write ("#pragma omp " + s + "\n")

			f.close()
	except IOError:
		print ("Error! File {} is not accessible for writing.".format(outfilename))
#
# generateAlternateMDCode_Fortran (f, c, arraySections)
#  f = file where the alternate code will be dumped
#  c = construct
#  arraySections = description of the array and slices
def generateAlternateMDCode_Fortran(f, c, arraySections):
	enter_or_exit = "enter" if c.startswith ("target enter data") else "exit";
	for part in TT.extractArraySections_Fortran (arraySections):
		direction, varslices = part
		for varslice in varslices:
			varname = varslice[0]
			slices = varslice[1]
			# Skip this code generation if the array is only 1D
			if len(slices) > 1:
				slicesm1 = slices[0:len(slices)-1]
				tailrange = slices[len(slices)-1]
				f.write ("! ATTENTION! The following suggested code is an alternative reference implementation\n")
				f.write ("! ATTENTION! that could be used if {} is a non-contiguous allocated multi-dimensional array\n".format(varname))
				f.write ("! block\n")
				cnt = 0
				for declvar in slicesm1:
					f.write ("! integer :: idx{}\n".format(cnt))
					cnt = cnt + 1
				depth = 0;
				sectionprefix = ""
				for r in slicesm1:
					offset, length = r[0], r[1]
					f.write ("! " + " "*2*depth + "!$omp target {} data map({}:{}({}{}:{}))\n".format(enter_or_exit,direction,varname,sectionprefix,offset,length))
					f.write ("! " + " "*2*depth + "do idx{} = 1, {}\n".format(depth,length))
					sectionprefix = sectionprefix + "idx{},".format(depth)
					depth = depth + 1
				offset, length = tailrange[0], tailrange[1]
				f.write ("! " + " "*2*depth + "!$omp target {} data map({}:{}({}{}:{}))\n".format(enter_or_exit,direction,varname,sectionprefix,offset,length))
				for r in slicesm1:
					depth = depth - 1
					f.write ("! " + " "*2*depth + "end do ! idx{}\n".format(depth))
				f.write ("! end block\n")


# generateTranslatedFileFortran (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename)
#  generates a translation of the input Fortran file.
#   txConfig = tool configuration plus code details (lang, and tool knobs)
#   lines = input file lines
#   constructs = OpenACC constructs found in lines --> these constructs already have
#       been translated
#   supplines = supplementary constructs to be added into the translated file (with indices
#       from source file)
#   outfilename = name of the output file

def generateTranslatedFileFortran (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename):

	openacc_ifdefcondition = txConfig.OpenACCConditionalDefine
	translated_ifdefcondition = txConfig.TranslatedOMPConditionalDefine
	original_ifdefcondition = txConfig.OriginalOMPConditionalDefine
	removeOpenACC = txConfig.SuppressTranslatedOpenACC
	generateAlternateMDCode = txConfig.GenerateMultiDimensionalAlternateCode

	try:
		with open(outfilename, 'w') as f:

			# Process lines one by one
			for i in range(0, len(lines)):
				# If we have to suppress translated OpenACC constructs, check if current line refers to an
				# OpenACC statement
				if removeOpenACC:
					isAnOpenACCConstruct = False
					for k, v in ACCconstructs.items():
						if v.bline <= i+1 and i+1 <= v.eline:
							isAnOpenACCConstruct = True
					if not isAnOpenACCConstruct:
						f.write (lines[i])
				else:
				# If we don't have to suppress OpenACC constructs, emit the line. Potentially with #ifdef
				# guards
					if openacc_ifdefcondition:
						for k, v in ACCconstructs.items():
							if i+1 == v.bline:
								f.write ("#if defined(" + str(openacc_ifdefcondition) + ")\n")
					f.write (lines[i])
					if openacc_ifdefcondition:
						for k, v in ACCconstructs.items():
							if i+1 == v.eline:
								f.write ("#endif // defined(" + str(openacc_ifdefcondition) + ")\n")

				# If the line refers to an OpenACC construct (indexed by its end line), then emit the translation
				# Make sure we have a translation, if not pass
				# Careful not to emit empty translations
				if i in ACCconstructs and ACCconstructs[i].openmp != None and len(ACCconstructs[i].openmp) > 0:
					# Emit the #ifdef condition if necessary
					if translated_ifdefcondition:
						f.write ("#if defined(" + str(translated_ifdefcondition) + ")\n")
					for c in ACCconstructs[i].openmp:
						# Split the statements for better readability
						splitted_lines = splitCodeWords (c, 64)
						# Emit the statement, use the appropriate language
						if txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
							for l in range(0, len(splitted_lines)):
								f.write ("!$omp " + splitted_lines[l] + ("&" if l+1 < len(splitted_lines) else "") + "\n")
						elif txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed:
							for l in range(0, len(splitted_lines)):
								f.write ("!$omp" + ("& " if l > 0 else " ") + splitted_lines[l] + "\n")
						# A 'target enter/exit data' construct might have associated some multi-dimensional
						# data structures. The proposed code should work on contiguous data, but might not
						# work on non-contiguous data. Here, we propose an alternative reference
						# implementation to support non-contiguous data.
						# So far, only C alternate implementation works -- this is disabled on Fortran
						if False and generateAlternateMDCode and \
						    (c.startswith ("target enter data") or c.startswith ("target exit data")):
							generateAlternateMDCode_Fortran(f, c, ACCconstructs[i].AUX)
					# Close the #ifdef condition if it was necessary
					if translated_ifdefcondition:
						f.write ("#endif // defined(" + str(translated_ifdefcondition) + ")\n")

				# Check if next or current lines refer to OpenMP constructs
				#  --> for next, let's add an #if defined(X) BEFORE the construct, so we need
				#      to lookahead of +1 (and +2 when comparing the begin line)
				#  --> on current, let's add an #endif /* X /* AFTER the construct, so
				#      check the current line
				if original_ifdefcondition:
					if i in OMPconstructs and OMPconstructs[i].eline == i+1:
						f.write ("#endif // defined(" + str(original_ifdefcondition) + ")\n")
					if i+1 in OMPconstructs and OMPconstructs[i+1].bline == i+2:
						f.write ("#if defined(" + str(original_ifdefcondition) + ")\n")

				# If we have SupplementaryConstructs lines to be added into the translation, inject them now
				if i in SupplementaryConstructs:
					for s in SupplementaryConstructs[i]:
						f.write ("!$omp " + s + "\n")

			f.close()
	except IOError:
		print ("Error! File {} is not accessible for writing.".format(outfilename))

# generateTranslatedFile (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename)
#  generates a translation of the input file.
#   txConfig = tool configuration plus code details (lang, and tool knobs)
#   lines = input file lines
#   ACCconstructs = OpenACC constructs found in lines --> these constructs already have
#       been translated
#   OMPconstructs = OpenMP constructs found in original code --> to be protected?
#   SupplementaryConstructs = supplementary OpenMP constructs to be added into the translated file (with indices
#       from source file)
#   outfilename = name of the output file

def generateTranslatedFile (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename):

	if txConfig.Lang == CONSTANTS.FileLanguage.C or txConfig.Lang == CONSTANTS.FileLanguage.CPP:
		generateTranslatedFileC (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename)
	else:
		generateTranslatedFileFortran (txConfig, lines, ACCconstructs, OMPconstructs, SupplementaryConstructs, outfilename)

# vim:set noexpandtab tabstop=4:
