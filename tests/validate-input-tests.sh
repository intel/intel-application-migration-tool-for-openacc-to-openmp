#!/bin/bash

RED="\e[91m"
GREEN="\e[92m"
NEUTRAL="\033[0m"

THISPWD=$PWD

F77="nvfortran -acc -silent -c"
F90=${F77}
CC="nvc -acc -silent -c"

which nvfortran &> /dev/null
if [[ $? -ne 0 ]]; then
	echo
	echo -e ${RED}Error!${NEUTRAL} Could not locate nvfortran compiler
	exit 1
fi

which nvcc &> /dev/null
if [[ $? -ne 0 ]]; then
	echo
	echo -e ${RED}Error!${NEUTRAL} Could not locate nvcc compiler
	exit 1
fi

if [[ $# -eq 0 ]]; then
	INPUTFILES="Fortran/Fixed*/*.f Fortran/Free*/*.f90 C*/*.c C*/*.h"
else
	INPUTFILES=$@
fi

echo Compiling ...
for f in ${INPUTFILES}
do
	echo "   "${f}
	if [[ "${f: -2}" == ".f" ]]; then
		$F77 -c ${f}
		COMPILE_STATUS=$?
		rm -f *.o *.mod
	elif [[ "${f: -4}" == ".f90" ]]; then
		$F90 -c ${f}
		COMPILE_STATUS=$?
		rm -f *.o *.mod
	elif [[ "${f: -2}" == ".c" ]]; then
		${CC} -c ${f}
		COMPILE_STATUS=$?
		rm -f *.o
	else
		echo
		echo -e ${RED}failed${NEUTRAL} for file ${f}
		exit 1
	fi
	if [[ ${COMPILE_STATUS} -ne 0 ]] ; then
		echo
		echo -e ${RED}failed${NEUTRAL} for file ${f}
		exit ${COMPILE_STATUS}
	fi

done
echo -e Compilation ${GREEN}suceeded${NEUTRAL}!
