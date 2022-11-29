module testmodule
  contains
  function meaningoflife(N)
    !$acc routine
    implicit none
    integer :: N
    integer :: meaningoflife
    meaningoflife = 42 + N
  end function
  subroutine foo (N, R)
    implicit none
    integer, intent(in) :: N
    integer, intent(out) :: R
    !$acc routine
    R = N + R
  end subroutine
end module

program app
  use testmodule
  integer :: res1, res2
  integer :: N

  !$acc serial copyout(res1, res2)
  call foo(N,res1)
  res2 = meaningoflife(N)
  !$acc end serial

  write (*,*) res1 .eq. res2
end program
