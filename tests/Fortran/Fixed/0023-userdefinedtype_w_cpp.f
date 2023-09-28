      module m_test
        implicit none
        private
        public t_date, t_hour, t_hour_ns

        type :: t_date
          integer :: year
          integer :: month
#if defined(A) && \
    defined(B)
          integer :: day
#endif // A & B
        end type

        type :: t_hour
          integer :: hour,
     1    minute
#ifdef C
          integer :: second ! ignore me
#endif // C
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
#if defined(A) && defined(B)
        tdate%day = 13
#endif

        !$acc serial copy(tdate)
        tdate%month = tdate%month + 1
        !$acc end serial

        thour1%hour = 23
        thour1%minute = 59
#ifdef C
        thour1%second = 58
#endif

        !$acc serial copyin(thour1)
        thour1%hour = thour1%hour - 1
        !$acc end serial

        !$acc serial copyout(thour2)
        thour2%hour = 23
        thour2%minute = 59
#if defined(C)
        thour2%second = 58
#endif
        thour2%nanosecond = 100
        !$acc end serial

      end program test
