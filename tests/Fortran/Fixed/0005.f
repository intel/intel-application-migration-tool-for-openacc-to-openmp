       program test
       integer, parameter :: N = 10
       real v1(N), v2(N), v3(N)

!$acc update device(v1)

!$acc update device(v1)
!$acc& device(v2,v3)

!$acc update device(v1)
!$acc1 device(v2)
!$acc2 device(v3)
       end program
