<a name="top"></a>

# Examples using the Intel&reg; Application Migration Tool for OpenACC* to OpenMP* API*

## POT3D

+ [Download the migration tool](#download-the-migration-tool)
+ [Download POT3D](#download-pot3d)
+ [Migrate POT3D](#migrate-pot3d)
+ [Adapt POT3D Makefile](#adapt-pot3d-makefile)

### Download the migration tool

Download the Intel&reg; Application Migration Tool for OpenACC\* to OpenMP\* API by cloning this repository.

```
$ git clone https://github.com/intel/intel-application-migration-tool-for-openacc-to-openmp
Cloning into 'intel-application-migration-tool-for-openacc-to-openmp'...
remote: Enumerating objects: 307, done.
remote: Counting objects: 100% (307/307), done.
remote: Compressing objects: 100% (203/203), done.
remote: Total 307 (delta 132), reused 275 (delta 102), pack-reused 0
Receiving objects: 100% (307/307), 86.24 KiB | 9.58 MiB/s, done.
Resolving deltas: 100% (132/132), done.
```

Go to [top](#top)

### Download POT3D

Download the POT3D code by cloning its repository.

```
~/apps $ git clone https://github.com/predsci/POT3D
Cloning into 'POT3D'...
remote: Enumerating objects: 211, done.
remote: Counting objects: 100% (3/3), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 211 (delta 1), reused 0 (delta 0), pack-reused 208
Receiving objects: 100% (211/211), 24.56 MiB | 12.56 MiB/s, done.
Resolving deltas: 100% (102/102), done.
```

The migration tool has been validated with the following commit-id, although it might work on more recent versions of the application.

```
$ git checkout 42984a8ce428d54036d6b8a0732f05a046e8f840
Note: switching to '42984a8ce428d54036d6b8a0732f05a046e8f840'.
..
HEAD is now at 42984a8 RMC: POT3D v3.1.0 - Cleaned up code, added analytic validation run mode, updated documentation and scripts.

```

Go to [top](#top)

### Migrate POT3D

Let's apply the migration tool to convert the OpenACC statements found in all Fortran files. At the moment of writing this document, the asynchrounous capabilities of the migration tool are quite limited (only supporting naive asynchronism), and this is why the option `-async=ignore` is suggested.
When applying apply this process on already translated files, the tool should reject repeating the translation because that would overwrite the backup files. To avoid this issue, use `-force-backup` option.

```
~/apps/POT3D/src $ ~/intel-application-migration-tool-for-openacc-to-openmp/src/intel-application-migration-tool-for-openacc-to-openmp -async=ignore *.f
Processing file number_types.f
Processing file pot3d.f
Processing file zm_parse.f
Processing file zm_parse_modules.f
Processing file zm_sds.f
Processing file zm_sds_modules.f
```

Go to [top](#top)

### Adapt POT3D Makefile

At this point, you should be able to build the POT3D binary. However, before proceeding the Makefile needs to be adapted so that it uses an OpenMP compiler with support for offloading. In the summarized Makefile below, the Makefile has been changed to use Intel's MPI compiler wrapper invoking the Intel's IFX compiler.

```
~/apps/POT3D/src $ cat Makefile.ifx
FC = mpiifort -fc=ifx
FFLAGS = -fiopenmp -fopenmp-targets=spir64 -mllvm -vpo-paropt-atomic-free-reduction=true -O -g -mcmodel=medium -I$(HDF5_HOME)/include
OBJS = number_types.o \
 zm_parse_modules.o \
 zm_parse.o \
 zm_sds_modules.o \
 zm_sds.o \
 pot3d.o
LDFLAGS = -L$(HDF5_HOME)/lib -Wl,-rpath -Wl,$(HDF5_HOME)/lib -lhdf5_fortran -lhdf5_hl_fortran -lhdf5 -lhdf5_hl

all:    $(OBJS)
        $(FC) $(FFLAGS) $(OBJS) $(LDFLAGS) -o pot3d
        rm *.mod *.o 2>/dev/null
clean:
        rm pot3d 2>/dev/null
        rm -f *.mod *.o 2>/dev/null
number_types.o: number_types.f
        $(FC) -c $(FFLAGS) $<
zm_parse_modules.o: zm_parse_modules.f
        $(FC) -c $(FFLAGS) $<
zm_parse.o: zm_parse.f zm_parse_modules.f number_types.f
        $(FC) -c $(FFLAGS) $<
zm_sds_modules.o: zm_sds_modules.f
        $(FC) -c $(FFLAGS) $<
zm_sds.o: zm_sds.f zm_sds_modules.f number_types.f
        $(FC) -c $(FFLAGS) $<
pot3d.o: pot3d.f
        $(FC) -c $(FFLAGS) $<
```

Go to [top](#top)

