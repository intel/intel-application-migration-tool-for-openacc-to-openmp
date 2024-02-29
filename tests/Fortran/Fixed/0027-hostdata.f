      program main
      integer :: a(1000),b(1000)
      integer :: i
      !$acc data copyin(a,b)
        !$acc kernels
        do i = 1, 1000
          a(i) = i
        enddo
        !$acc end kernels
        !$acc host_data use_device(a,b)
        !$acc end host_data
      !$acc end data
      end program
