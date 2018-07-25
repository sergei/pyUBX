"""Receiver Manager Messages: i.e. Satellite Status, RTC Status. """

from UBXMessage import initMessageClass, addGet
from Types import U1, U4


@initMessageClass
class RXM:
    """Message class RXM."""

    _class = 0x02

    @addGet
    class SFRBX:
        """§32.19.7.2 Broadcast Navigation Data Subframe."""

        _id = 0x13

        class Fields:
            gnssId = U1(1)
            svId = U1(2)
            reserved1 = U1(3)
            freqId = U1(4)
            numWords = U1(5)
            chn = U1(6)
            ver = U1(7)
            reserved2 = U1(8)

            class Repeated:
                dwrd = U4(1)

