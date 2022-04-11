program test
implicit none
integer i, j, k, l, m

  !$acc kernels
  !$acc loop
  do i = 1, 10
    !$acc loop
    do j = 1, 10
    end do
  end do
  l = 1
  m = 2
  !$acc loop
  do i = 1, 10
    !$acc loop
    do j = 1, 10
    end do
  end do
  !$acc loop
  do i = 1, 10
    !$acc loop
    do j = 1, 10
      do k = 1, 3
      enddo
    enddo
    !$acc loop
    do j = 1, 10
    enddo
  enddo
  !$acc end kernels

end program
