module m
  implicit none
  type, public :: t
    integer :: i
    contains
    procedure :: plusone => m_plusone
  end type
  contains
    subroutine m_plusone(this)
     class (t), intent(inout) :: this
     this%i = this%i + 1
    end subroutine m_plusone
end module m
program p
  use m
  class(t), allocatable :: v
  allocate(v)
  write (*,*) v%i
  call v%plusone()
  write (*,*) v%i
  deallocate(v)
end program p
