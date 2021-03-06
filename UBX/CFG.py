"""Configuration Input Messages: Set Dynamic Model, Set DOP Mask, Set Baud Rate, etc."""

from UBXMessage import UBXMessage, initMessageClass, addGet
import struct
from Types import U1, U2, U4, X2, X4, U, I2, I4, X1, I1


@initMessageClass
class CFG:
    """Message class CFG."""

    _class = 0x06

    @addGet
    class PMS:

        _id = 0x86

        class Fields:
            version = U1(1)
            powerSetupValue = U1(2)
            period = U2(3)
            onTime = U2(4)
            reserved = U2(5)

        class Set(UBXMessage):
            def __init__(self, powerSetupValue=1, period=0, onTime=0):
                payload = struct.pack(
                    '<BBhhBB', 0, powerSetupValue, period, onTime, 0, 0
                )
                UBXMessage.__init__(
                    self, CFG._class, CFG.PMS._id, payload
                )

    @addGet
    class GNSS:
        u"""GNSS system configuration. §31.11.10."""

        _id = 0x3E

        class Fields:
            msgVer = U1(1)
            numTrkChHw = U1(2)
            numTrkChUse = U1(3)
            numConfigBlocks = U1(4)

            class Repeated:
                gnssId = U1(
                    1,
                    allowed={
                        0: 'GPS',
                        1: 'SBAS',
                        2: 'Galileo',
                        3: 'BeiDou',
                        4: 'IMES',
                        5: 'QZSS',
                        6: 'GLONASS',
                    })
                resTrkCh = U1(2)
                maxTrkCh = U1(3)
                reserved = U1(4)
                flags = X4(5)

        class Set(UBXMessage):
            def __init__(self, cfgBlocks):
                msgVer = 0
                numTrkChHw = 0x20  # R/O anyway
                numTrkChUse = 0x20
                numConfigBlocks = len(cfgBlocks)

                payload = bytearray(4 + 8 * numConfigBlocks)
                offset = 0
                struct.pack_into(
                    '<BBBB', payload, offset,
                    msgVer, numTrkChHw, numTrkChUse, numConfigBlocks
                )
                offset += 4
                for cfg_block in cfgBlocks:
                    struct.pack_into(
                        '<BBBBI', payload, offset,
                        cfg_block['gnssId'], cfg_block['resTrkCh'], cfg_block['maxTrkCh'], 0, cfg_block['flags']
                    )
                    offset += 8

                UBXMessage.__init__(
                    self, CFG._class, CFG.GNSS._id, payload
                )

    @addGet
    class PM2:
        u"""§31.11.20 Extended Power Management configuration."""

        _id = 0x3B

        class Fields:
            version = U1(1)  # Message version (0x02 for this version)
            reserved1 = U1(2)  # Reserved
            maxStartupStartupDur = U1(
                3)  # Maximum time to spend in Acquisition state. If 0: bound disabled (see maxStartupStateDur). (not supported in protocol versions less than 17), (not supported in protocol versions 23 to 23.01)
            reserved2 = U1(4)  # Reserved
            flags = X4(5)  # PSM configuration flags (see graphic below)
            updatePeriod = U4(
                6)  # ms  Position update period. If set to 0, the receiver will never retry a fix and it will wait for external events
            searchPeriod = U4(
                7)  # ms  Acquisition retry period if previously failed. If set to 0, the receiver will never retry a startup (not supported in protocol versions 23 to 23.01)
            gridOffset = U4(
                8)  # ms  Grid offset relative to GPS start of week (not supported in protocol versions 23 to 23.01)
            onTime = U2(9)  # s  Time to stay in Tracking state (not supported in protocol versions 23 to 23.01)
            minAcqTime = U2(10)  # s  minimal search time
            reserved3 = U(11, 20)  # Reserved
            extintInactivityMs = U4(12)  # ms  inactivity time out on EXTINT pint if enabled

    @addGet
    class MSG:
        u"""§32.11.16.3 Set Message Rate.  (page 188)"""

        _id = 0x01

        class Fields:
            msgClass = U1(1)  # Message Class
            msgId = U1(2)  # Message Identifier
            rateI2C = U1(3)  # Send rate on I2C port
            rateUART1 = U1(4)  # Send rate on UART 1 port
            rateRes1 = U1(5)  # Send rate on port 4 (reserved)
            rateUSB = U1(6)  # Send rate on USB port
            rateSPI = U1(7)  # Send rate on SPI port
            rateRes2 = U1(8)  # Send rate on port 5 (reserved)

        class Set(UBXMessage):
            def __init__(self, msgClass=0, msgId=0, rate=None, rateI2C=None, rateUART1=None,
                         rateUSB=None, rateSPI=None):
                if rate:  # Set message rate configuration for the current port.
                    payload = struct.pack(
                        '<BBB', msgClass, msgId, rate,
                    )
                elif rateI2C:  # Set message rate configuration for all ports.
                    if not rateUART1:
                        raise ValueError('rateUART1 is not specified')
                    if not rateUSB:
                        raise ValueError('rateUSB is not specified')
                    if not rateSPI:
                        raise ValueError('rateSPI is not specified')
                    payload = struct.pack(
                        '<BBBBBBBB', msgClass, msgId, rateI2C, rateUART1, 0, rateUSB, rateSPI, 0
                    )
                else:  # Poll request
                    payload = struct.pack(
                        '<BB', msgClass, msgId
                    )

                UBXMessage.__init__(
                    self, CFG._class, CFG.MSG._id, payload
                )

    @addGet
    class RST:
        u"""§32.11.27.1 Reset Receiver / Clear Backup Data Structures.  (page 212)"""

        _id = 0x04

        class Fields:
            navBbrMask = X2(1)  # BBR Sections to clear. The following Special Sets
            # apply:
            # 0x0000 Hot start
            # 0x0001 Warm start
            # 0xFFFF Cold start

            resetMode = U1(2)  # Reset Type
            # 0x00 - Hardware reset (Watchdog) immediately
            # 0x01 - Controlled Software reset
            # 0x02 - Controlled Software reset (GNSS only)
            # 0x04 - Hardware reset (Watchdog) after
            # shutdown
            # 0x08 - Controlled GNSS stop
            # 0x09 - Controlled GNSS start

            reserved1 = U1(3)  # Reserved

        class Set(UBXMessage):
            def __init__(self, navBbrMask=0, resetMode=0):
                payload = struct.pack(
                    '<HBB', navBbrMask, resetMode, 0
                )

                UBXMessage.__init__(
                    self, CFG._class, CFG.RST._id, payload
                )

    @addGet
    class RATE:
        u"""§31.11.24 Navigation/Measurement Rate Settings."""

        _id = 0x08

        class Fields:
            measRate = U2(1)
            navRate = U2(2)
            timeRef = U2(
                3,
                allowed={
                    0: "UTC time",
                    1: "GPS time",
                    2: "GLONASS time",
                    3: "BeiDou time",
                    4: "Galileo time"
                })

    @addGet
    class RXM:
        u"""§31.11.27 RXM configuration.

        For a detailed description see section 'Power Management'.
        """

        _id = 0x11

        class Fields:
            reserved1 = U1(1)  # reserved
            lpMode = U1(  # Low Power Mode
                2,
                allowed={
                    0: "Continuous Mode",
                    1: "Power Save Mode",
                    4: "Continuous Mode"  # for ver>=14 0 and 4 are the same
                }
            )

    class PRT:
        u"""§31.11.22.4 Port Configuration."""

        _id = 0x00

        class Fields:
            portID = U1(1)
            reserved1 = U1(2)
            txReady = X2(3)
            mode = X4(4)
            reserved2 = U4(5)
            inProtoMask = X2(6)
            outProtoMask = X2(7)
            flags = X2(8)
            reserved3 = U2(9)

    class PRT_GET:
        u"""§31.11.22.4 Port Configuration."""

        _id = 0x00

        class Fields:
            portID = U1(1)

    @addGet
    class TP5:
        u"""§31.11.32.3 Time Pulse Parameters."""

        _id = 0x31

        class Fields:
            tpIdx = U1(1)  # Time pulse selection (0 = TIMEPULSE, 1 = TIMEPULSE2)
            version = U1(2)  # Message version (0x00 for this version)
            reserved2 = U2(3)
            antCableDelay = I2(4)  # Antenna cable delay
            rfGroupDelay = I2(5)  # RF group delay
            freqPeriod = U4(6)  # Frequency or period time, depending on setting of bit 'isFreq'
            freqPeriodLock = U4(
                7)  # Frequency or period time when locked to GPS time, only used if 'lockedOtherSet' is set
            pulseLenRatio = U4(8)  # Pulse length or duty cycle, depending on 'isLength'
            pulseLenRatioLock = U4(
                9)  # Pulse length or duty cycle when locked to GPS time, only used if 'lockedOtherSet' is set
            userConfigDelay = I4(10)  # User configurable time pulse delay
            flags = X4(11)  # Configuration flags

    class TP5_GET:
        u"""§31.11.32.2 Poll Time Pulse Parameters."""

        _id = 0x00

        class Fields:
            tpIdx = U1(1)  # Time pulse selection (0 = TIMEPULSE, 1 = TIMEPULSE2)

    @addGet
    class INF:
        """32.11.13.2 Information message configuration."""

        _id = 0x02

        class Fields:
            class Repeated:
                protocolID = U1(
                    1,
                    allowed={
                        0: 'UBX',
                        1: 'NMEA',
                        255: 'Reserved',
                    })
                reserved1_1 = U1(2)
                reserved1_2 = U1(3)
                reserved1_3 = U1(4)
                infMsgMask = X1(5)

    @addGet
    class NAV5:
        """32.11.17.1 Navigation Engine Settings."""

        _id = 0x24

        class Fields:
            mask = X2(1)
            dynMode1 = U1(2)
            fixMode = U1(3)
            fixedAlt = I4(4)
            fixedAltVar = U4(5)
            minElev = I1(6)
            drLimit = U1(7)
            pDop = U2(8)
            tDop = U2(9)
            pAcc = U2(10)
            tAcc = U2(11)
            staticHoldThr = U1(12)
            dgnssTimeout = U1(13)
            cnoThreshNumSvs = U1(14)
            cnoThres = U1(15)
            reserved1_1 = U1(16)
            reserved1_2 = U1(17)
            staticHoldMaxDist = U2(18)
            utcStandard = U1(19)
            reserved2_1 = U1(20)
            reserved2_2 = U1(21)
            reserved2_3 = U1(22)
            reserved2_4 = U1(23)
            reserved2_5 = U1(24)

        class Set(UBXMessage):
            def __init__(self, mask=0, dynMode1=0, fixMode=0, fixedAlt=0, fixedAltVar=0,
                         minElev=0, drLimit=0, pDop=0, tDop=0, pAcc=0, tAcc=0,
                         staticHoldThr=0, dgnssTimeout=0, cnoThreshNumSvs=0,
                         cnoThres=0, staticHoldMaxDist=0, utcStandard=0):
                payload = struct.pack(
                    '<HBBlLbBHHHHBBBBBBHBBBBBB',
                    mask, dynMode1, fixMode, fixedAlt, fixedAltVar, minElev, drLimit,
                    pDop, tDop, pAcc, tAcc, staticHoldThr, dgnssTimeout, cnoThreshNumSvs, cnoThres,
                    1, 2, staticHoldMaxDist, utcStandard, 1, 2, 3, 4, 5
                )

                UBXMessage.__init__(
                    self, CFG._class, CFG.NAV5._id, payload
                )

    @addGet
    class NMEA:
        """32.10.21.3 Extended NMEA protocol configuration V1."""

        _id = 0x17

        class Fields:
            filterFlags = X1(1)
            nmeaVersion = U1(2)
            numSV = U1(3)
            flags = X1(4)
            gnssToFilter = X4(5)
            svNumbering = U1(6)
            mainTalkerId = U1(7)
            gsvTalkerId = U1(8)
            version = U1(9)
            bdsTalkerId_1 = U1(10)
            bdsTalkerId_2 = U1(11)
            reserved1_1 = U1(12)
            reserved1_2 = U1(13)
            reserved1_3 = U1(14)
            reserved1_4 = U1(15)
            reserved1_5 = U1(16)
            reserved1_6 = U1(17)

        class Set(UBXMessage):
            def __init__(self, filterFlags=0, nmeaVersion=0, numSV=0, flags=0, gnssToFilter=0, svNumbering=0,
                         mainTalkerId=0, gsvTalkerId=0, version=0, bdsTalkerId_1=0, bdsTalkerId_2=0):
                payload = struct.pack(
                    '<BBBBLBBBBBBBBBBBB',
                    filterFlags, nmeaVersion, numSV, flags, gnssToFilter, svNumbering, mainTalkerId,
                    gsvTalkerId, version, bdsTalkerId_1, bdsTalkerId_2, 1, 2, 3, 4, 5, 6
                )

                UBXMessage.__init__(
                    self, CFG._class, CFG.NMEA._id, payload
                )
