<a name="top"></a>

# Intel&reg; Application Migration Tool for OpenACC* to OpenMP* API
A tool that helps migrating OpenACC-based applications into OpenMP

## Table of contents

+ [What is Intel Application Migration Tool for OpenACC to OpenMP API?](#what-is-intel-application-migration-tool-for-openacc-to-openmp-api)
+ [Requirements](#requirements)
+ [Status](#status)
+ [Using the tool](#using-the-tool)
+ [Experimental features](#experimental-features)
+ [Examples](EXAMPLES.md)
+ [Known issues](#known-issues)
+ [Copyrights](#copyrights)


## What is Intel Application Migration Tool for OpenACC to OpenMP API?

The Intel Application Migration Tool for OpenACC to OpenMP API is a Python3-based tool that helps developers to migrate OpenACC applications into OpenMP by the means of the offloading mechanisms. The tool takes application sources (either C/C++ or Fortran languages) with OpenACC constructs and generates a semantically-equivalent source using OpenMP. Since the tool is under active development, it does not rely on compiler-infrastructures and the existing divergences between OpenACC and OpenMP specifications, the translation may need some tweaking. So, **the user takes the responsability of supervising the generated code**.

The tool does not aim at guaranteeing the best achievable performance but at generating a semantically equivalent translation. The tool tries to generate the most efficient translation but there are a number of performance tweaks (_e.g._ hardware binding (gangs, workers, vector length)) that are unlikely to be performant-portable among other hardware. This is why, once the application has been successfully ported, we encourage developers and users to use performance tools for tuning their application performance.

Go to [top](#top)

## Requirements

* Python 3.6

Go to [top](#top)

## Status

The tool recognizes many  of the OpenACC compute and data constructs but cannot translate OpenACC API calls at the moment. The tool generates a source file with the original contents plus the OpenMP translated constructs. These constructs can be wrapped using `#ifdef` and `#endif` pre-processing directives.

Given the semantic differences between some OpenACC constructs and their closest OpenMP constructs, there are a few caveats that users should be aware:

*  The _kernels_ construct is a prescriptive construct for the OpenACC compiler to automatically extract the parallelism from the code enclosed by the construct and it has no direct OpenMP counter-part. The tool, by default, converts this construct into a serial offloaded region because it cannot identify potential parallelism. However, the tool also provides a few experimental knobs to take advantage of loops within kernels annotated with the _loop_ construct.
*  The _present_ data-mapping clause does exist in recent OpenMP specifications, however there are compilers that do not support it yet. The tool provides a few alternatives that would mimic this clause but at the expense of performance.
*  Similarly as above, the _loop_ construct appeared in recent OpenMP specifications. The tool suggests using this construct over using other alternatives (e.g. _for_ and _do_).
*  The asynchronous mechanisms in OpenACC and OpenMP differ. For the time being, the tool has a very naive support to migrate the _async_ and _wait_ constructs that may map correctly on applications that use them in a simple manner.
*  The _routine_ construct is currently only implemented in Fortran and implementation for C/C++ is WIP.
*  The hardware binding clauses (_gangs, workers, vector length_) are ignored by default. However, the tool user can migrate these clauses into the OpenMP translation to evaluate the performance impact.

In addition to these, the tool generates a report for each migrated file with information about the suggested translation and potential issues/warnings related to either the original or the suggested codes.

## Using the tool

To invoke the translator, use the following command: 

       <path>/src/intel-application-migration-tool-for-openacc-to-openmp <optional-flags> <input-files>

where `<input-files>` refers to source-code files containing OpenACC constructs. For each given input-file, the tool will generate a translation file named `<input-file>.translated` and will also dump a report with translation details into a file named `<input-file>.report`.

The tool supports the following optional flags:

* `-[no-]force-backup` (default: **disabled**)
Enforces the translator to write a backup file with .original extension of the processed file even if a backed up file exists. If disabled, the tool will refuse to proceed with the translation.
* `-[no-]generate-report` (default: **enabled**)
Generates a translation report into a separate file with the .report extension.
* `-[no-]generate-multidimensional-alternate-code` (default: **enabled**)
Provides implementation suggestions for _acc enter_/_acc exit_ constructs to be employed if the multi-dimensional data is non-contiguous (only in C).
* `-keep-binding-clauses=[none,all,gang,worker,vector]` (defaut: **none**)
Specifies which OpenACC hardware binding clauses (none, all, or a comma-separated combination of:_gang_, _worker_ or _vector_) are kept in the translation.
* `-[no-]overwrite-input` (default: **disabled**)
When enabled, the translator will overwrite the input file with the translation file.
* `-present=<alloc,tofrom,keep>` (default: **keep**)
Specifies how the tool translates OpenACC's present clause:
    * `alloc` -- into OpenMP's _map(alloc)_.
    * `tofrom` -- into OpenMP's _map(tofrom)_. Note that this is may be less performant.
    * `keep` -- keep using the present clause but using the OpenMP approach -- but note that this requires OpenMP 5.0+ compatible compiler.
* `-async=<ignore,nowait>` (default: **nowait**)
Selects how the async OpenACC clauses are translated.
   * `ignore` -- do ignore the _async_ and _wait_ clauses -- note that this might have a performance impact.
   * `nowait` -- convert into _nowait_ and _taskwait_ clauses but this is not semantically equivalent to OpenACC.
* `-[no-]suppress-openacc` (default: **disabled**)
The translator removes the OpenACC constructs in the translated file.
* `-[no-]translated-openmp-conditional-define` (default: **disabled**)
The tool wraps the translated OpenMP code with `#if defined(OPENACC2OPENMP_TRANSLATED_OPENMP)` pre-processing macros.
* `-translated-openmp-conditional-define=X`
The tool wraps the translated OpenMP code with `#if defined(X)` pre-processing macros.
* `-[no-]original-openmp-conditional-define` (default: **enabled**)
The tool wraps the original OpenMP code with `#if defined(OPENACC2OPENMP_ORIGINAL_OPENMP)` pre-processing macros.
* `-original-openmp-conditional-define=X`
The tool wraps the original code with `#if defined(X)` pre-processing macros.

Go to [top](#top)

## Experimental features

The tool supports some experimental features which are under development.

* `-[no-]experimental-kernels-support` (default: **disabled**)
On Fortran codes, the tool breaks the _loop_ constructs nested within _kernels_ into independent code regions to be executed back-to-back.
**NOTE**: Resulting code may not OpenMP compliant -- depending on the _kernels_ and _loop_ locations. In some circumstances, you may need to manually change the code.
**PERFORMANCE NOTE**: This feature might inject OpenMP constructs that lead to empty-kernel executions. We encourage you to visit the code and manually remove the existing empty-kernels, if any.
* `-[no-]experimental-remove-kernels-bubbles` (default: **disabled**)
This option attempts to remove empty OpenMP _target_ and _end target_ constructs injected through the use of `-experimental-kernels-support`.

Go to [top](#top)

## Known issues

These are the currently known issues:

* The _kernels_ construct is supported but there will appear issues when there exist control flow instructions between the _kernels_ and subsequent _loop_ constructs. Such as:
```
!$acc kernels
if (X) then
  !$acc loop
  do i = ..
  end do
end if
```
A potential workaround is to move the _kernels_ construct immediately before the _loop_ construct.

* The code parser is not able to process OpenACC constructs intertwined with preprocessor commands, such as:
```
!$acc parallel &
#if defined(X)
!$acc loop 
#else
!$acc loop vector
#endif
```
A potential solution for this is to move the preprocessor commands outside the OpenACC constructs, like:
```
#if defined(X)
!$acc parallel loop
#else
!$acc parallel loop vector
#endif
```

* The _auto_ clause from the _loop_ construct is currently ignored and the _loop_ construct is converted into a parallel loop. This may break the semantics of the migration because this tool does not search for dependencies.

Go to [top](#top)

## Copyrights

&copy; 2022 Harald Servat, Intel Corporation

Intel is a trademark of Intel Corporation or its subsidiaries.

\* Other names and brands may be claimed as the property of others.

We welcome anyone interested in using, developing or contributing to Intel Application Migration Tool for OpenACC to OpenMP API!

Go to [top](#top)
