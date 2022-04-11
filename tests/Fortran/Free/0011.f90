program dot
  implicit none
  integer, parameter :: N = 1024
  integer i
  real :: x(N), y(N)
  real :: dot1, dot2

  !$acc parallel loop reduction(+:dot1)
  do i = 1, N
    dot1 = x(i)*y(i)
  end do

  !$acc parallel loop reduction(+:dot1) reduction(+:dot2)
  do i = 1, N
    dot1 = x(i)*y(i)
    dot2 = y(i)*x(i)
  end do

end program
