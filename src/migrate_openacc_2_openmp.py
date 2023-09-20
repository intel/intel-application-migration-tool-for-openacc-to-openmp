#
# Main module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP*"
#

import migrate_openacc_2_openmp_constants as CONSTANTS
import migrate_openacc_2_openmp_convert as OACC2OMP
import migrate_openacc_2_openmp_codegen as CODEGEN
import migrate_openacc_2_openmp_parser as PARSER
import sys
import os
import shutil
import re
from enum import Enum

class FortranVariant(Enum):
	AUTO = 0                                   # Infer from file extension
	FIXED = 1                                  # Fixed source
	FREE = 2                                   # Free source

# generateReport (lang, construct, infilename, APIwarnings)
#  generates a report of the requested translation
#  lang = "C" or "Fortran" -> for #pragma omp or !$OMP emission
#  construct = contains OpenACC translated statements. these statements contain
#      information about specific warnings issued during the translation
#  infilename = name of the input file
#  APIwarnings = a list of API-calls related warnings
def generateReport(lang, construct, infilename, APIwarnings):
	try:
		with open(infilename+str(".report"), 'w') as report:
			# Process constructs, by line
			for line, construct in construct.items():
				# Emit the original statement
				if construct.eline == construct.bline:
					report.write (f"* Line {construct.bline} contains the following statement\n")
				else:
					report.write (f"* Lines {construct.bline}-{construct.eline} contains the following statement\n")
				for l in construct.original:
					report.write (f"{l}\n")
				# Follows the emission of the translated statement, if it was translated
				if construct.openmp is None:
					report.write ("that has NOT been as been translated.\n")
				else:
					report.write("that has been as been translated into:\n")
					if construct.openmp != []:
						if lang == CONSTANTS.FileLanguage.FortranFree or lang == CONSTANTS.FileLanguage.FortranFixed:
							report.write ("!$omp")
						elif lang == CONSTANTS.FileLanguage.C or lang == CONSTANTS.FileLanguage.CPP:
							report.write ("#pragma omp")
						for p in construct.openmp:
							report.write (f" {p}")
						report.write ("\n")
					else:
						report.write ("Nothing.\n")
				# Emit specific warnings related to this construct translation into
				# OpenMP
				if construct.warnings:
					report.write ("* WARNING(s)! Please review the translation.\n")
					cnt = 1
					for p in construct.warnings:
						report.write (f"  {cnt}. {p}\n")
						cnt = cnt + 1
				report.write ("\n\n")

			# Finally, dump warnings related to OpenACC API usage. These are not
			# translated yet.
			if len(APIwarnings) > 0:
				report.write ("Note the following OpenACC API calls. These have NOT been translated.\n")
				for w in APIwarnings:
					report.write (f"* {w}\n")
				report.write ("\n\n")

			report.close()
	except IOError:
		print (f"Error! File {infile} is not accessible for writing.")

