program test

integer, parameter :: N = 10
integer, parameter :: M = 20
integer, parameter :: O = 30
real super_long_variable_name(N,M,O)
real ultra_long_variable_name_but_this_is_too_long(M)
real short_var(M)
real shorter(O)
integer x(N),y(N),z(N),v(N)

!$acc enter data copyin(super_long_variable_name(1:N,1:M,1:O)) &
!$acc copyin(ultra_long_variable_name_but_this_is_too_long(N:M)) &
!$acc copyin(short_var) copyin(shorter) copyin(x,y,z,v)

end program
