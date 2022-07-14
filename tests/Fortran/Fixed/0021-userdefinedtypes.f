      module m_test
          implicit none
          type test_type_allocatable
          integer n
          real, allocatable :: datum(:)
          end type
          type test_type_pointer
          integer n
          real, allocatable :: datum(:)
          end type
      end module

      program test
        use m_test
        implicit none
        type(test_type_allocatable) :: tta
        type(test_type_pointer) :: ttp

        tta%N = 123
        allocate (tta%datum(tta%N))
        tta%datum = 0

!$acc serial copy(tta)
          tta%datum(10) = 123
!$acc end serial

        if (sum(tta%datum) == 123) then
          write (*,*) "Success"
        else
          write (*,*) "Failure"
        endif

        ttp%N = 123
        allocate (ttp%datum(ttp%N))
        ttp%datum = 0

!$acc serial copy(ttp)
          ttp%datum(100) = 321
!$acc end serial

        if (sum(ttp%datum) == 123) then
          write (*,*) "Success"
        else
          write (*,*) "Failure"
        endif

      end program
