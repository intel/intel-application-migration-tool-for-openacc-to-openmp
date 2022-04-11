program test
integer i
!$acc parallel
i = 0
!$acc end parallel
end program
