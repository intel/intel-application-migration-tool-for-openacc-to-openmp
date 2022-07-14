      module m_test
        implicit none
        private
        public t_date, t_hour, t_hour_ns

        type :: t_date
          integer :: year, month, day
        end type

        type :: t_hour
          integer :: hour,
     1    minute,
C ignore me
     2    second ! ignore me
        end type

        type, extends(t_hour) :: t_hour_ns
          integer :: nanosecond
        end type

      end module m_test

      program test
        use m_test
        implicit none
        type(t_date) :: tdate
        type(t_hour) :: thour1
        type(t_hour_ns) :: thour2

        tdate%year = 2022
        tdate%month = 7
        tdate%day = 13

        !$acc serial copy(tdate)
        tdate%month = tdate%month + 1
        !$acc end serial

        thour1%hour = 23
        thour1%minute = 59
        thour1%second = 58

        !$acc serial copyin(thour1)
        thour1%hour = thour1%hour - 1
        !$acc end serial

        !$acc serial copyout(thour2)
        thour2%hour = 23
        thour2%minute = 59
        thour2%second = 58
        thour2%nanosecond = 100
        !$acc end serial

      end program test
