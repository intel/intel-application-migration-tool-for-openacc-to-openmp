       program test
       integer N
       integer i
!$acc parallel loop
       do i = 1, N
       enddo
!$acc parallel loop
c comment1
* comment2
! comment3
       do i = 1, N
       enddo
!$acc parallel
!$acc1 loop
       do i = 1, N
       enddo
       end program
