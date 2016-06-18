import struct


class ACUDPProtoTypes(object):
    ACSP_ADMIN_COMMAND = 209
    ACSP_BROADCAST_CHAT = 203
    ACSP_CAR_INFO = 54
    ACSP_CAR_UPDATE = 53
    ACSP_CE_COLLISION_WITH_CAR = 10
    ACSP_CE_COLLISION_WITH_ENV = 11
    ACSP_CHAT = 57
    ACSP_CLIENT_EVENT = 130
    ACSP_CLIENT_LOADED = 58
    ACSP_CONNECTION_CLOSED = 52
    ACSP_END_SESSION = 55
    ACSP_ERROR = 60
    ACSP_GET_CAR_INFO = 201
    ACSP_GET_SESSION_INFO = 204
    ACSP_KICK_USER = 206
    ACSP_LAP_COMPLETED = 73
    ACSP_NEW_CONNECTION = 51
    ACSP_NEW_SESSION = 50
    ACSP_NEXT_SESSION = 207
    ACSP_REALTIMEPOS_INTERVAL = 200
    ACSP_RESTART_SESSION = 208
    ACSP_SEND_CHAT = 202
    ACSP_SESSION_INFO = 59
    ACSP_SET_SESSION_INFO = 205
    ACSP_VERSION = 56

    @classmethod
    def id_to_name(cls, id_):
        for attr in cls.__dict__.keys():
            if attr.startswith('ACSP_'):
                if getattr(cls, attr) == id_:
                    return attr
        return None


class ACUDPStruct(object):
    def __init__(self, fmt, formatter=lambda x: x):
        self.fmt = fmt
        self.formatter = formatter

    def size(self):
        return struct.calcsize(self.fmt)

    def get(self, file_obj):
        data = struct.unpack(self.fmt, file_obj.read(self.size()))
        if len(data) == 1:
            return self.formatter(data[0])
        return self.formatter(data)


class ACUDPString(object):
    def __init__(self, char_size, decoder=lambda x: x.decode('ascii')):
        self.char_size = char_size
        self.decoder = decoder

    def get(self, file_obj):
        size = UINT8.get(file_obj)
        return self.decoder(file_obj.read(self.char_size*size))


class ACUDPConditionalStruct(object):
    def __init__(self, ac_struct, formatter=lambda x: x,
                 cond_func=lambda x: True, default=''):
        self.ac_struct = ac_struct
        self.cond_func = cond_func
        self.default = default
        self.formatter = formatter

    def size(self):
        return self.ac_struct.size()

    def get(self, file_obj, context=None):
        if not self.cond_func(context):
            return self.default
        return self.formatter(self.ac_struct.get(file_obj, context))


UINT8 = ACUDPStruct('B')
BOOL = ACUDPStruct('B', formatter=lambda x: x != 0)
UINT16 = ACUDPStruct('H')
INT16 = ACUDPStruct('h')
UINT32 = ACUDPStruct('I')
INT32 = ACUDPStruct('i')
FLOAT = ACUDPStruct('f')
VECTOR3F = ACUDPStruct('fff')
UTF32 = ACUDPString(4, decoder=lambda x: x.decode('utf32'))
ASCII = ACUDPString(1, decoder=lambda x: x.decode('ascii'))
