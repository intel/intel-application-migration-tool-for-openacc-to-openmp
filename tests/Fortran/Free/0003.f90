program test
integer N
integer i

!$acc parallel &
!$acc & loop
      do i = 1, N
      enddo

!$acc parallel &
!$acc loop
      do i = 1, N
      enddo

!$acc parallel &
!$acc loop
      do i = 1, N
      enddo

!$acc parallel &
!$acc     & loop
      do i = 1, N
      enddo

!$acc parallel &

!$acc     & loop
      do i = 1, N
      enddo

!$acc parallel &
! comment inside
!$acc     & loop
      do i = 1, N
      enddo

!$acc parallel &
!$acc     & loop
! comment outside
      do i = 1, N
      enddo

end program
