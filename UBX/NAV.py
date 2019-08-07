"""Navigation Results Messages: i.e. Position, Speed, Time, Acceleration, Heading, DOP, SVs used. """

from UBXMessage import initMessageClass, addGet
from Types import U1, U4, I4, I2, I1, X1, X4


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

    @addGet
    class SAT:
        """§32.18.17.1 Satellite Information."""

        _id = 0x35

        class Fields:
            iTOW = U4(1)
            version = U1(2)
            numSvs = U1(3)
            reserved1_1 = U1(4)
            reserved1_2 = U1(5)

            class Repeated:
                gnssId = U1(1)
                svId = U1(2)
                cno = U1(3)
                elev = I1(4)
                azim = I2(5)
                prRes = I2(6)
                flags = X4(7)

