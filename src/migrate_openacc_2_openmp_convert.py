#
# Translation module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP*"
#

import migrate_openacc_2_openmp_tools as TT
import migrate_openacc_2_openmp_constants as CONSTANTS
import migrate_openacc_2_openmp_parser as PARSER
import os
import sys

#
# CLASS: OpenACC construct and its OpenMP translation
#  -- these are build when parsing the input C/Fortran files
class accConstruct:
	def __init__(self, original, construct, beginline, endline):
		self.original = original                 # Original code
		self.construct = construct               # Original construct
		self.bline = beginline                   # Beginning line of the construct
		self.eline = endline                     # End line of the construct
		self.openmp = None                       # OpenMP conversion -- should be a list []
		self.warnings = None                     # List of warnings associated to this translation
		self.hasLoop = False                     # Does it include a loop clause/construct?
		self.AUX = None                          # Auxiliary field. This is specific to the construct
#
# CLASS: OpenMPconstruct
#  -- these are build when parsing the input C/Fortran files
#  -- we only keep begin/end lines for protecting them
class ompConstruct:
	def __init__(self, original, construct, beginline, endline):
		self.original = original                 # Original code
		self.construct = construct               # Original construct
		self.bline = beginline                   # Beginning line of the construct
		self.eline = endline                     # End line of the construct

#
# CLASS: Translation configuration
#  -- basically keeps the translation behavior requested by the user
class txConfiguration:
	def __init__(self, Lang, PresentBehavior, AsyncBehavior, HostDataBehavior,
		  BindingClauses, GenerateMultiDimensionalAlternateCode,
		  OpenACCConditionalDefine, TranslatedOMPConditionalDefine,
		  OriginalOMPConditionalDefine, SuppressTranslatedOpenACC,
		  expKernelsSupport, expRemoveKernelsBubblesSupport):
		self.Lang = Lang
		self.PresentBehavior = PresentBehavior
		self.AsyncBehavior = AsyncBehavior
		self.HostDataBehavior = HostDataBehavior
		self.BindingClauses = BindingClauses
		self.GenerateMultiDimensionalAlternateCode = GenerateMultiDimensionalAlternateCode
		self.OpenACCConditionalDefine = OpenACCConditionalDefine
		self.TranslatedOMPConditionalDefine = TranslatedOMPConditionalDefine
		self.OriginalOMPConditionalDefine = OriginalOMPConditionalDefine
		self.SuppressTranslatedOpenACC = SuppressTranslatedOpenACC
		self.experimentalKernelsSupport = expKernelsSupport
		self.experimentalRemoveKernelsBubblesSupport = expRemoveKernelsBubblesSupport

# List of OpenACC API calls 
ACC_API_calls = dict ([
	( "acc_get_num_devices", "You can use omp_get_num_devices()." ),
	( "acc_set_device_type", "All OpenMP devices are the same. This call should be meaningless." ),
	( "acc_get_device_type", "All OpenMP devices are the same. This call should be meaningless." ),
	( "acc_set_device_num", "You can use omp_set_default_device()." ),
	( "acc_get_device_num", "You can use omp_get_default_device()." ),
	( "acc_get_property", "Unknown translation." ),
	( "acc_init", "This is done automatically by the OpenMP runtime." ),
	( "acc_shutdown", "This is done automatically by the OpenMP runtime." ),
	( "acc_async_test_device", "Unknown translation." ),
	( "acc_async_test_all", "Unknown translation." ),
	( "acc_async_test_all_device", "Unknown translation." ),
	( "acc_wait", "Consider using #pragma omp taskwait." ),
	( "acc_wait_device", "Consider using #pragma omp taskwait." ),
	( "acc_wait_async", "Consider using #pragma omp taskwait." ),
	( "acc_wait_device_async", "Consider using #pragma omp taskwait." ),
	( "acc_wait_all", "Consider using #pragma omp taskwait." ),
	( "acc_wait_all_device", "Consider using #pragma omp taskwait." ),
	( "acc_wait_all_async", "Consider using #pragma omp taskwait." ),
	( "acc_wait_all_device_async", "Consider using #pragma omp taskwait." ),
	( "acc_get_default_async", "Unknown translation." ),
	( "acc_set_default_async", "Unknown translation." ),
	( "acc_on_device", "You can use omp_is_initial_device()." ),
	( "acc_malloc", "You can use omp_target_alloc()." ),
	( "acc_free", "You can use omp_target_free()." ),
	( "acc_copyin", "Consider using #pragma omp target enter data map(to:)." ),
	( "acc_create", "Consider using #pragma omp target enter data map(alloc:)." ),
	( "acc_copyout", "Consider using #pragma omp target enter data map(from:)." ),
	( "acc_delete", "Consider using #pragma omp target exit data map(delete:)." ),
	( "acc_update_device", "Consider using #pragma omp target data update(to:)." ),
	( "acc_update_self", "Consider using #pragma omp target data update(from:)." ),
	( "acc_map_data", "You can use omp_target_associate_ptr()." ),
	( "acc_unmap_data", "You can use omp_target_disassociate_ptr()." ),
	( "acc_deviceptr", "You can use omp_get_mapped_ptr()." ),
	( "acc_hostptr", "Unclear. Consider using the use_device_ptr clause." ),
	( "acc_is_present", "Consider using omp_target_is_present()."),
	( "acc_memcpy_to_device", "You can use omp_target_memcpy()." ),
	( "acc_memcpy_from_device", "You can use omp_target_memcpy()." ),
	( "acc_memcpy_device", "You can use omp_target_memcpy()." ),
	( "acc_attach", "Unknown translation." ),
	( "acc_detach", "Unknown translation." ),
	( "acc_memcpy_d2d", "You can use omp_target_memcpy()." )
])


