#!/bin/bash

TESTS="Fortran/Fixed*/*.f Fortran/Free*/*.f90 C*/*.c C*/*.h"

RED="\e[91m"
GREEN="\e[92m"
NEUTRAL="\033[0m"

THISPWD=$PWD

DELTA=`which delta`
if [[ "${DELTA}" == "" ]]; then
	echo Cannot find delta on path. Consider installing it. Using regular diff to show file differences.
fi
DIFF=`which diff`
if [[ "${DIFF}" == "" ]]; then
	echo Cannot find diff on path! Aborting!
fi

echo Running the translations --
cd Fortran/Fixed
${THISPWD}/../src/intel-application-migration-tool-for-openacc-to-openmp -force-backup -keep-binding-clauses=all -fixed *.f
if [[ ${?} -ne 0 ]]; then
	echo -e Translation ${RED}failed!${NEUTRAL}
	exit ${?}
fi
cd ../Fixed+async
${THISPWD}/../src/intel-application-migration-tool-for-openacc-to-openmp -force-backup -keep-binding-clauses=all -fixed -async=nowait *.f
if [[ ${?} -ne 0 ]]; then
	echo -e Translation ${RED}failed!${NEUTRAL}
	exit ${?}
fi
cd ../Free
${THISPWD}/../src/intel-application-migration-tool-for-openacc-to-openmp -force-backup -keep-binding-clauses=all -free *.f90
if [[ ${?} -ne 0 ]]; then
	echo -e Translation ${RED}failed!${NEUTRAL}
	exit ${?}
fi
cd ../Free+async
${THISPWD}/../src/intel-application-migration-tool-for-openacc-to-openmp -force-backup -keep-binding-clauses=all -free -async=nowait *.f90
if [[ ${?} -ne 0 ]]; then
	echo -e Translation ${RED}failed!${NEUTRAL}
	exit ${?}
fi
cd ../../C
${THISPWD}/../src/intel-application-migration-tool-for-openacc-to-openmp -force-backup -keep-binding-clauses=all *.c *.h
if [[ ${?} -ne 0 ]]; then
	echo -e Translation ${RED}failed!${NEUTRAL}
	exit ${?}
fi
cd ../C+async
${THISPWD}/../src/intel-application-migration-tool-for-openacc-to-openmp -force-backup -keep-binding-clauses=all -async=nowait *.c
if [[ ${?} -ne 0 ]]; then
	echo -e Translation ${RED}failed!${NEUTRAL}
	exit ${?}
fi
cd ..
echo

nfiles=0
for f in ${TESTS}
do
	nfiles=$((nfiles+1))
done

echo -n Comparing \(${nfiles}\)" "
curfile=0
for f in ${TESTS}
do
	curfile=$((curfile+1))
	if [[ (${curfile} == 1) || ($((curfile % 10)) == 0) ]]; then
		echo -n ${curfile}
	else
		echo -n .
	fi
	# Ignore the command line appended in the last line of the translation
	if [[ -f ${f}.reference ]] ; then
		head --lines=-1 ${f}.reference > ${f}.reference.nocmdline
	else
		echo
		echo -e ${RED}Error!${NEUTRAL} Missing ${f}.reference file
		exit
	fi
	if [[ -f ${f}.translated ]] ; then
		head --lines=-1 ${f}.translated > ${f}.translated.nocmdline
	else
		echo
		echo -e ${RED}Error!${NEUTRAL} Missing ${f}.translated file
		exit
	fi
	# Calculate the difference
	${DIFF} ${f}.reference.nocmdline ${f}.translated.nocmdline >& /dev/null
	DIFF_STATUS=$?
	# Remove the intermediate files
	rm -f ${f}.reference.nocmdline ${f}.translated.nocmdline
	# If there are differences, dump them
	if [[ ${DIFF_STATUS} -ne 0 ]]; then
		echo -e ${RED}failed${NEUTRAL}!
		echo
		echo Invalid results for ${f}
		echo Side by side comparison \(${f}.reference on the left, ${f}.translated on the right\)
		echo --
		# If delta is available, use it for pretty-printing. Otherwise use
		# regular diff
		if [[ "${DELTA}" == "" ]]; then
			${DIFF} --minimal --side-by-side ${f}.reference ${f}.translated
		else
			${DELTA} -s ${f}.reference ${f}.translated
		fi
		exit $?
	fi

done
echo -e ${GREEN}suceeded${NEUTRAL}!

F77="ifx -fixed -fiopenmp -fopenmp-targets=spir64"
# F77="nvfortran -mp -Mfixed"
F90="ifx -free -fiopenmp -fopenmp-targets=spir64"
# F90="nvfortran -mp -Mfree"
CC="icx -fiopenmp -fopenmp-targets=spir64 -fopenmp-version=51 -std=c99"
#CC="nvc -mp"

F77COMPILER=${F77%% *}
which ${F77COMPILER} &> /dev/null
if [[ $? -ne 0 ]]; then
	echo
	echo -e ${RED}Error!${NEUTRAL} Could not locate ${F77COMPILER} compiler
	exit 1
fi
F90COMPILER=${F90%% *}
which ${F90COMPILER} &> /dev/null
if [[ $? -ne 0 ]]; then
	echo
	echo -e ${RED}Error!${NEUTRAL} Could not locate ${F90COMPILER} compiler
	exit 1
fi
CCCOMPILER=${CC%% *}
which ${CCCOMPILER} &> /dev/null
if [[ $? -ne 0 ]]; then
	echo
	echo -e ${RED}Error!${NEUTRAL} Could not locate ${CCCOMPILER} compiler
	exit 1
fi

echo -n Compiling \(${nfiles}\)" "
curfile=0
for f in ${TESTS}
do
	curfile=$((curfile+1))
	if [[ (${curfile} == 1) || ($((curfile % 10)) == 0) ]]; then
		echo -n ${curfile}
	else
		echo -n .
	fi
	if [[ "${f: -2}" == ".f" ]]; then
		cp ${f}.translated tmp.f
		${F77} -fpp -c tmp.f
		COMPILE_STATUS=$?
		rm -f tmp.f tmp.o *.mod *.modmic
	elif [[ "${f: -4}" == ".f90" ]]; then
		cp ${f}.translated tmp.f90
		${F90} -fpp -c tmp.f90
		COMPILE_STATUS=$?
		rm -f tmp.f90 tmp.o *.mod *.modmic
	elif [[ "${f: -2}" == ".c" ]]; then
		cp ${f}.translated tmp.c
		${CC} -c tmp.c
		COMPILE_STATUS=$?
		rm -f tmp.c tmp.o
	fi
	if [[ ${COMPILE_STATUS} -ne 0 ]] ; then
		echo -e ${RED}failed${NEUTRAL} for file ${f}.translated
		echo
		exit ${COMPILE_STATUS}
	fi

done
echo -e ${GREEN}suceeded${NEUTRAL}!
