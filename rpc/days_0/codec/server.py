import socket
import logging
import json
from sys import argv
import threading

_lock = threading.Lock()


from rpc.days_0.codec import const
from rpc.days_0.codec.codec import NewCodecFuncMap, Codec

logger = logging.getLogger(__file__)

class Option():
    def __init__(self, codec_type, magic_number=None):
        self.magic_number = magic_number or const.MagicNumber
        self.codec_type = codec_type

DefaultOption = Option(codec_type=const.CodeType.GobType, magic_number=const.MagicNumber)

class Request():
    def __init__(self, header, argv, replyv):
        self.header = header
        self.argv = argv
        self.replyv = replyv

class Server():
    def __init__(self):
        self.s = socket.socket()
        self.host = "127.0.0.1"
        self.port = '9999'
        self.s.bind((self.host, self.port))
        self.s.listen(5)

    def accept(self):
        while True:
            try:
                conn, addr = self.s.accept()
            except Exception as e:
                logger.error(f"{e}")
            # TODO 开启子协程处理

    def serverconn(self, conn):
        opt: Option =  json.loads(conn).decode()
        if opt.magic_number != const.MagicNumber:
            logger.error('rpc server error: invalid magic number')
            return

        func_codec = NewCodecFuncMap[opt.codec_type]

        if not func_codec:
            logger.error('rpc server error: rpc invalid type')

        self.servercodec(func_codec(conn))

    def servercodec(self, codec):
        _lock.acquire()
        while True:
            pass

    def read_request_header(self, codec:Codec):
        header = codec.readheader()
        return header

    def read_request(self, codec:Codec):
        header = self.read_request_header(codec)
    

    def close(self):
        self.c.close()


