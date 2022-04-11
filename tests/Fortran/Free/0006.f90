program test
integer, parameter :: N = 10
real v1(N), v2(N), v3(N)

!$acc update host(v1)

!$acc update host(v1) &
!$acc& host(v2,v3)

!$acc update host(v1) &
!$acc host(v2) &
!$acc host(v3)

end program
