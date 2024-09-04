      program test
      implicit none
      integer i,j
      real vec(1000)

!$acc parallel loop num_workers(10) copy (vec)
      do i = 1, 1000
        vec(i) = i+1
      end do

!$acc parallel num_gangs(2) copy (vec)
!$acc loop gang
      do i = 1, 1000
        vec(i) = i+2
      end do
!$acc end parallel

!$acc parallel num_workers(10) num_gangs(2) copy (vec)
!$acc loop
      do i = 1, 1000
        vec(i) = i+3
      end do
!$acc end parallel

!$acc parallel num_workers(10) num_gangs(2) copy(vec) if (1.eq.1)
!$acc loop vector
      do i = 1, 1000
        vec(i) = i+4
      end do
!$acc end parallel

!$acc parallel loop vector vector_length(8)
      do i = 1, 1000
        vec(i) = i+5
      end do

!$acc parallel loop
      do i = 1, 1000
!$acc loop seq
        do j = 1, 1000
          vec(i) = i+5
        end do
      end do

!$acc parallel loop
      do i = 1, 1000
!$acc loop
        do j = 1, 1000
          vec(i) = i+5
        end do
      end do

      end program
