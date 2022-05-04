      program test
      integer i
!$acc kernels
      i = 0
!$acc end kernels
      end program