def showHelp():
	print ("Intel(r) Application Migration Tool for OpenACC* to OpenMP*")
	print ("---")
	print ("Expected parameters: <Options> file")
	print ("")
	print ("Where options:")
	print (" -h // -help                  : Shows this help screen")
	print (" -async=<ignore,nowait>       : Specifies how to treat ACC ASYNC clauses.                                 (nowait)")
	print ("                                - ignore refers to not translate the ASYNC clauses.")
	print ("                                - nowait translates ACC ASYNC clauses into nowait.")
	print (" [-no]-declare-mapper         : Declares mappers for user-defined data-types (Fortran only)               (enabled)")
	print (" -fixed|-free                 : Sets fixed-format or free-format for Fortran translation                  (auto)")
	print (" -specify-language=L          : Forces the parsing of the file for language                               (auto)")
	print ("                                (auto, C, C++, Fortran/Free or Fortran/Fixed) ")
	print (" [-no]-force-backup           : If enabled, enforce writing a backup of the original file.                (disabled)")
	print (" [-no]-generate-report        : Enables/Disables report generation about the translation.                 (enabled)")
	print (" [-no]-generate-multidimensional-alternate-code :                                                         (enabled)")
	print ("                                Provides implementation suggestions for ACC ENTER/EXIT DATA constructs to be employed ")
	print ("                                if the multi-dimensional data is non-contiguous")
	print (" -host_data=<target_data,target_update> : Specifies how to convert HOST_DATA clauses                      (target_update)")
	print ("                                - target_data employs !$omp target data")
	print ("                                - target_data employs !$omp target update, using host memory.")
	print (" -keep-binding-clauses=X      : Specifies which hardware binding clauses are kept in OpenMP               (none)")
	print ("                                Where X can be: all, none, and a combination of gang, worker and vector")
	print (" [-no]-overwrite-input        : Enables/Disables overwriting the original file with the translation.      (disabled)")
	print (" -present=<alloc,tofrom,keep> : Specifies how to treat ACC PRESENT constructs.                            (keep)")
	print ("                                - alloc refers to mimic PRESENT clauses with MAP(ALLOC:)")
	print ("                                - tofrom refers to mimic PRESENT clauses with MAP(TOFROM:)")
	print ("                                - keep refers to use OMP PRESENT clauses (requires OpenMP 5.1+ compiler).")
	print (" [-no]-suppress-openacc       : Enables/Disables suppression of OpenACC translated statements in result.  (disabled)")
	print ("")
	print ("* PREPROCESSING GUARDS")
	print (" [-no]-openacc-conditional-define           : If enabled, wraps OpenACC source code with #ifdef OPENACC2OPENMP_OPENACC.              (disabled)")
	print (" -openacc-conditional-define=DEF            : If enabled, wraps OpenACC source code with #ifdef DEF.")
	print (" [-no]-translated-openmp-conditional-define : If enabled, wraps OpenMP translated code with #ifdef OPENACC2OPENMP_TRANSLATED_OPENMP. (disabled)")
	print (" -translated-openmp-conditional-define=DEF  : If enabled, wraps OpenMP translated code with #ifdef DEF.")
	print (" [-no]-original-openmp-conditional-define   : If enabled, wraps OpenMP source code with #ifdef OPENACC2OPENMP_ORIGINAL_OPENMP.       (disabled)")
	print (" -original-openmp-conditional-define=DEF    : If enabled, wraps OpenMP source code with #ifdef DEF.")
	print ("")
	print ("* EXPERIMENTAL FEATURES")
	print (" [-no]-experimental-kernels-support :                                                                     (enabled)")
	print ("                                When enabled, the tool tries to extract parallelism from loop constructs found")
	print ("                                within kernels constructs (Fortran only).")
	print ("                                NOTE: Explore the code for target/end target empty bubbles.")
	print (" [-no]-experimental-remove-kernels-bubbles:                                                               (enabled)")
	print ("                                When enabled, the tool attempts to remove the target/end target empty bubbles")
	print ("                                introduced by -[no-]experimental-kernels-support.")

#
#
# PROCESS FILE
#
#

def processFile (inputfile, txConfig, GenerateReport, ForceBackup, OverwriteInput):

	inputfile_l = inputfile.lower()
	print (f"Processing file {inputfile}")

	# Check for file existance
	if os.path.exists(inputfile):
		if os.path.isfile(inputfile):
			if not os.access (inputfile, os.R_OK):
				print ("Error! File {inputfile} is not accessible for reading.")
				sys.exit(-1)
		else:
			print ("Error! Path {inputfile} does not refer to a file.")
			sys.exit(-1)
	else:
		print ("Error! Path {inputfile} does not exist.")
		sys.exit(-1)

	# If a backup file (suffix .original) is found, then die unless
	# the user requested to force a backup
	if os.path.exists(inputfile+str(".original")) and not ForceBackup:
		print ("Error! Backup file {} already exists not exist. Pass -force-backup to bypass this test.".format(inputfile+str(".original")))
		sys.exit(-1)

	# Makes a backup of the original file
	shutil.copyfile (inputfile, inputfile+str(".original"))

	# Parse input file
	lines, ACCconstructs, OMPconstructs, UDTdefinitions, ListFortranFunctionsSubroutines = PARSER.parseFile (inputfile, txConfig)

	# Run the translation
	APIwarnings, SupplementaryConstructs = OACC2OMP.translate (txConfig, lines,
	  ACCconstructs)

	if txConfig.experimentalRemoveKernelsBubblesSupport:
		ACCconstructs, SupplementaryConstructs = CODEGEN.removeTargetEndTargetBubbles (txConfig,
		  lines, ACCconstructs, SupplementaryConstructs)

	# Generate the translated file, and if requested, the report
	TXfile = inputfile+str(".translated")
	CODEGEN.generateTranslatedFile (txConfig, lines, ACCconstructs, OMPconstructs,
	  SupplementaryConstructs, UDTdefinitions, ListFortranFunctionsSubroutines, TXfile)

	if GenerateReport:
		generateReport (txConfig.Lang, ACCconstructs, inputfile, APIwarnings)

	return TXfile

