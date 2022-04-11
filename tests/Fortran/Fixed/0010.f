      program test

      integer, parameter :: N = 10
      integer, parameter :: M = 20
      integer, parameter :: O = 30
      integer x(N),y(M),z(O)

!$acc data present(x)

!$acc end data

!$acc DATA
!$acc1 PRESENT(y)

!$acc end data

!$acc data
!$acc2 copy(X)
!$acc3 copyin(Y)
!$acc4 copyout(Z)

!$acc end data

!$acc data present (x)
!$acc end data

!$acc data
!$acc& copy (x)
!$acc& copyin(y) 
!$acc& copyout (z)
!$acc end DATA

      end program
