       program test
       integer, parameter :: N = 1000
       integer, parameter :: M = 2000
       real v1(N), v2(N), v3(M), v4(N)
       logical condA, condB, condC

!$acc enter data copyin(v1,v2(1:N))

!$acc enter data copyin(v1,v2)
!$acc& copyin(v3(2:M),v4(5))

!$acc enter data copyin(v1,v2)
!$acc1 copyin(v3,v4(1:N))

!$acc enter data copyin(v1,v2,
!$acc1 v3
!$acc2 ,v4(N:M))

!$acc exit data copyout(v1,v2(1:N))

!$acc exit data copyout(v1,v2)
!$acc& copyout(v3(2:M),v4(5))

!$acc exit data copyout(v1,v2)
!$acc1 copyout(v3,v4(1:N))

!$acc exit data copyout(v1,v2,
!$acc1 v3
!$acc2 ,v4(N:M))

!$acc enter data copyin(v1, v2)
!$acc& create(v3, v4)
!$acc& if ((condA .and. condB)
!$acc& .or. (condA .and. condC))

       end program
