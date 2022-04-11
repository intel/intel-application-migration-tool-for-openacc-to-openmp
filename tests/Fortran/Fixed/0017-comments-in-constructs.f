      program app
      implicit none
      integer :: a

      a = 0

!$acc serial ! this is a comment
c
!$acc1 copy(a)
      a = 1
!$acc end serial

      write (*,*) a

!$acc serial
c
!$acc1 copy(a) ! this is another comment
      a = 2
!$acc end
!$acc1 serial

      write (*,*) a

      end program
