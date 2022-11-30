module oacc2omp_sync_support_f
  use iso_c_binding, only : c_char
  implicit none
  integer, parameter :: oacc2omp__sync_dep_array_size = 1024*1024
  character(kind=c_char) :: oacc2omp__sync_dep_array(0:oacc2omp__sync_dep_array_size-1)
    bind(c, name="__oacc2omp_sync_dep_array") :: oacc2omp__sync_dep_array
end module oacc2omp_sync_support_f
