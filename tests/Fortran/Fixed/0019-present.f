      program test
      implicit none
      integer :: v(10)
      integer :: i
      v(:) = 0

!$acc data create(v)
!$acc parallel loop present(v)
        do i = 1, 10
          v(i) = i
        end do
        write (*,*) "v(3) = ", v(3)
!$acc update host(v)
        write (*,*) "v(3) = ", v(3)
!$acc end data

!$acc data create(v)
!$acc parallel loop default(present)
        do i = 1, 10
          v(i) = i
        end do
        write (*,*) "v(3) = ", v(3)
!$acc update host(v)
        write (*,*) "v(3) = ", v(3)
!$acc end data

      end program
