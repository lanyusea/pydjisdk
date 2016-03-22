from ..utils import *

import struct
import ctypes
from ctypes import c_uint8, c_uint16, c_uint32, c_double, c_float, c_int16, c_int32
from collections import OrderedDict

msg_flag_field_table = (
    'stamp', 'quat', 'acc', 'lin_vel', 'ang_vel', 'gps', 'mag', 'rc',
    'gim', 'status', 'batt', 'cmd', 'res0', 'res1', 'res2', 'res3')

msg_flag_struct_table = zip(
    msg_flag_field_table,
    [c_uint8] * len(msg_flag_field_table),
    [1] * len(msg_flag_field_table),)

msg_info = dict()
msg_info['stamp'] = ('2IB', ['time', 'asr_ts', 'sync_flag'])
msg_info['quat'] = ('4f', ['q0', 'q1', 'q2', 'q3'])
msg_info['acc'] = ('3f', ['ax', 'ay', 'az'])
msg_info['lin_vel'] = ('3fB', ['vx', 'vy', 'vz', 'vel_flag'])
msg_info['ang_vel'] = ('3f', ['wx', 'wy', 'wz'])
msg_info['gps'] = ('2d2fB', ['longti', 'lati', 'alti',
                              'height', 'health_flag'])
msg_info['mag'] = ('3h', ['mx', 'my', 'mz'])
msg_info['rc'] = ('6h', ['roll', 'pitch', 'yaw',
                          'throttle', 'mode', 'gear'])
msg_info['gim'] = ('3fB', ['gimroll', 'gimpitch', 'gimyaw','limit'])
msg_info['status'] = ('B', ['status'])
msg_info['batt'] = ('B', ['status'])
msg_info['cmd'] = ('2B', ['mode','status'])


class MessageFlagStruct(ctypes.LittleEndianStructure):
    _fields_ = msg_flag_struct_table


class MessageFlagUnion(ctypes.Union):
    _fields_ = [('buf', ctypes.ARRAY(c_uint8, 2)),
                ('data', MessageFlagStruct)]


def encode_message(s):
    pass


def decode_message(s):
    u = MessageFlagUnion()
    u.buf[0] = ord(s[0])
    u.buf[1] = ord(s[1])
    # print('flag:{}'.format(bytesToBinStr(s[:2])))
    fmts = ['<']
    keys = []
    for f in msg_flag_field_table:
        # print('flag[{}]={}'.format(f, eval('u.data.' + f)))
        if u.data.__getattribute__(f):
            fmts.append(msg_info[f][0])
            keys += msg_info[f][1]
    fmt = ''.join(fmts)
    values = struct.unpack(fmt, s[2:])
    d = OrderedDict(zip(keys,values))
    # print d

if __name__ == '__main__':
	pass
    #decode_message('\x01\x10')
