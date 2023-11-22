      subroutine foo(a, b, n)
      implicit none
      integer :: a(:)
      integer :: b(:)
      integer :: n
      integer :: i

!$acc kernels copyin(a)
!$acc loop
      do i=1,n
        a(i) = i + 1
      enddo
!$acc end kernels

!$acc kernels copyin(a) copyout(b)
!$acc loop
      do i=1,n
        b(i) = a(i) + 1
      enddo
!$acc end kernels

!$acc kernels copyin(a) copyout(b)
!$acc loop
      do i=1,n
        a(i) = i + 1
      enddo
!$acc loop
      do i=1,n
        b(i) = a(i) + 1
      enddo
!$acc end kernels

!$acc kernels loop copyin(a) copyout(b)
      do i=1,n
        b(i) = a(i) + 1
      enddo
!$acc end kernels loop

      end subroutine foo

