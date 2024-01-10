#
# Enumerations module for "Intel(r) Application Migration Tool for OpenACC* to OpenMP*"
#

from enum import Enum, IntEnum

class PresentBehavior(Enum):
	TOFROM = 0                                   # Translate present into map(tofrom:)
	ALLOC = 1                                    # Translate present into map(alloc:)
	KEEP = 2                                     # Keep usage of present (req. OpenMP 5.1)

class AsyncBehavior(Enum):
	IGNORE = 0                                   # Do not translate async
	NOWAIT = 1                                   # Translate async into a nowait

class HostDataBehavior(Enum):
	TARGET_DATA = 0                              # Translate host_data into target data
	TARGET_UPDATE = 1                            # Translate host_data into target update

class FileLanguage(Enum):
	C = 0                                        # C
	CPP = 1                                      # C++
	FortranFixed = 2                             # Fortran (fixed)
	FortranFree = 3                              # Fortran (free)

class FileSuffixToFileLanguage:
	_map = {
	         ".f90": FileLanguage.FortranFree,
	         ".f95": FileLanguage.FortranFree,
	         ".f03": FileLanguage.FortranFree,
	         ".f08": FileLanguage.FortranFree,
	         ".f":   FileLanguage.FortranFixed,
	         ".f77": FileLanguage.FortranFixed,
	         ".cxx": FileLanguage.CPP,
	         ".c++": FileLanguage.CPP,
	         ".cpp": FileLanguage.CPP,
	         ".cc":  FileLanguage.CPP,
	         ".hxx": FileLanguage.CPP,
	         ".h++": FileLanguage.CPP,
	         ".hpp": FileLanguage.CPP,
	         ".c":   FileLanguage.C,
	         ".h":   FileLanguage.C
	  }

class BindingClauses(IntEnum):
	NONE = 0                                     # No binding clause translated
	GANG = 1 << 0                                # gang / num_gangs
	WORKER = 1 << 1                              # worker / num_workers
	VECTOR =  1 << 2                             # vector / vector_length
	ALL = GANG | WORKER | VECTOR                 # All above

# vim:set noexpandtab tabstop=4:
