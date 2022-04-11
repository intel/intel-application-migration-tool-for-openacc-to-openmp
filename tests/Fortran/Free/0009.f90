program test

integer, parameter :: N = 10
integer :: i
integer :: A(N)

!$acc kernels

!$acc loop
   do i = 1,N
    a(i) = i
   end do

!$acc end kernels

!$acc kernels
!$acc loop
   do i = 1,N
    a(i) = i
   end do
!$acc end kernels

!$acc kernels loop
   do i = 1,N
    a(i) = i+1
   end do

! This is unsupported as of nvfortran 22.2-0
! !$acc kernels
!    BLOCK
!      integer :: j
!      !$acc loop
!      do j = 1, N
!        a(j) = i + j
!      end do
!    END BLOCK
!
! !$acc kernels
!    BLOCK
!      integer :: j
!      !$acc loop
!      do j = 1, N
!        a(j) = i + j
!      end do
!    ENDBLOCK

end program
