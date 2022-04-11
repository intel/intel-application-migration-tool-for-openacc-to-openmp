       program test
       integer i
!$acc parallel async(1)
       i = 0
!$acc end parallel
!$acc parallel async
       i = 0
!$acc end parallel
!$acc parallel async(2) wait
       i = 0
!$acc end parallel
!$acc wait(2)
       end program