#
#
# MAIN ENTRY POINT
#
#

def entry(argv):

	if len(argv) == 0:
		showHelp ()
		sys.exit (0)

	for i in range(0, len(argv)):
		param = argv[i]
		if param == "-h" or param == "-help":
			showHelp ()
			sys.exit (0)

	GenerateReport = True
	ForceBackup = False
	OverwriteInput = False
	GenerateMultiDimensionalAlternateCode = True
	OpenACCConditionalDefine = None
	TranslatedOMPConditionalDefine = None
	OriginalOMPConditionalDefine = "OPENACC2OPENMP_ORIGINAL_OPENMP"
	SuppressTranslatedOpenACC = False
	PresentBehavior = CONSTANTS.PresentBehavior.KEEP
	AsyncBehavior = CONSTANTS.AsyncBehavior.NOWAIT
	HostDataBehavior = CONSTANTS.HostDataBehavior.TARGET_UPDATE
	FortranV = FortranVariant.AUTO
	ForceLanguage = None
	KeepBindingClauses = CONSTANTS.BindingClauses.NONE
	ExperimentalKernelsSupport = True
	ExperimentalRemoveKernelsBubblesSupport = True
	DeclareMapper = True

	LastGoodParam = None

	for i in range(0, len(argv)):
		param = argv[i]
		if param == "-generate-report":
			GenerateReport = True
		elif param == "-no-generate-report":
			GenerateReport = False
		elif param == "-overwrite-input":
			OverwriteInput = True
		elif param == "-no-overwrite-input":
			OverwriteInput = False
		elif param == "-force-backup":
			ForceBackup = True
		elif param == "-no-force-backup":
			ForceBackup = False
		elif param == "-declare-mapper":
			DeclareMapper = True
		elif param == "-no-declare-mapper":
			DeclareMapper = False
		elif param == "-generate-multidimensional-alternate-code":
			GenerateMultiDimensionalAlternateCode = True
		elif param == "-no-generate-multidimensional-alternate-code":
			GenerateMultiDimensionalAlternateCode = False
		elif param == "-openacc-conditional-define":
			OpenACCConditionalDefine = "OPENACC2OPENMP_OPENACC"
		elif param == "-no-openacc-conditional-define":
			OpenACCConditionalDefine = None
		elif param.startswith ("-openacc-conditional-define="):
			OpenACCConditionalDefine = param[len("-openacc-conditional-define="):]
		elif param == "-translated-openmp-conditional-define":
			TranslatedOMPConditionalDefine = "OPENACC2OPENMP_TRANSLATED_OPENMP"
		elif param == "-no-translated-openmp-conditional-define":
			TranslatedOMPConditionalDefine = None
		elif param.startswith ("-translated-openmp-conditional-define="):
			TranslatedOMPConditionalDefine = param[len("-translated-openmp-conditional-define="):]
		elif param == "-original-openmp-conditional-define":
			OriginalOMPConditionalDefine = "OPENACC2OPENMP_ORIGINAL_OPENMP"
		elif param == "-no-original-openmp-conditional-define":
			OriginalOMPConditionalDefine = None
		elif param.startswith ("-original-openmp-conditional-define="):
			OriginalOMPConditionalDefine = param[len("-original-openmp-conditional-define="):]
		elif param == "-suppress-openacc":
			SuppressTranslatedOpenACC = True
		elif param == "-no-suppress-openacc":
			SuppressTranslatedOpenACC = False
		elif param == "-present=alloc":
			PresentBehavior = CONSTANTS.PresentBehavior.ALLOC
		elif param == "-present=tofrom":
			PresentBehavior = CONSTANTS.PresentBehavior.TOFROM
		elif param == "-present=keep":
			PresentBehavior = CONSTANTS.PresentBehavior.KEEP
		elif param == "-async=ignore":
			AsyncBehavior = CONSTANTS.AsyncBehavior.IGNORE
		elif param == "-async=nowait":
			AsyncBehavior = CONSTANTS.AsyncBehavior.NOWAIT
		elif param == "-host_data=target_data":
			HostDataBehavior = CONSTANTS.HostDataBehavior.TARGET_DATA
		elif param == "-host_data=target_update":
			HostDataBehavior = CONSTANTS.HostDataBehavior.TARGET_UPDATE
		elif param == "-fixed":
			FortranV = FortranVariant.FIXED
		elif param == "-free":
			FortranV = FortranVariant.FREE
		elif param.startswith ("-specify-language="):
			ForceLanguage = param[len("-specify-language="):]
		elif param.startswith ("-keep-binding-clauses="):
			clauses = param[len("-keep-binding-clauses="):]
			if clauses == "all":
				KeepBindingClauses = CONSTANTS.BindingClauses.ALL
			elif clauses == "none":
				KeepBindingClauses = CONSTANTS.BindingClauses.NONE
			else:
				KeepBindingClauses = CONSTANTS.BindingClauses.NONE
				lclauses = clauses.split(',')
				if "vector" in lclauses:
					lclauses.remove ("vector")
					KeepBindingClauses |= CONSTANTS.BindingClauses.VECTOR
				if "gang" in lclauses:
					lclauses.remove ("gang")
					KeepBindingClauses |= CONSTANTS.BindingClauses.GANG
				if "worker" in lclauses:
					lclauses.remove ("worker")
					KeepBindingClauses |= CONSTANTS.BindingClauses.WORKER
				for unused in lclauses:
					print (f"Unused parameter ({unused}) for -keep-binding-clauses")
		elif param == "-experimental-kernels-support":
			ExperimentalKernelsSupport = True
		elif param == "-no-experimental-kernels-support":
			ExperimentalKernelsSupport = False
		elif param == "-experimental-remove-kernels-bubbles":
			ExperimentalRemoveKernelsBubblesSupport = True
		elif param == "-no-experimental-remove-kernels-bubbles":
			ExperimentalRemoveKernelsBubblesSupport = False
		else:
			LastGoodParam = i
			break

	# If LastGoodParam is not set, then we haven't received input files
	if LastGoodParam is None:
		print ("Error! No input files given. Aborting.")
		sys.exit(-1)

	# All params after the last good param are considered file.
	# Process them one by one.
	for i in range(LastGoodParam, len(argv)):
		# Store current directory
		currentdir = os.getcwd()

		# Change to new directory if necessary, and work/generate
		# files there
		inputdir = os.path.dirname(argv[i])
		if inputdir is not None and len(inputdir) > 0:
			os.chdir (inputdir)
		inputfile = os.path.basename(argv[i])

		if not os.path.isfile(inputfile):
			print (f"Error! Cannot find file {inputfile}.")
			sys.exit (-1)

		inputfile_l = inputfile.lower()

		# Determines the language for this file
		lang = None

		# If the user did not specify a language or chose "auto" we try to identify
		# the language out of the file extension/suffix.
		if ForceLanguage is None or ForceLanguage == "auto":
			# Can / Should we infer the Fortran variant?
			if FortranV == FortranVariant.AUTO:
				if len(inputfile) > len(".f90") and \
				    (inputfile_l[-4:] == ".f90" or inputfile_l[-4:] == ".f95" or \
				     inputfile_l[-4:] == ".f03" or inputfile_l[-4:] == ".f08"):
					lang = CONSTANTS.FileLanguage.FortranFree
				if len(inputfile) > len(".f77") and inputfile_l[-4:] == ".f77":
					lang = CONSTANTS.FileLanguage.FortranFixed
				if len(inputfile) > len(".f") and inputfile_l[-2:] == ".f":
					lang = CONSTANTS.FileLanguage.FortranFixed
			else:
				if len(inputfile) > len(".f90") and \
				    (inputfile_l[-4:] == ".f90" or inputfile_l[-4:] == ".f95" or \
				     inputfile_l[-4:] == ".f03" or inputfile_l[-4:] == ".f08" or \
				     inputfile_l[-4:] == ".f77"):
						lang = CONSTANTS.FileLanguage.FortranFree if FortranV == FortranVariant.FREE else CONSTANTS.FileLanguage.FortranFixed
				if len(inputfile) > len(".f") and inputfile_l[-2:] == ".f":
						lang = CONSTANTS.FileLanguage.FortranFree if FortranV == FortranVariant.FREE else CONSTANTS.FileLanguage.FortranFixed

			if len(inputfile) > len(".cxx"):
				if inputfile_l[-4:] == ".cxx" or inputfile_l[-4:] == ".cpp" or inputfile_l[-4:] == ".c++" or \
				   inputfile_l[-4:] == ".hxx" or inputfile_l[-4:] == ".hpp" or inputfile_l[-4:] == ".h++":
					lang = CONSTANTS.FileLanguage.CPP
			if len(inputfile) > len(".cc"):
				if inputfile_l[-3:] == ".cc":
					lang = CONSTANTS.FileLanguage.CPP
			if len(inputfile) > len(".c"):
				if inputfile_l[-2:] == ".c" or inputfile_l[-2:] == ".h":
					lang = CONSTANTS.FileLanguage.C
		else:
			# The user suggested the language
			if ForceLanguage == "C":
				lang = CONSTANTS.FileLanguage.C
			elif ForceLanguage == "C++":
				lang = CONSTANTS.FileLanguage.CPP
			elif ForceLanguage == "Fortran/Fixed":
				lang = CONSTANTS.FileLanguage.FortranFixed
			elif ForceLanguage == "Fortran/Free":
				lang = CONSTANTS.FileLanguage.FortranFree
			else:
				print (f"Error! Incorrect language proposed {ForceLanguage}. Valid alternatives are: C, C++, Fortran/Fixed and Fortran/Free.")
				sys.exit (-1)

		# Did we get the language for the file?
		if lang == None:
			print (f"Error! Unknown language file for file {inputfile}.")
			sys.exit (-1)

		# Create a configuration for this translation based on the give parameters
		txConfig = OACC2OMP.txConfiguration (lang, PresentBehavior, AsyncBehavior, HostDataBehavior,
		  KeepBindingClauses, GenerateMultiDimensionalAlternateCode, OpenACCConditionalDefine,
		  TranslatedOMPConditionalDefine, OriginalOMPConditionalDefine, SuppressTranslatedOpenACC,
		  DeclareMapper,
		  ExperimentalKernelsSupport, ExperimentalRemoveKernelsBubblesSupport)
		TXfile = processFile (inputfile, txConfig, GenerateReport, ForceBackup, OverwriteInput)

		# Append execution details for reproducibility porpuses$a
		try:
			with open (TXfile, 'a') as f:
				f.write ("\n")
				if lang == CONSTANTS.FileLanguage.C or lang == CONSTANTS.FileLanguage.CPP:
					f.write ("// Code was translated using:")
				elif lang == CONSTANTS.FileLanguage.FortranFree or lang == CONSTANTS.FileLanguage.FortranFixed:
					f.write ("! Code was translated using:")
				f.write (" {}".format (os.path.abspath(sys.argv[0])))
				for j in range (1, LastGoodParam+1):
					f.write (" ")
					f.write (sys.argv[j])
				f.write (" ")
				f.write (argv[i])
				f.write ("\n")
				f.close()
		except IOError:
			print (f"Error! File {TXfile} is not accessible for appending.")

		# Overwrite input if requested
		if OverwriteInput:
			shutil.copyfile (TXfile, inputfile)

		# Return to original directory
		os.chdir (currentdir)

# vim:set noexpandtab tabstop=4:
