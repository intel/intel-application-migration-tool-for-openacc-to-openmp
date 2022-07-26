<a name="top"></a>

# Examples using the Intel&reg; Application Migration Tool for OpenACC* to OpenMP* API

## POT3D

+ [Download the migration tool](#download-the-migration-tool)
+ [Download POT3D](#download-pot3d)
+ [Migrate POT3D](#migrate-pot3d)
+ [Adapt POT3D Makefile](#adapt-pot3d-makefile)

### Download the migration tool

Go to [top](#top)

### Download POT3D

Go to [top](#top)

### Migrate POT3D

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

