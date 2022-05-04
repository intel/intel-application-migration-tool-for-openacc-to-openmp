      program test
      integer i
!$acc kernels async(1)
      i = 0
!$acc end kernels
!$acc kernels async(2) wait(1)
      i = 0
!$acc end kernels
!$acc kernels async(3) wait (2)
      i = 0
!$acc end kernels
!$acc wait
      end program
