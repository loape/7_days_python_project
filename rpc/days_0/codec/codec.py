import logging
import io
from abc import abstractmethod
from rpc.days_0.codec import const

logger = logging.getLogger(__file__)

class EncodeHeaderException(BaseException):
    pass

class EncodeBodyException(BaseException):
    pass

class Header():
    def __init__(self, service_method:str, seq:int, error:str):
        self.service_method:str  = service_method
        self.seq: int = seq
        self.error: str = error

class Codec():

    @abstractmethod
    def readheader(self, *args, **kwargs):
        raise

    @abstractmethod
    def readbody(self, *args, **kwargs):
        raise

    @abstractmethod
    def close(self, *args, **kwargs):
        pass

    @abstractmethod
    def write(self, *args, **kwargs):
        pass

class GobCodec(Codec):
    def __init__(self, conn, buf, dec, enc):
        self.conn = conn # 连接
        self.buf = buf or io.BufferedWriter  # 缓冲
        self.dec = dec  # 解码
        self.enc = enc  # 转码

    def readheader(self, h:Header) -> str:
        return self.dec.decode(h)

    def readbody(self, body:object) -> str:
        return self.dec.decode(body)

    def write(self, h:Header, body: object) -> str:
        try:
            self.enc.encode(h)
            self.enc.encode(body)
        except EncodeHeaderException as e:
            logger.error(f"Encode Header Error: {e}")
        except EncodeBodyException as e:
            logger.error(f"Encode Body Error: {e}")
        except Exception as e:
            logger.error(f"Not Known Error: {e}")
        finally:
            self.close()
        
    def close(self):
        self.conn.close()

    def __enter__(self):
        pass

    def __exit__(self, exec):
        self.conn.close()


NewCodecFuncMap = {const.CodeType.GobType: GobCodec}
    
    
    
