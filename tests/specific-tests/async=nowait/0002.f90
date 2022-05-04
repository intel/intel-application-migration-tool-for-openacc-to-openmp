program test
integer i
!$acc parallel async(1)
i = 0
!$acc end parallel
!$acc parallel async(2)
i = 0
!$acc end parallel
!$acc parallel async(3) wait(1,2)
i = 0
!$acc end parallel
!$acc wait
end program
