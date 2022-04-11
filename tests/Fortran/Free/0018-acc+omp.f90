program test
integer :: a, b, r, i

!$acc serial copy(a) copy(b)
!$omp target map(a,b)
  b = 2*a
!$acc end serial
!$omp end target

!$acc serial copy(a) &
!$acc  copy(b)
!$omp target &
!$omp  map(a,b)
  b = 2*a
!$acc end serial
!$omp end target

!$acc serial copy(a) &
!$acc  copy(b)
!$omp target &
!$omp  map(tofrom:a) &
!$omp  map(tofrom:b)
  b = 2*a
!$acc end serial
!$omp end target

r = 0
!$acc parallel
!$acc loop reduction(+:r)
!$omp target teams
!$omp loop reduction(+:r)
do i = a, b
  r = r + a*a
end do
!$omp end target teams
!$acc end parallel

end program