#
# The following warnings are emitted by the translation tool when
#  certain OpenACC constructs are found.
#
PREDEFINED_WARNINGS = dict ([
	( "atomic_strange_capture_update", "Unexpected capture update clause on atomic."),
	( "collapse_force", "Collapse clause has a force: statement which is not supported on OpenMP."),
	( "hint_kernels", "The kernels construct in OpenACC is a hint to the compiler of where it should look for parallelism. OpenMP does not have a direct translation for this construct."),
	( "kernels_bubbles", "Note on potential empty omp target / omp end target regions created from loop constructs found within kernels constructs."),
	( "ignore_cache", "There is no translation from ACC CACHE into OpenMP. The ACC CACHE is ignored."),
	( "missing_async", "OpenACC and OpenMP differ on asynchronous mechanisms. Check for the translation."),
	( "unsupported_async", "OpenACC and OpenMP differ on asynchronous mechanisms. async is not supported on the translated OpenMP statement."),
	( "missing_independent", "The independent directive has no direct translation into OpenMP."),
	( "loop_auto_not_supported", "The AUTO clause in the loop construct is not currently supported."),
	( "loop_tile_not_supported", "The TILE clause in the loop construct is not currently supported."),
	( "loop_seq_not_supported", "The SEQ clause in the loop construct is not currently supported."),
	( "loop_vector_not_supported", "The VECTOR clause in the loop construct is not currently supported."),
	( "ignored_wait", "The wait construct has been gnored because of the command-line parameters."),
	( "missing_serial_reduction", "Cannot translate the reduction clause in a serial section."),
	( "mismatch_depend_wait_semantics", "Different semantics on depend/wait constructs."),
	( "mismatch_depend_wait_semantics_if", "wait if() has no direct translation into OpenMP."),
	( "unimplemented_routine_parallelism", "The level of parallelism in routine declaration is not supported in OpenMP."),
	( "present_or_X", "The present_or_X construct in OpenACC has been deprecated since 2.5."),
	( "unimplemented_declare_create", "The declare create() is not literally translated into OpenMP, using copyin approach instead."),
	( "unimplemented_declare_deviceresident", "The declare device_resident() is not currently translated into OpenMP."),
	( "unsupported_vector_length_parallel", "The vector_length clause does not have an OpenMP counterpart in a parallel region."),
	( "unsupported_num_gangs_kernels", "The num_gangs clause cannot be mapped into the OpenMP counterpart in a serial target region."),
])

#
# getMultiParenthesisContents (construct, key)
#  merges the contents of multiple clauses (key) found in a construct
#
def getMultiParenthesisContents(construct, key, mergedResults = True):

	_key = str(" ") + key + str ("(")
	contents = "" if mergedResults else []

	# Process construct, even if they appear multiple times
	pos = construct.find (_key) # Check without immediate following space
	while pos >= 0:

		pos_end,_ = TT.findClosingParenthesis (construct, pos, None, None)
		if pos_end == -1:
			print ("Error! Ill-formed construct around '{}'".format(construct))
			sys.exit (-1)
		else:
			# Get the content within the parenthesis. Remove spaces, btw.
			content = construct[pos+len(_key):pos_end].replace (" ", "")
			if mergedResults:
				# Merge the contents into the contents we alread had.
				if len(contents) > 0:
					contents = contents + str(",") + content
				else:
					contents = content
			else:
				# Add into the list
				contents.append (content)

		# Search for the next construct, if any
		pos = construct.find (_key, pos_end) # Check without immediate following space

	return contents

#
# getSingleParenthesisContents (construct, key)
#  returns the contents of the clause(key) found in the construct
#
def getSingleParenthesisContents(construct, key):
	_key = key + str ("(")
	contents = ""

	# Process construct, even if they appear multiple times

	# Check if the key without an immediate following space exists
	pos = construct.find (_key)

	# If key is found, then search for the contents within the parenthesis block
	if pos >= 0:
		pos_end,_ = TT.findClosingParenthesis (construct, pos, None, None)
		if pos_end == -1:
			print ("Error! Ill-formed construct around '{}'".format(construct))
			sys.exit (-1)
		else:
			contents = construct[pos+len(_key):pos_end].replace (" ", "")
	return contents


#
# AUXILIARY functions
#

