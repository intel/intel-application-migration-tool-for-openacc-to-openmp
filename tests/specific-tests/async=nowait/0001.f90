program test
integer i
!$acc kernels async(1)
i = 0
!$acc end kernels
!$acc kernels async(2)
i = 0
!$acc end kernels
!$acc wait(2)
!$acc wait
end program
