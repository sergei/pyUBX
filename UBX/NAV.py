"""Navigation Results Messages: i.e. Position, Speed, Time, Acceleration, Heading, DOP, SVs used. """

from UBXMessage import initMessageClass, addGet
from Types import U1, U4, I4, I2, I1, X1


@initMessageClass
class NAV:
    """Message class NAV."""

    _class = 0x01

    @addGet
    class TIMEGPS:
        """§32.18.26.1 GPS Time Solution."""

        _id = 0x20

        class Fields:
            iTOW = U4(1)
            fTOW = I4(2)
            week = I2(3)
            leapS = I1(4)
            valid = X1(5)
            tAcc = U4(6)

