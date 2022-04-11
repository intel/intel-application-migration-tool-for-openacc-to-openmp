program test
integer, parameter :: N = 10
real v1(N),v2(N),v3(N),v4(N)
real v1a(N),v2a(N),v3a(N)

!$acc update device(v1) host(v2)

!$acc update device(v1) &
!$acc device(v2,v3)&
!$acc host(v4)

!$acc update device(v1) host(v1a) &
!$acc& device(v2) host(v2a) &
!$acc& device(v3) host(v3a)

end program