def translate_oacc2_aux_copy_clauses(txConfig, c):
	omp_clauses = []
	warnings = []

	# Process copy clause
	variables = getMultiParenthesisContents (c.construct, "copy")
	if len(variables) > 0:
		omp_clauses.append ("map(tofrom:{})".format(variables))

	variables = getMultiParenthesisContents (c.construct, "pcopy")
	if len(variables) > 0:
		omp_clauses.append ("map(tofrom:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	variables = getMultiParenthesisContents (c.construct, "present_or_copy")
	if len(variables) > 0:
		omp_clauses.append ("map(tofrom:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	# Process copyin clause
	variables = getMultiParenthesisContents (c.construct, "copyin")
	if len(variables) > 0:
		omp_clauses.append ("map(to:{})".format(variables))

	variables = getMultiParenthesisContents (c.construct, "pcopyin")
	if len(variables) > 0:
		omp_clauses.append ("map(to:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	variables = getMultiParenthesisContents (c.construct, "present_or_copyin")
	if len(variables) > 0:
		omp_clauses.append ("map(to:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	# Process copyout clause
	variables = getMultiParenthesisContents (c.construct, "copyout")
	if len(variables) > 0:
		omp_clauses.append ("map(from:{})".format(variables))

	variables = getMultiParenthesisContents (c.construct, "pcopyout")
	if len(variables) > 0:
		omp_clauses.append ("map(from:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	variables = getMultiParenthesisContents (c.construct, "present_or_copyout")
	if len(variables) > 0:
		omp_clauses.append ("map(from:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	# Process create clause
	variables = getMultiParenthesisContents (c.construct, "create")
	if len(variables) > 0:
		omp_clauses.append ("map(alloc:{})".format(variables))

	variables = getMultiParenthesisContents (c.construct, "pcreate")
	if len(variables) > 0:
		omp_clauses.append ("map(alloc:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	variables = getMultiParenthesisContents (c.construct, "present_or_create")
	if len(variables) > 0:
		omp_clauses.append ("map(alloc:{})".format(variables))
		warnings.append (PREDEFINED_WARNINGS["present_or_X"])

	# Process delete clause
	variables = getMultiParenthesisContents (c.construct, "delete")
	if len(variables) > 0:
		omp_clauses.append ("map(delete:{})".format(variables))

	# Process detach clause
	variables = getMultiParenthesisContents (c.construct, "detach")
	if len(variables) > 0:
		omp_clauses.append ("map(release:{})".format(variables))

	return omp_clauses, warnings


#
# BEGIN STATEMENTS
#

# Translate: ACC ATOMIC ==> OMP ATOMIC
def translate_oacc_2_omp_acc_atomic(c):
	omp_construct = ["atomic"]
	omp_clauses = []
	warnings = []

	# Check for atomic-clauses
	update_pos = c.construct.find ("update")
	read_pos = c.construct.find ("read")
	write_pos = c.construct.find ("write")
	capture_pos = c.construct.find ("capture")

	if capture_pos != -1 and update_pos != -1:
		if update_pos < capture_pos:
			omp_clauses.append ("update capture")
		else:
			warnings.append ( PREDEFINED_WARNINGS["atomic_strange_capture_update"] )
			omp_clauses.append ("update capture")
	elif read_pos != -1:
		omp_clauses.append ("read")
	elif write_pos != -1:
		omp_clauses.append ("write")
	elif update_pos != -1:
		omp_clauses.append ("update")
	elif capture_pos != -1:
		omp_clauses.append ("capture")

	# Store data back into the construct class
	c.openmp = [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC CACHE ==> []
def translate_oacc_2_omp_acc_cache(c):
	omp_construct = []
	warnings = [ PREDEFINED_WARNINGS["ignore_cache"] ]

	# Store data back into the construct class
	c.openmp = omp_construct
	c.warnings = warnings

# Translate: ACC DATA ==> OMP TARGET DATA
def translate_oacc_2_omp_acc_data(txConfig, c):
	omp_construct = ["target data"]
	omp_clauses = []
	warnings = []

	# Process create, copy, copyin, copyout clauses
	omp_clauses, warn_aux = translate_oacc2_aux_copy_clauses (txConfig, c)
	warnings.extend (warn_aux)

	# Process present clause
	variables = getMultiParenthesisContents (c.construct, "present")
	if len(variables) > 0:
		if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
			omp_clauses.append ("map(alloc:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
			omp_clauses.append ("map(tofrom:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
			omp_clauses.append ("map(present,tofrom:{})".format(variables))

	# Process deviceptr clause
	variables = getMultiParenthesisContents (c.construct, "deviceptr")
	if len(variables) > 0:
		omp_clauses.append ("is_device_ptr({})".format(variables))

	# Process if
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process default clause -- emit a warning on default(none)
	defaultv = getSingleParenthesisContents (c.construct, "default")
	if len(defaultv) > 0:
		# OpenACC firstprivatizes scalars even when default() is given,
		# so we apply defaultmap with the requested modified to the
		# remaining variables (aggregate, pointer and allocatable).
		if defaultv == "present":
			# We have to honor user's request on how to process the
			# present clause
			if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
				omp_clauses.append ("defaultmap(alloc:aggregate)")
				omp_clauses.append ("defaultmap(alloc:pointer)")
				omp_clauses.append ("defaultmap(alloc:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
				omp_clauses.append ("defaultmap(tofrom:aggregate)")
				omp_clauses.append ("defaultmap(tofrom:pointer)")
				omp_clauses.append ("defaultmap(tofrom:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
				omp_clauses.append ("defaultmap(present:aggregate)")
				omp_clauses.append ("defaultmap(present:pointer)")
				omp_clauses.append ("defaultmap(present:allocatable)")
		elif defaultv == "none":
			omp_clauses.append ("defaultmap(none:aggregate)")
			omp_clauses.append ("defaultmap(none:pointer)")
			omp_clauses.append ("defaultmap(none:allocatable)")

	# Store data back into the construct class
	c.openmp = [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC ENTER DATA ==> OMP TARGET ENTER DATA
def translate_oacc_2_omp_acc_enter_data(txConfig, c):
	pre_constructs = []
	omp_construct = ["target enter data"]
	omp_clauses = []
	warnings = []

	# Process create, copy, copyin, copyout clauses
	omp_clauses, warn_aux = translate_oacc2_aux_copy_clauses (txConfig, c)
	warnings.extend (warn_aux)

	# Save the copy/creation constructs for its later use
	c.AUX = omp_clauses

	# Process if
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process wait clause
	if c.construct.find(" wait(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
		else:
			pre_constructs = ["taskwait"]
			warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / async clause
	if c.construct.find(" async(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			pass
		elif txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.NOWAIT:
			omp_clauses.append ("nowait")
		warnings.append (PREDEFINED_WARNINGS["missing_async"])

	# Store data back into the construct class
	c.openmp = pre_constructs + [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC EXIT DATA ==> OMP TARGET EXIT DATA
def translate_oacc_2_omp_acc_exit_data(txConfig, c):
	pre_constructs = []
	omp_construct = ["target exit data"]
	omp_clauses = []
	warnings = []

	# Process create, copy, copyin, copyout clauses
	omp_clauses, warn_aux = translate_oacc2_aux_copy_clauses (txConfig, c)
	warnings.extend (warn_aux)

	# Save the copy/creation constructs for its later use
	c.AUX = omp_clauses

	# Process if
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process wait clause
	if c.construct.find(" wait(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
		else:
			pre_constructs = ["taskwait"]
			warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / async clause
	if c.construct.find(" async(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			pass
		elif txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.NOWAIT:
			omp_clauses.append ("nowait")
		warnings.append (PREDEFINED_WARNINGS["missing_async"])

	# Store data back into the construct class
	c.openmp = pre_constructs + [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC HOST DATA ==> OMP TARGET DATA
def translate_oacc_2_omp_acc_host_data(txConfig, c, carryOnStatus):
	omp_construct = []
	omp_clauses = []
	warnings = []

	if txConfig.HostDataBehavior == CONSTANTS.HostDataBehavior.TARGET_DATA:
		omp_construct = ["target data"]
		# Process !$acc host_data use_device(sbuf11,sbuf12,rbuf11,rbuf12)
		variables = getMultiParenthesisContents (c.construct, "use_device")
		if len(variables) > 0:
			omp_clauses.append ("use_device_ptr({})".format(variables))
	elif txConfig.HostDataBehavior == CONSTANTS.HostDataBehavior.TARGET_UPDATE:
		omp_construct = ["target update"]
		# Process !$acc host_data use_device(sbuf11,sbuf12,rbuf11,rbuf12)
		variables = getMultiParenthesisContents (c.construct, "use_device")
		if len(variables) > 0:
			omp_clauses.append ("from({})".format(variables))

	# Process if
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Store data back into the construct class
	c.openmp = [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

	# The closing (end) acc_host may need the variables in the opening (begin)
	# acc_host section
	carryOnStatus["host_data"] = variables

	return carryOnStatus

# Translate: ACC KERNELS ==> OMP TARGET TEAMS
def translate_oacc_2_omp_acc_kernels (lines, txConfig, c, carryOnStatus):
	pre_constructs = []
	omp_construct = ["target"]
	omp_clauses = []
	warnings = [ PREDEFINED_WARNINGS["hint_kernels"] ]

	# do we have a worksharing (loop) construct ?
	if c.construct.find (" loop") >= 0:
		omp_construct = ["target teams"]
		c.hasLoop = True
		carryOnStatus, _ = translate_oacc_2_omp_acc_loop(None, txConfig, c, carryOnStatus, None)
	else:
		# If not, we will identify the block for potential nested !$acc loop
		# constructs so that these can run in parallel
		# We identify the block with a simple entry on carryOnStatus if we're
		# parsing fortran, and the end of the subsequent block if we're
		# parsing C/C++
		if txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed or txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
			# Look if a BLOCK/END_BLOCK follows.
			if lines[c.eline].lower().find (" block") >= 0:
				begin_block = c.eline
				end_block = 0
				for l in range(c.eline+1, len(lines)):
					if lines[l].lower().find ("end block") >= 0 or \
					   lines[l].lower().find ("endblock") >= 0:
						end_block = l
						break
				if end_block == 0:
					print ("Error! Cannot find the matching closing end block for block on line {}".format(begin_line+1))
					sys.exit (-1)
				else:
					carryOnStatus["within_kernels_range"] = [ begin_block+1, end_block+1 ]
			# If not, then we're likely to be finding an acc kernels + acc end kernels construct
			# Mark that we're inside a kernels section, and this mark will be removed upon finding
			# the acc end kernels
			else:
				carryOnStatus["within_kernels"] = True
		elif txConfig.Lang == CONSTANTS.FileLanguage.C or txConfig.Lang == CONSTANTS.FileLanguage.CPP:
			# Look if follows a block {} or a statement. If the former, search for the
			# closing bracket (end of block). If the latter, apply only to next statement
			# Recall -- lines in constructs range 1..NLINES
			block_pos = lines[c.eline].find ("{")
			if block_pos >= 0:
				num = TT.findClosingBrackets (c.eline, block_pos, lines)
				carryOnStatus["within_kernels_range"] = [ c.eline+1, num+1 ]
			else:
				carryOnStatus["within_kernels_range"] = [ c.eline+1, c.eline+1 ]
		else:
			pass

	# Process create, copy, copyin, copyout clauses
	omp_clauses, warn_aux = translate_oacc2_aux_copy_clauses (txConfig, c)
	warnings.extend (warn_aux)

	# Process present clause
	variables = getMultiParenthesisContents (c.construct, "present")
	if len(variables) > 0:
		if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
			omp_clauses.append ("map(alloc:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
			omp_clauses.append ("map(tofrom:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
			omp_clauses.append ("map(present,tofrom:{})".format(variables))

	# Process deviceptr clause
	variables = getMultiParenthesisContents (c.construct, "deviceptr")
	if len(variables) > 0:
		omp_clauses.append ("use_device_ptr({})".format(variables))

	# Process if(x)
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process num_gangs(x)
	if (CONSTANTS.BindingClauses.GANG & txConfig.BindingClauses) != 0:
		n = getSingleParenthesisContents (c.construct, "num_gangs")
		if len(n) > 0:
			if omp_construct == ["target teams"]:
				omp_clauses.append ("num_teams({})".format(n))
			else:
				warnings.append (PREDEFINED_WARNINGS["unsupported_num_gangs_kernels"])

	# Process num_workers(x)
	if (CONSTANTS.BindingClauses.WORKER & txConfig.BindingClauses) != 0:
		n = getSingleParenthesisContents (c.construct, "num_workers")
		if len(n) > 0:
			omp_clauses.append ("thread_limit({})".format(n))

	# Process vector_length(x)
	if (CONSTANTS.BindingClauses.VECTOR & txConfig.BindingClauses) != 0:
		n = getSingleParenthesisContents (c.construct, "vector_length")
		if len(n) > 0:
			warnings.append (PREDEFINED_WARNINGS["unsupported_vector_length_parallel"])

	# Process default clause -- emit a warning on default(none)
	defaultv = getSingleParenthesisContents (c.construct, "default")
	if len(defaultv) > 0:
		# OpenACC firstprivatizes scalars even when default() is given,
		# so we apply defaultmap with the requested modified to the
		# remaining variables (aggregate, pointer and allocatable).
		if defaultv == "present":
			# We have to honor user's request on how to process the
			# present clause
			if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
				omp_clauses.append ("defaultmap(alloc:aggregate)")
				omp_clauses.append ("defaultmap(alloc:pointer)")
				omp_clauses.append ("defaultmap(alloc:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
				omp_clauses.append ("defaultmap(tofrom:aggregate)")
				omp_clauses.append ("defaultmap(tofrom:pointer)")
				omp_clauses.append ("defaultmap(tofrom:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
				omp_clauses.append ("defaultmap(present:aggregate)")
				omp_clauses.append ("defaultmap(present:pointer)")
				omp_clauses.append ("defaultmap(present:allocatable)")
		elif defaultv == "none":
			omp_clauses.append ("defaultmap(none:aggregate)")
			omp_clauses.append ("defaultmap(none:pointer)")
			omp_clauses.append ("defaultmap(none:allocatable)")

	# Process wait clause
	if c.construct.find(" wait(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
		else:
			pre_constructs = ["taskwait"]
			warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / async clause
	if c.construct.find(" async(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			pass
		elif txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.NOWAIT:
			omp_clauses.append ("nowait")
		warnings.append (PREDEFINED_WARNINGS["missing_async"])

	# Store data back into the construct class
	#  keep those already collected in c.openmp/warnings if this
	#  construct has the loop/ws clause
	c.openmp = pre_constructs + [ " ".join(omp_construct + (c.openmp if c.hasLoop else []) + omp_clauses) ]
	c.warnings = warnings + (c.warnings if c.hasLoop else [])

	return carryOnStatus


# Translate: ACC LOOP ==> <multiple depending on config>
def translate_oacc_2_omp_acc_loop(lines, txConfig, c, carryOnStatus, SupplementaryConstructs):
	c.hasLoop = True

	omp_clauses = []
	warnings = []
	pre_constructs = []

	# EXPERIMENTAL
	# We can handle loop constructs inside kernel construcs in Fortran by
	# splitting the region using multiple target regions. 
	if txConfig.experimentalKernelsSupport and \
	   (txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed or txConfig.Lang == CONSTANTS.FileLanguage.FortranFree):

		# Are we inside a kernels construct?
		insideKernelsConstruct = False
		if "within_kernels" in carryOnStatus:
			insideKernelsConstruct = True
		elif "within_kernels_range" in carryOnStatus:
			begin, end = carryOnStatus["within_kernels_range"]
			if c.bline >= begin and c.eline <= end:
				insideKernelsConstruct = True

		# If we are inside a kernels construct, check that we're not already
		# inside a kernels + loop -- or, in other words, is this loop we're
		# processing a nested loop?
		nestedLoopConstruct = False
		if insideKernelsConstruct:
			if "within_kernels_and_loop_range" in carryOnStatus:
				begin, end = carryOnStatus["within_kernels_and_loop_range"]
				if c.bline >= begin and c.eline <= end:
					nestedLoopConstruct = True

		# If we found a loop construct inside a kernels that is not nested, then
		# we delimit which lines does this construct spans so that we can later
		# check if there is a nested loop construct in this range
		if insideKernelsConstruct and not nestedLoopConstruct:
			EndOfLoopLine = PARSER.findEndOfLoop (txConfig, lines, c.eline)
			if EndOfLoopLine != -1:
				carryOnStatus["within_kernels_and_loop_range"] = [c.eline, EndOfLoopLine]
			else:
				print ("Error! Cannot determine end of loop starting at line {}".format(c.eline+1))
				sys.exit (-1)

		# We emit a new code region with a parallel loop in OpenMP
		# (end target + target teams loop) if this acc loop is within a kernels
		# and it is note nested
		# NOTE: We don't need the end target teams loop because this construct
		# is derived from the end of the loop. So we only add end target
		if insideKernelsConstruct and not nestedLoopConstruct:
			pre_constructs = ["end target"]
			omp_construct = ["target teams loop"]
			if SupplementaryConstructs is None:
				print ("Error! Supplementary constructs cannot be None!")
				sys.exit (-1)
			# Add start of next target region immediately after the loop
			if EndOfLoopLine not in SupplementaryConstructs:
				SupplementaryConstructs[EndOfLoopLine] = ["target"]
			else:
				SupplementaryConstructs[EndOfLoopLine].append ("target")
			warnings.append ( PREDEFINED_WARNINGS["kernels_bubbles"] )
		else:
			omp_construct = ["loop"]
	else:
		omp_construct = ["loop"]

	# Process private clause
	variables = getMultiParenthesisContents (c.construct, "private")
	if len(variables) > 0:
		omp_clauses.append ("private({})".format(variables))

	# Process reduction clause
	reductions = getMultiParenthesisContents (c.construct, "reduction", False)
	if len(reductions) > 0:
		for r in reductions:
			omp_clauses.append ("reduction({})".format(r))

	# Process possible bindings
	if (CONSTANTS.BindingClauses.GANG & txConfig.BindingClauses) != 0:
		if c.construct.find ("gang") >= 0:
			omp_clauses.append ("bind(teams)")
	if (CONSTANTS.BindingClauses.WORKER & txConfig.BindingClauses) != 0:
		if c.construct.find ("worker") >= 0:
			omp_clauses.append ("bind(thread)")
	if (CONSTANTS.BindingClauses.VECTOR & txConfig.BindingClauses) != 0:
		# Check first if vector has a given parameter
		if c.construct.find ("vector(") >= 0:
			warnings.append (PREDEFINED_WARNINGS["loop_vector_not_supported"])
		# Check now if vector has no parameters
		elif c.construct.find ("vector") >= 0:
			warnings.append (PREDEFINED_WARNINGS["loop_vector_not_supported"])

	# Process other clauses
	if c.construct.find ("auto") >= 0:
		warnings.append ( PREDEFINED_WARNINGS["loop_auto_not_supported"] )
	if c.construct.find ("seq") >= 0:
		warnings.append ( PREDEFINED_WARNINGS["loop_seq_not_supported"] )
	if c.construct.find ("tile") >= 0:
		warnings.append ( PREDEFINED_WARNINGS["loop_tile_not_supported"] )

	# Check for independent clause
	if c.construct.find ("independent") >= 0:
		omp_clauses.append ("order(concurrent)")

	# Process collapse clause
	depth = getSingleParenthesisContents (c.construct, "collapse")
	if len(depth) > 0:
		# If force: is passed to collapse, ignore it
		# note that this is not explicitly supported in the openACC spec but some
		# apps like VASP uses it
		if depth.startswith ("force:"):
			depth = depth[len("force:"):]
			warnings.append (PREDEFINED_WARNINGS["collapse_force"])
		if int(depth) >= 1:
			omp_clauses.append ("collapse({})".format(depth))

	# Store data back into the construct class
	c.openmp = pre_constructs + [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

	return carryOnStatus, SupplementaryConstructs

# Translate: ACC DECLARE ==> OMP DECLARE TARGET
def translate_oacc_2_omp_acc_declare(txConfig, c):
	omp_construct = []
	omp_clauses = []
	warnings = []

	if txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed or txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
		omp_construct = ["declare target"]
		# Process copyin clause
		variables = getMultiParenthesisContents (c.construct, "copyin")
		if len(variables) > 0:
			omp_clauses.append ("({})".format(variables))
		# Process copy clause
		variables = getMultiParenthesisContents (c.construct, "copy")
		if len(variables) > 0:
			omp_clauses.append ("({})".format(variables))
		# Process create clause
		variables = getMultiParenthesisContents (c.construct, "create")
		if len(variables) > 0:
			omp_clauses.append ("({})".format(variables))
			warnings.append (PREDEFINED_WARNINGS["unimplemented_declare_create"])
		# Process link clause
		variables = getMultiParenthesisContents (c.construct, "link")
		if len(variables) > 0:
			omp_clauses.append ("link({})".format(variables))
		# Process deviceptr clause
		variables = getMultiParenthesisContents (c.construct, "deviceptr")
		if len(variables) > 0:
			omp_clauses.append ("device_type(\"nohost\")")
		# Process device_resident clause
		variables = getMultiParenthesisContents (c.construct, "device_resident")
		if len(variables) > 0:
			omp_construct = []
			warnings.append (PREDEFINED_WARNINGS["unimplemented_declare_deviceresident"])
	else:
		print ("ACC DECLARE construct is only supported in Fortran as of now.\nCheck line {}: '{}'".format(c.bline, c.construct))

	# Store data back into the construct class
	c.openmp = [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC ROUTINE ==> OMP DECLARE TARGET
def translate_oacc_2_omp_acc_routine(txConfig, c):
	omp_construct = ["declare target"]
	omp_clauses = []
	warnings = []

	# is there a list coming after the acc routine, if so, forward it.
	if c.construct.find("(") >= 0:
		r = getSingleParenthesisContents (c.construct, "routine")
		if len(r) > 0:
			omp_clauses.append ("({})".format(r))

	if c.construct.find (" vector") or \
	   c.construct.find (" gang") or \
	   c.construct.find (" worker") or \
	   c.construct.find (" seq"):
		warnings.append (PREDEFINED_WARNINGS["unimplemented_routine_parallelism"])

	# Store data back into the construct class
	c.openmp = [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC PARALLEL ==> OMP TARGET TEAMS
def translate_oacc_2_omp_acc_parallel(txConfig, c, carryOnStatus):
	pre_constructs = []
	omp_construct = ["target teams"]
	omp_clauses = []
	warnings = []

	# do we have a worksharing (loop) construct ?
	if c.construct.find (" loop") >= 0:
		c.hasLoop = True
		carryOnStatus, _ = translate_oacc_2_omp_acc_loop(None, txConfig, c, carryOnStatus, None)

	# Process create, copy, copyin, copyout clauses
	omp_clauses, warn_aux = translate_oacc2_aux_copy_clauses (txConfig, c)
	warnings.extend (warn_aux)

	# Process present clause
	variables = getMultiParenthesisContents (c.construct, "present")
	if len(variables) > 0:
		if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
			omp_clauses.append ("map(alloc:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
			omp_clauses.append ("map(tofrom:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
			omp_clauses.append ("map(present,tofrom:{})".format(variables))

	# Process deviceptr clause
	variables = getMultiParenthesisContents (c.construct, "deviceptr")
	if len(variables) > 0:
		omp_clauses.append ("is_device_ptr({})".format(variables))

	# Process firstprivate clause
	variables = getMultiParenthesisContents (c.construct, "firstprivate")
	if len(variables) > 0:
		omp_clauses.append ("firstprivate({})".format(variables))

	# Process if(x)
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process num_gangs(x)
	if (CONSTANTS.BindingClauses.GANG & txConfig.BindingClauses) != 0:
		n = getSingleParenthesisContents (c.construct, "num_gangs")
		if len(n) > 0:
			omp_clauses.append ("num_teams({})".format(n))

	# Process num_workers(x)
	if (CONSTANTS.BindingClauses.WORKER & txConfig.BindingClauses) != 0:
		n = getSingleParenthesisContents (c.construct, "num_workers")
		if len(n) > 0:
			omp_clauses.append ("thread_limit({})".format(n))

	# Process vector_length(x)
	if (CONSTANTS.BindingClauses.VECTOR & txConfig.BindingClauses) != 0:
		n = getSingleParenthesisContents (c.construct, "vector_length")
		if len(n) > 0:
			warnings.append (PREDEFINED_WARNINGS["unsupported_vector_length_parallel"])

	# Process reduction/private clause, only if this has no work-sharing clause
	# because otherwise the reduction/private is already processed for that clause
	# See OpenACC 3.1 section 2.11
	if not c.hasLoop:
		# Process reduction clause
		reductions = getMultiParenthesisContents (c.construct, "reduction", False)
		if len(reductions) > 0:
			for r in reductions:
				omp_clauses.append ("reduction({})".format(r))
		# Process private clause
		variables = getMultiParenthesisContents (c.construct, "private")
		if len(variables) > 0:
			omp_clauses.append ("private({})".format(variables))

	# Process default clause -- emit a warning on default(none)
	defaultv = getSingleParenthesisContents (c.construct, "default")
	if len(defaultv) > 0:
		# OpenACC firstprivatizes scalars even when default() is given,
		# so we apply defaultmap with the requested modified to the
		# remaining variables (aggregate, pointer and allocatable).
		if defaultv == "present":
			# We have to honor user's request on how to process the
			# present clause
			if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
				omp_clauses.append ("defaultmap(alloc:aggregate)")
				omp_clauses.append ("defaultmap(alloc:pointer)")
				omp_clauses.append ("defaultmap(alloc:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
				omp_clauses.append ("defaultmap(tofrom:aggregate)")
				omp_clauses.append ("defaultmap(tofrom:pointer)")
				omp_clauses.append ("defaultmap(tofrom:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
				omp_clauses.append ("defaultmap(present:aggregate)")
				omp_clauses.append ("defaultmap(present:pointer)")
				omp_clauses.append ("defaultmap(present:allocatable)")
		elif defaultv == "none":
			omp_clauses.append ("defaultmap(none:aggregate)")
			omp_clauses.append ("defaultmap(none:pointer)")
			omp_clauses.append ("defaultmap(none:allocatable)")

	# Process wait clause
	if c.construct.find(" wait(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
		else:
			pre_constructs = ["taskwait"]
			warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / async clause
	if c.construct.find(" async(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			pass
		elif txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.NOWAIT:
			omp_clauses.append ("nowait")
		warnings.append (PREDEFINED_WARNINGS["missing_async"])

	# Store data back into the construct class
	#  keep those already collected in c.openmp/warnings if this
	#  construct has the loop/ws clause
	c.openmp = pre_constructs + [ " ".join(omp_construct + (c.openmp if c.hasLoop else []) + omp_clauses) ]
	c.warnings = warnings + (c.warnings if c.hasLoop else [])

	return carryOnStatus

# Translate: ACC SERIAL ==> OMP TARGET
def translate_oacc_2_omp_acc_serial(txConfig, c, carryOnStatus):
	pre_constructs = []
	omp_construct = ["target"]
	omp_clauses = []
	warnings = []

	# do we have a worksharing (loop) construct ?
	if c.construct.find (" loop") >= 0:
		c.hasLoop = True
		carryOnStatus, _ = translate_oacc_2_omp_acc_loop(None, txConfig, c, carryOnStatus, None)

	# Process create, copy, copyin, copyout clauses
	omp_clauses, warn_aux = translate_oacc2_aux_copy_clauses (txConfig, c)
	warnings.extend (warn_aux)

	# Process present clause
	variables = getMultiParenthesisContents (c.construct, "present")
	if len(variables) > 0:
		if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
			omp_clauses.append ("map(alloc:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
			omp_clauses.append ("map(tofrom:{})".format(variables))
		elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
			omp_clauses.append ("map(present,tofrom:{})".format(variables))

	# Process deviceptr clause
	variables = getMultiParenthesisContents (c.construct, "deviceptr")
	if len(variables) > 0:
		omp_clauses.append ("is_device_ptr({})".format(variables))

	# Process private clause
	variables = getMultiParenthesisContents (c.construct, "private")
	if len(variables) > 0:
		omp_clauses.append ("private({})".format(variables))

	# Process firstprivate clause
	variables = getMultiParenthesisContents (c.construct, "firstprivate")
	if len(variables) > 0:
		omp_clauses.append ("firstprivate({})".format(variables))

	# Process if(x)
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process default clause -- emit a warning on default(none)
	defaultv = getSingleParenthesisContents (c.construct, "default")
	if len(defaultv) > 0:
		# OpenACC firstprivatizes scalars even when default() is given,
		# so we apply defaultmap with the requested modified to the
		# remaining variables (aggregate, pointer and allocatable).
		if defaultv == "present":
			# We have to honor user's request on how to process the
			# present clause
			if txConfig.PresentBehavior == CONSTANTS.PresentBehavior.ALLOC:
				omp_clauses.append ("defaultmap(alloc:aggregate)")
				omp_clauses.append ("defaultmap(alloc:pointer)")
				omp_clauses.append ("defaultmap(alloc:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.TOFROM:
				omp_clauses.append ("defaultmap(tofrom:aggregate)")
				omp_clauses.append ("defaultmap(tofrom:pointer)")
				omp_clauses.append ("defaultmap(tofrom:allocatable)")
			elif txConfig.PresentBehavior == CONSTANTS.PresentBehavior.KEEP:
				omp_clauses.append ("defaultmap(present:aggregate)")
				omp_clauses.append ("defaultmap(present:pointer)")
				omp_clauses.append ("defaultmap(present:allocatable)")
		elif defaultv == "none":
			omp_clauses.append ("defaultmap(none:aggregate)")
			omp_clauses.append ("defaultmap(none:pointer)")
			omp_clauses.append ("defaultmap(none:allocatable)")

	# Process wait clause
	if c.construct.find(" wait(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORED:
			warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
		else:
			pre_constructs = ["taskwait"]
			warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / async clause
	if c.construct.find(" async(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			pass
		elif txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.NOWAIT:
			omp_clauses.append ("nowait")
		warnings.append (PREDEFINED_WARNINGS["missing_async"])

	# Process reduction/private clause, only if this has no work-sharing clause
	# because otherwise the reduction/private is already processed for that clause
	# See OpenACC 3.1 section 2.11
	if not c.hasLoop:
		# Process reduction clause
		reductions = getMultiParenthesisContents (c.construct, "reduction", False)
		if len(reductions) > 0:
			for r in reductions:
				omp_clauses.append ("reduction({})".format(r))
		# Process private clause
		variables = getMultiParenthesisContents (c.construct, "private")
		if len(variables) > 0:
			omp_clauses.append ("private({})".format(variables))

	# Store data back into the construct class
	#  keep those already collected in c.openmp/warnings if this
	#  construct has the loop/ws clause
	c.openmp = pre_constructs + [ " ".join(omp_construct + (c.openmp if c.hasLoop else []) + omp_clauses) ]
	c.warnings = warnings + (c.warnings if c.hasLoop else [])

	return carryOnStatus

# Translate: ACC UPDATE ==> OMP TARGET UPDATE
def translate_oacc_2_omp_acc_update(txConfig,c):
	pre_constructs = []
	omp_construct = ["target update"]
	omp_clauses = []
	warnings = []

	# Process self clause
	variables = getMultiParenthesisContents (c.construct, "self")
	if len(variables) > 0:
		omp_clauses.append ("from({})".format(variables))

	# Process host clause
	variables = getMultiParenthesisContents (c.construct, "host")
	if len(variables) > 0:
		omp_clauses.append ("from({})".format(variables))

	# Process device clause
	variables = getMultiParenthesisContents (c.construct, "device")
	if len(variables) > 0:
		omp_clauses.append ("to({})".format(variables))

	# Process if
	condition = getSingleParenthesisContents (c.construct, "if")
	if len(condition) > 0:
		omp_clauses.append ("if({})".format(condition))

	# Process wait clause
	if c.construct.find(" wait(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
		else:
			pre_constructs = ["taskwait"]
			warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / async clause
	if c.construct.find(" async(") >= 0:
		if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
			pass
		elif txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.NOWAIT:
			omp_clauses.append ("nowait")
		warnings.append (PREDEFINED_WARNINGS["missing_async"])

	# Store data back into the construct class
	c.openmp = pre_constructs + [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

# Translate: ACC WAIT ==> OMP TASKWAIT [depending on config]
def translate_oacc_2_omp_acc_wait(txConfig, c):
	warnings = []

	if txConfig.AsyncBehavior == CONSTANTS.AsyncBehavior.IGNORE:
		omp_construct = []
		warnings.append (PREDEFINED_WARNINGS["ignored_wait"])
	else:
		omp_construct = ["taskwait"]
		warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics"])

	# Process unhandled / if directives
	if c.construct.find(" if(") >= 0:
		warnings.append (PREDEFINED_WARNINGS["mismatch_depend_wait_semantics_if"])

	# Store data back into the construct class
	c.openmp = omp_construct
	c.warnings = warnings

#
# END STATEMENTS
#

# Translate: ACC END ATOMIC ==> OMP END ATOMIC
def translate_oacc_2_omp_acc_end_atomic(c):
	# Store data back into the construct class
	c.openmp = ["end atomic"]
	c.warnings = []

# Translate: ACC END DATA ==> OMP END DATA
def translate_oacc_2_omp_acc_end_data(c):
	# Store data back into the construct class
	c.openmp = ["end target data"]
	c.warnings = []

# Translate: ACC END HOST DATA ==> OMP END TARGET DATA
def translate_oacc_2_omp_acc_end_host_data(txConfig, c, carryOnStatus):
	# We need to update the data in the device

	warnings = []
	omp_construct = []
	omp_clauses = []

	if txConfig.HostDataBehavior == CONSTANTS.HostDataBehavior.TARGET_DATA:
		omp_construct = ["end target data"]
	elif txConfig.HostDataBehavior == CONSTANTS.HostDataBehavior.TARGET_UPDATE:
		omp_construct = ["target update"]
		if "host_data" not in carryOnStatus:
			print ("Error! Cannot find the matching opening construct for '{}'".format(construct))
			sys.exit (-1)
		# Grab the variables used in the opening section
		variables = carryOnStatus["host_data"]
		if len(variables) > 0:
			omp_clauses.append ("to({})".format(variables))
		else:
			print ("Error! The matching opening construct for '{}' does not include variables.".format(construct))
			sys.exit (-1)
		# Remove the key entry in the carryOnStatus dictionary
		del carryOnStatus["host_data"]

	# Store data back into the construct class
	c.openmp = [ " ".join(omp_construct + omp_clauses) ]
	c.warnings = warnings

	return carryOnStatus

# Translate: ACC END ERNELS [LOOP]
def translate_oacc_2_omp_acc_end_kernels(c, carryOnStatus):
	# Store data back into the construct class
	c.warnings = []

	# do we have a worksharing (loop) construct ?
	if c.construct.find (" loop") >= 0:
		c.openmp = ["end target teams loop"]
	else:
		c.openmp = ["end target"]

	# Remove the kernels marker from the carryOnStatus data.
	if "within_kernels" in carryOnStatus:
		del carryOnStatus["within_kernels"]

	return carryOnStatus

# Translate: ACC END PARALLEL [LOOP]
def translate_oacc_2_omp_acc_end_parallel(c):
	# Store data back into the construct class
	c.warnings = []

	# do we have a worksharing (loop) construct ?
	if c.construct.find (" loop") >= 0:
		c.openmp = ["end target teams loop"]
	else:
		c.openmp = ["end target teams"]

# Translate: ACC END SERIAL [LOOP]
def translate_oacc_2_omp_acc_end_serial (c):
	# Store data back into the construct class
	c.warnings = []

	# do we have a worksharing (loop) construct ?
	if c.construct.find (" loop") >= 0:
		c.openmp = ["end target loop"]
	else:
		c.openmp = ["end target"]

# Main translation point for ACC constructs
def translate_oacc_2_omp (lines, txConfig, c, carryOnStatus, SupplementaryConstructs):

	# begin constructs
	if c.construct.startswith ("atomic"):
		translate_oacc_2_omp_acc_atomic (c)
	elif c.construct.startswith ("cache"):
		translate_oacc_2_omp_acc_cache (c)
	elif c.construct.startswith ("data"):
		translate_oacc_2_omp_acc_data (txConfig, c)
	elif c.construct.startswith ("enter data"):
		translate_oacc_2_omp_acc_enter_data (txConfig, c)
	elif c.construct.startswith ("exit data"):
		translate_oacc_2_omp_acc_exit_data (txConfig, c)
	elif c.construct.startswith ("host_data"):
		translate_oacc_2_omp_acc_host_data (txConfig, c, carryOnStatus)
	elif c.construct.startswith ("kernels"):
		carryOnStatus = translate_oacc_2_omp_acc_kernels (lines, txConfig, c, carryOnStatus)
	elif c.construct.startswith ("loop"):
		carryOnStatus, SupplementaryConstructs = translate_oacc_2_omp_acc_loop (lines,
		  txConfig, c, carryOnStatus, SupplementaryConstructs)
	elif c.construct.startswith ("parallel"):
		carryOnStatus = translate_oacc_2_omp_acc_parallel (txConfig, c, carryOnStatus)
	elif c.construct.startswith ("routine"):
		translate_oacc_2_omp_acc_routine (txConfig, c)
	elif c.construct.startswith ("declare"):
		translate_oacc_2_omp_acc_declare (txConfig, c)
	elif c.construct.startswith ("serial"):
		carryOnStatus = translate_oacc_2_omp_acc_serial (txConfig, c, carryOnStatus)
	elif c.construct.startswith ("update"):
		translate_oacc_2_omp_acc_update (txConfig, c)
	elif c.construct.startswith ("wait"):
		translate_oacc_2_omp_acc_wait (txConfig, c)
	# end constructs
	elif c.construct.startswith ("end atomic"):
		translate_oacc_2_omp_acc_end_atomic (c)
	elif c.construct.startswith ("end data"):
		translate_oacc_2_omp_acc_end_data (c)
	elif c.construct.startswith ("end host_data"):
		translate_oacc_2_omp_acc_end_host_data (txConfig, c, carryOnStatus)
	elif c.construct.startswith ("end kernels"):
		carryOnStatus = translate_oacc_2_omp_acc_end_kernels (c, carryOnStatus)
	elif c.construct.startswith ("end parallel"):
		translate_oacc_2_omp_acc_end_parallel (c)
	elif c.construct.startswith ("end serial"):
		translate_oacc_2_omp_acc_end_serial (c)

	return carryOnStatus, SupplementaryConstructs

# translate (txconfig, lines, constructs)
#  translates the constructs found in the code lines while observing the requested
#  configuration by the user
def translate (txConfig, lines, construct):
	# First process the constructs

	# We will use the carryOnStatus dictionary to carry on some parameters/clauses from
	# one construct to another.
	# The dictionary is indexed by the originator construct, and will store whatever
	# information is needed later
	carryOnStatus = dict ()
	SupplementaryConstructs = dict()
	 
	for line, construct in construct.items():
		carryOnStatus, SupplementaryConstructs = translate_oacc_2_omp (lines, txConfig,
		  construct, carryOnStatus, SupplementaryConstructs)

	APIwarnings = []
	# Then, check for OpenACC calls in the code - so that we emit
	# a warning for each of those.
	for i in range(0,len(lines)):
		line = lines[i]

		# Check for headers/modules
		if txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed or txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
			line = line.lower()
			# Check for use 
			if line.find ("use") >= 0:
				if line[line.find("use"):].find ("openacc") >= 0:
					w = "Line {} includes the Fortran OpenACC module. Change it into 'USE omplib'.".format(i+1)
					APIwarnings.append (w)
					pass
		else:
			# Check for #include <openacc.h> or "openacc.h"
			if line.find ("#include") >= 0:
				if line[line.find("#include"):].find ("openacc.h") >= 0:
					w = "Line {} includes the C/C++ OpenACC header. Change it into '#include <omp.h>'.".format(i+1)
					APIwarnings.append (w)
					pass

		# Check for calls
		for call, suggestion in ACC_API_calls.items():
			# convert to lower-case if input is in Fortran
			if txConfig.Lang == CONSTANTS.FileLanguage.FortranFixed or txConfig.Lang == CONSTANTS.FileLanguage.FortranFree:
				line = line.lower()
			if line.find(call) >= 0:
				w = "Line {} contains an invocation to '{}'.".format(i+1, call)
				if len(suggestion) > 0:
					w += " " + suggestion
				APIwarnings.append (w)

	return APIwarnings, SupplementaryConstructs

# vim:set noexpandtab tabstop=4:
