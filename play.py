#!/usr/bin/env python3
"""A space to play around with messages."""

import UBX
from UBXMessage import parseUBXPayload, parseUBXMessage

if __name__ == '__main__':

    print("UBX.ACK.ACK.Get: ", UBX.ACK.ACK.Get().serialize())

    print("UBX.CFG.PMS.Get: ", UBX.CFG.PMS.Get().serialize())

    print("UBX.CFG.PMS.Set: ", UBX.CFG.PMS.Set(powerSetupValue=2).serialize())

    print("UBX.MON.VER.Get: ", UBX.MON.VER.Get().serialize())

    print("UBX.TEST.TEST.Get: ", UBX.TEST.TEST.Get().serialize())

    print(parseUBXPayload(0x05, 0x01, b'12'))

    print(parseUBXPayload(0x05, 0x00, b'gh'))

    print(parseUBXPayload(UBX.TEST._class, UBX.TEST.TEST._id,
                          b'\x80\xff\x01\x00\x02\x00'))

    # CFG-GNSS
    msg = b'\x00\x20\x20\x07\x00\x08\x10\x00\x01\x00\x01\x01\x01\x01\x03\x00\x01\x00\x01\x01\x02\x04\x08\x00\x00\x00\x01\x01\x03\x08\x10\x00\x00\x00\x01\x01\x04\x00\x08\x00\x00\x00\x01\x03\x05\x00\x03\x00\x01\x00\x01\x05\x06\x08\x0e\x00\x01\x00\x01\x01'
    print(parseUBXPayload(UBX.CFG._class, UBX.CFG.GNSS._id, msg))

    gps = {'gnssId': 0, 'resTrkCh': 12, 'maxTrkCh': 12, 'flags': 0x01010001}
    sbas = {'gnssId': 1, 'resTrkCh': 0, 'maxTrkCh': 0, 'flags': 0x01010000}
    gal = {'gnssId': 2, 'resTrkCh': 8, 'maxTrkCh': 8, 'flags': 0x01010001}
    bds = {'gnssId': 3, 'resTrkCh': 4, 'maxTrkCh': 4, 'flags': 0x01010001}
    imes = {'gnssId': 4, 'resTrkCh': 0, 'maxTrkCh': 0, 'flags': 0x01010000}
    qzss = {'gnssId': 5, 'resTrkCh': 0, 'maxTrkCh': 0, 'flags': 0x01010000}
    glo = {'gnssId': 6, 'resTrkCh': 8, 'maxTrkCh': 8, 'flags': 0x01010001}
    cfgBlocks = [ gps, sbas, gal, bds, imes, qzss, glo]
    msg = UBX.CFG.GNSS.Set(cfgBlocks)
    cfg_gnss_bytes = msg.serialize()
    print("UBX.CFG.GNSS.Set: ", cfg_gnss_bytes)
    print(parseUBXMessage(cfg_gnss_bytes))


    # MON-VER
    msg = b'\x52\x4f\x4d\x20\x43\x4f\x52\x45\x20\x33\x2e\x30\x31\x20\x28\x31\x30\x37\x38\x38\x38\x29\x00\x00\x00\x00\x00\x00\x00\x00\x30\x30\x30\x38\x30\x30\x30\x30\x00\x00\x46\x57\x56\x45\x52\x3d\x53\x50\x47\x20\x33\x2e\x30\x31\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x50\x52\x4f\x54\x56\x45\x52\x3d\x31\x38\x2e\x30\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x47\x50\x53\x3b\x47\x4c\x4f\x3b\x47\x41\x4c\x3b\x42\x44\x53\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x53\x42\x41\x53\x3b\x49\x4d\x45\x53\x3b\x51\x5a\x53\x53\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    print(parseUBXPayload(UBX.MON._class, UBX.MON.VER._id, msg))

    # CFG-MSG
    msg = UBX.CFG.MSG.Set(msgClass=6, msgId=7, rate=8)
    print("UBX.CFG.MSG.Set: ", msg.serialize())

    msg = UBX.CFG.MSG.Set(msgClass=6, msgId=7)
    print("UBX.CFG.MSG.Set: ", msg.serialize())

    msg = UBX.CFG.MSG.Get()
    print("UBX.CFG.MSG.Get: ", msg.serialize())
