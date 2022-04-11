program app
implicit none
integer :: a

a = 0

!$acc serial &
    ! comment
!$acc copy(a) ! this is a comment
      a = 1
!$acc end serial

      write (*,*) a

!$acc serial & ! this is a comment in a multiline-statement
     ! ---
 !$acc copy(a)
      a = 2
  !$acc end & ! this is another comment in another multi-line statement
   !$acc serial

      write (*,*) a
end program app
